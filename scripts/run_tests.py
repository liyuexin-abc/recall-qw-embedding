"""
全量测试脚本：调用 /api/recall 对 data/tests.json 中的 59 条用例进行召回，
并按 "指标名 / 维度名 / 维度值" 维度评估命中情况，输出 JSON 报告 + Markdown 报告。

判断逻辑（综合判断，标准答案可能不完全准确）：
1) 解析期望答案中的「指标名」「维度名」「维度值」三类。
2) 在召回的候选集合（合并去重后的全部候选）中匹配：
   - metric / derived_metric 命中 -> 算指标命中
   - dimension 命中               -> 算维度命中
   - dim_value 命中               -> 算维度值命中
3) 名称匹配采用 "去单位 + 去括号 + 大小写无关 + 双向子串包含" 的宽松匹配，
   维度还会查询其 display_name 列表（'地区' 对应 'region_name' 等）。
4) 同时记录 Top-K 命中（K=5/10/20/50）以观察排名分布。

可通过 --api 改为远程地址；默认 http://localhost:8000/api/recall。
"""
import json
import re
import time
import sys
import os
import argparse
import requests

DEFAULT_API = "http://localhost:8000/api/recall"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_PATH = os.path.join(ROOT, "data", "tests.json")
OUTPUT_JSON = os.path.join(ROOT, "data", "test_report.json")
OUTPUT_MD = os.path.join(ROOT, "data", "test_report.md")
TOPK_LIST = [5, 10, 20, 50]

# 维度别名映射：用户回答里写 "地区"，实际维度 dimension_name=region_name display_name=地区
DIM_ALIAS = {
    "地区": ["region_name", "地区", "地区名", "省份", "省"],
    "电站": ["name", "名称", "电站名", "电站名称"],
    "名称": ["name", "名称"],
    "测点": ["point_name", "测点名"],
    "测点名": ["point_name", "测点名"],
    "发电类型": ["gen_type", "发电类型"],
    "送受电方向": ["power_flow_direction", "送受电方向"],
    "调管机构": ["dispatch_org", "调管机构"],
    "市级区域": ["city_belong", "市级区域", "城市"],
    "停电类型": ["power_outage_type", "停电类型"],
    "故障所属维护单位": ["fault_maintain_unit", "故障所属维护单位", "维护单位"],
    "线路名称": ["line_name", "线路名称", "线路"],
    "断面名": ["section_name", "断面名", "断面"],
    "越限状态": ["limit_status", "越限状态"],
    "电压等级": ["voltage_level", "电压等级"],
    "时间": ["ptdate", "日期"],
    "日期": ["ptdate", "日期"],
}


def normalize(name: str) -> str:
    """去括号内单位、去空白、转小写"""
    if not name:
        return ""
    s = re.sub(r"[\(（][^()（）]*[\)）]", "", name)  # 去掉括号及其内容
    s = re.sub(r"\s+", "", s)
    return s.strip().lower()


def parse_answer(answer: str):
    """解析「指标名：A、B；维度名：C；维度值：D、E」格式（同时容忍 "维度" "值" 等同义键）"""
    out = {"metrics": [], "dimensions": [], "values": []}
    if not answer:
        return out
    parts = re.split(r"[;；]", answer)
    for p in parts:
        if "：" not in p and ":" not in p:
            continue
        kv = re.split(r"[:：]", p, maxsplit=1)
        if len(kv) != 2:
            continue
        key, val = kv[0].strip(), kv[1].strip()
        items = [x.strip() for x in re.split(r"[、,，]+", val) if x.strip()]
        if "指标" in key:
            out["metrics"].extend(items)
        elif "维度名" in key or key == "维度":
            out["dimensions"].extend(items)
        elif "维度值" in key or key == "值":
            out["values"].extend(items)
    return out


def expand_aliases(text: str):
    """对维度名扩展到一组别名（含 dimension_name code 自身），用于宽松匹配"""
    if text in DIM_ALIAS:
        return [normalize(x) for x in DIM_ALIAS[text]] + [normalize(text)]
    return [normalize(text)]


def is_match(expected: str, candidate_names: list, expand=False) -> bool:
    """双向子串包含"""
    targets = expand_aliases(expected) if expand else [normalize(expected)]
    for cn in candidate_names:
        cn_norm = normalize(cn)
        if not cn_norm:
            continue
        for t in targets:
            if not t:
                continue
            if t in cn_norm or cn_norm in t:
                return True
    return False


def find_match_rank(expected: str, candidates: list, target_types: set, expand=False):
    """在候选列表中找到第一个匹配项，返回 {hit, rank, score, name, source} 或 {hit:False}"""
    for idx, c in enumerate(candidates):
        if c.get("entity_type") not in target_types:
            continue
        names = [c.get("display_name", "")]
        # 候选项的 description 中可能含 dimension_name code
        if c.get("entity_type") == "dimension":
            # display_name 是 "地区"，dimension_name code 在 description 中已写入。
            # 但前端响应没暴露 dimension_name —— 此处把 description 也作为候选名
            names.append(c.get("description", ""))
        if is_match(expected, names, expand=expand):
            return {
                "hit": True,
                "rank": idx + 1,
                "score": round(c.get("score", 0), 4),
                "name": c.get("display_name"),
                "source": c.get("source"),
            }
    return {"hit": False}


def evaluate_one(expected: dict, candidates: list) -> dict:
    metric_hits, dim_hits, val_hits = [], [], []
    for m in expected["metrics"]:
        # 综合判断：先在指标里找；找不到再在维度里找（金标可能把日期/计数类维度误标为指标）
        r = find_match_rank(m, candidates, {"metric", "derived_metric"})
        if not r.get("hit"):
            r2 = find_match_rank(m, candidates, {"dimension"})
            if r2.get("hit"):
                r2["soft_match"] = "matched-as-dimension"
                r = r2
        metric_hits.append({"expected": m, **r})
    for d in expected["dimensions"]:
        dim_hits.append({"expected": d,
                         **find_match_rank(d, candidates, {"dimension"}, expand=True)})
    for v in expected["values"]:
        val_hits.append({"expected": v,
                         **find_match_rank(v, candidates, {"dim_value"})})

    def hit_rate(items):
        if not items:
            return None
        return sum(1 for x in items if x.get("hit")) / len(items)

    def topk_hits(items, k):
        if not items:
            return None
        return sum(1 for x in items if x.get("hit") and x.get("rank", 9999) <= k) / len(items)

    return {
        "metric_hits": metric_hits,
        "dimension_hits": dim_hits,
        "value_hits": val_hits,
        "metric_recall": hit_rate(metric_hits),
        "dimension_recall": hit_rate(dim_hits),
        "value_recall": hit_rate(val_hits),
        "topk": {
            f"top{k}": {
                "metric": topk_hits(metric_hits, k),
                "dimension": topk_hits(dim_hits, k),
                "value": topk_hits(val_hits, k),
            } for k in TOPK_LIST
        },
        "all_hit": all(
            (rate is None or rate == 1.0)
            for rate in [hit_rate(metric_hits), hit_rate(dim_hits), hit_rate(val_hits)]
        )
    }


def _avg(results, key):
    vals = [r["evaluation"][key] for r in results
            if "evaluation" in r and r["evaluation"].get(key) is not None]
    return round(sum(vals) / len(vals), 4) if vals else None


def _topk_avg(results, k, kind):
    vals = []
    for r in results:
        if "evaluation" not in r:
            continue
        v = r["evaluation"]["topk"].get(f"top{k}", {}).get(kind)
        if v is not None:
            vals.append(v)
    return round(sum(vals) / len(vals), 4) if vals else None


def write_markdown(out: dict, path: str):
    s = out["summary"]
    lines = []
    lines.append("# 召回服务测试报告\n")
    lines.append(f"- 测试用例数：**{s['total']}**")
    lines.append(f"- 用时：{s['elapsed_seconds']}s（平均 {s['avg_per_query_ms']} ms/query）")
    lines.append(f"- 三类全部命中（all_hit）：**{s['all_hit']}** / {s['total']}（{s['all_hit']/max(s['total'],1):.1%}）")
    lines.append("")
    lines.append("## 整体命中率")
    lines.append("| 类型 | 平均命中率 |")
    lines.append("| --- | --- |")
    lines.append(f"| 指标 | {s['metric_recall_avg']} |")
    lines.append(f"| 维度 | {s['dimension_recall_avg']} |")
    lines.append(f"| 维度值 | {s['value_recall_avg']} |")
    lines.append("")
    lines.append("## Top-K 命中率")
    lines.append("| K | 指标 | 维度 | 维度值 |")
    lines.append("| --- | --- | --- | --- |")
    for k in TOPK_LIST:
        v = s["topk_avg"][f"top{k}"]
        lines.append(f"| {k} | {v['metric']} | {v['dimension']} | {v['value']} |")
    lines.append("")
    lines.append("## 用例详情")
    for r in out["details"]:
        if "evaluation" not in r:
            lines.append(f"- ❌ [{r.get('id')}] {r.get('question')} — error: {r.get('error')}")
            continue
        ev = r["evaluation"]
        flag = "✅" if ev["all_hit"] else "❌"
        lines.append(f"### {flag} [{r['id']}] {r['question']}")
        lines.append(f"- 期望：{r['expected']}")
        lines.append(f"- 候选数：{r['candidate_count']}, "
                     f"指标={ev['metric_recall']} 维度={ev['dimension_recall']} 维度值={ev['value_recall']}")
        if ev["metric_hits"]:
            lines.append("- 指标命中：")
            for x in ev["metric_hits"]:
                if x.get("hit"):
                    lines.append(f"  - ✓ `{x['expected']}` → {x['name']} (rank={x['rank']}, score={x['score']}, src={x.get('source')})")
                else:
                    lines.append(f"  - ✗ `{x['expected']}`")
        if ev["dimension_hits"]:
            lines.append("- 维度命中：")
            for x in ev["dimension_hits"]:
                if x.get("hit"):
                    lines.append(f"  - ✓ `{x['expected']}` → {x['name']} (rank={x['rank']}, score={x['score']}, src={x.get('source')})")
                else:
                    lines.append(f"  - ✗ `{x['expected']}`")
        if ev["value_hits"]:
            lines.append("- 维度值命中：")
            for x in ev["value_hits"]:
                if x.get("hit"):
                    lines.append(f"  - ✓ `{x['expected']}` → {x['name']} (rank={x['rank']}, score={x['score']}, src={x.get('source')})")
                else:
                    lines.append(f"  - ✗ `{x['expected']}`")
        lines.append("- Top-10 候选：")
        for c in r.get("top10_candidates", []):
            lines.append(f"  - [{c['entity_type']}] {c['display_name']} (score={c['score']}, src={c['source']})")
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default=DEFAULT_API)
    ap.add_argument("--tests", default=TESTS_PATH)
    ap.add_argument("--output", default=OUTPUT_JSON)
    ap.add_argument("--md", default=OUTPUT_MD)
    args = ap.parse_args()

    with open(args.tests, encoding="utf-8") as f:
        tests = json.load(f)

    print(f"Loaded {len(tests)} tests; calling {args.api}")
    results = []
    t0 = time.time()
    for i, t in enumerate(tests, 1):
        q = t["question"]
        expected = parse_answer(t.get("answer", ""))
        try:
            r = requests.post(args.api, json={"query": q}, timeout=60).json()
            cands = r.get("candidates", [])
        except Exception as e:
            print(f"[{i}] ERROR: {e}")
            results.append({**t, "error": str(e)})
            continue
        ev = evaluate_one(expected, cands)
        rec = {
            "id": t.get("id", i),
            "question": q,
            "answer": t.get("answer", ""),
            "expected": expected,
            "candidate_count": len(cands),
            "timings_ms": r.get("timings_ms"),
            "evaluation": ev,
            "top10_candidates": [
                {"entity_type": c["entity_type"], "display_name": c.get("display_name"),
                 "score": round(c.get("score", 0), 4),
                 "source": c.get("source")}
                for c in cands[:10]
            ],
        }
        results.append(rec)
        flag = "✓" if ev["all_hit"] else "✗"
        print(f"[{i:2d}] {flag} m={ev['metric_recall']} d={ev['dimension_recall']} "
              f"v={ev['value_recall']} | {q[:40]}")

    elapsed = time.time() - t0
    summary = {
        "total": len(results),
        "elapsed_seconds": round(elapsed, 2),
        "avg_per_query_ms": round(elapsed * 1000 / max(len(results), 1), 1),
        "all_hit": sum(1 for r in results if r.get("evaluation", {}).get("all_hit")),
        "metric_recall_avg": _avg(results, "metric_recall"),
        "dimension_recall_avg": _avg(results, "dimension_recall"),
        "value_recall_avg": _avg(results, "value_recall"),
        "topk_avg": {
            f"top{k}": {
                "metric": _topk_avg(results, k, "metric"),
                "dimension": _topk_avg(results, k, "dimension"),
                "value": _topk_avg(results, k, "value"),
            } for k in TOPK_LIST
        }
    }
    out = {"summary": summary, "details": results}
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    write_markdown(out, args.md)

    print("\n===== SUMMARY =====")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\nReports saved -> {args.output}\n             -> {args.md}")


if __name__ == "__main__":
    main()
