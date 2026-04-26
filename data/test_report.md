# 召回服务测试报告

- 测试用例数：**59**
- 用时：28.32s（平均 479.9 ms/query）
- 三类全部命中（all_hit）：**58** / 59（98.3%）

## 整体命中率
| 类型 | 平均命中率 |
| --- | --- |
| 指标 | 1.0 |
| 维度 | 1.0 |
| 维度值 | 0.9767 |

## Top-K 命中率
| K | 指标 | 维度 | 维度值 |
| --- | --- | --- | --- |
| 5 | 0.7825 | 0.0254 | 0.3062 |
| 10 | 0.8559 | 0.0763 | 0.3682 |
| 20 | 0.9153 | 0.1525 | 0.4651 |
| 50 | 0.9831 | 0.5508 | 0.5698 |

## 用例详情
### ✅ [1] 去年1月份广东-阳江海上风电场的新能源最大出力是多少
- 期望：{'metrics': ['新能源最大出力(MW)'], 'dimensions': ['名称'], 'values': ['广东-阳江海上风电场']}
- 候选数：99, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `新能源最大出力(MW)` → 新能源最大出力(MW) (rank=2, score=0.729, src=path_a)
- 维度命中：
  - ✓ `名称` → 名称 (rank=26, score=0.5697, src=path_a)
- 维度值命中：
  - ✓ `广东-阳江海上风电场` → 广东-阳江海上风电场 (rank=3, score=0.7248, src=path_a)
- Top-10 候选：
  - [table] 新能源运行情况 (score=0.735, src=path_a)
  - [metric] 新能源最大出力(MW) (score=0.729, src=path_a)
  - [dim_value] 广东-阳江海上风电场 (score=0.7248, src=path_a)
  - [metric] 最大出力(MW) (score=0.7184, src=path_a)
  - [metric] 实际出力(MW) (score=0.6811, src=path_a)
  - [metric] 最大受限出力(MW) (score=0.6759, src=path_a)
  - [table] 新能源信息填报 (score=0.6691, src=path_a)
  - [metric] 最小出力(MW) (score=0.6483, src=path_a)
  - [metric] 新能源控制最大电力(MW) (score=0.6471, src=path_b)
  - [metric] 新能源最大渗透率(%) (score=0.6471, src=path_b)

### ✅ [2] 去年1月1号广西受海南的实际电量是多少？
- 期望：{'metrics': ['全天实际电量（MWh）'], 'dimensions': ['送受电方向'], 'values': ['广西受海南']}
- 候选数：156, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `全天实际电量（MWh）` → 全天实际电量（MWh） (rank=6, score=0.7182, src=path_a)
- 维度命中：
  - ✓ `送受电方向` → 送受电方向 (rank=72, score=0.6276, src=path_a)
- 维度值命中：
  - ✓ `广西受海南` → 广西受海南 (rank=4, score=0.7296, src=path_a)
- Top-10 候选：
  - [table] 送受电量 (score=0.7912, src=path_a)
  - [table] 发受电量 (score=0.7466, src=path_a)
  - [dim_value] 海南送广西 (score=0.741, src=path_a)
  - [dim_value] 广西受海南 (score=0.7296, src=path_a)
  - [dim_value] 广西送广东 (score=0.7196, src=path_a)
  - [metric] 全天实际电量（MWh） (score=0.7182, src=path_a)
  - [dim_value] 广东送海南 (score=0.711, src=path_a)
  - [dim_value] 广西送贵州 (score=0.7005, src=path_a)
  - [dim_value] 贵州送海南 (score=0.6973, src=path_a)
  - [metric] 全电量_中调(MWh) (score=0.6921, src=path_a)

### ✅ [3] 3月4号乌东西岸电厂的电压数据是多少
- 期望：{'metrics': ['数据值'], 'dimensions': ['测点名'], 'values': ['乌东西岸电厂电压']}
- 候选数：135, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `数据值` → 数据值 (rank=22, score=0.6726, src=path_a)
- 维度命中：
  - ✓ `测点名` → 测点名 (rank=23, score=0.6623, src=path_a)
- 维度值命中：
  - ✓ `乌东西岸电厂电压` → 乌东西岸电厂电压 (rank=1, score=0.8566, src=path_a)
- Top-10 候选：
  - [dim_value] 乌东西岸电厂电压 (score=0.8566, src=path_a)
  - [dim_value] 乌东西岸电厂电流 (score=0.8126, src=path_a)
  - [dim_value] 乌东西岸电厂有功功率 (score=0.8091, src=path_a)
  - [dim_value] 乌东西岸电厂实时出力 (score=0.7959, src=path_a)
  - [dim_value] 乌东西岸电厂频率 (score=0.7952, src=path_a)
  - [dim_value] 乌东西岸电厂无功功率 (score=0.7942, src=path_a)
  - [dim_value] 乌东德电厂电压 (score=0.7776, src=path_a)
  - [dim_value] 乌东德电厂电流 (score=0.7477, src=path_a)
  - [dim_value] 乌东德电厂有功功率 (score=0.7423, src=path_a)
  - [dim_value] 乌东德电厂无功功率 (score=0.7356, src=path_a)

### ✅ [4] 云南省2025年1月1号地调最高时的时间是多少？
- 期望：{'metrics': ['最高时间_地调'], 'dimensions': ['地区'], 'values': ['云南']}
- 候选数：135, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `最高时间_地调` → 最高时间_地调 (rank=1, score=0.6568, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=19, score=0.548, src=path_c)
- 维度值命中：
  - ✓ `云南` → 云南外送断面 (rank=5, score=0.5953, src=path_a)
- Top-10 候选：
  - [dimension] 最高时间_地调 (score=0.6568, src=path_a)
  - [metric] 最高_地调（MW） (score=0.6318, src=path_a)
  - [dimension] 最低时间_地调 (score=0.6187, src=path_a)
  - [table] 负荷与备用 (score=0.6106, src=path_a)
  - [dim_value] 云南外送断面 (score=0.5953, src=path_a)
  - [dimension] 最高时间_中调 (score=0.591, src=path_a)
  - [dimension] 最高时间_统调 (score=0.581, src=path_a)
  - [metric] 最高_统调（MW） (score=0.5751, src=path_a)
  - [metric] 最低_地调（MW） (score=0.5669, src=path_a)
  - [metric] 峰谷差_地调(MW) (score=0.5652, src=path_a)

### ✅ [5] 佛山地调及南方总调累计跳闸多少次？
- 期望：{'metrics': ['停电时间（计数）'], 'dimensions': ['调管机构', '停电类型'], 'values': ['佛山地调', '南方总调']}
- 候选数：132, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `停电时间（计数）` → 停电时间 (rank=57, score=0.524, src=path_a)
- 维度命中：
  - ✓ `调管机构` → 调管机构 (rank=12, score=0.6341, src=path_a)
  - ✓ `停电类型` → 停电类型 (rank=31, score=0.5853, src=path_a)
- 维度值命中：
  - ✓ `佛山地调` → 佛山地调 (rank=2, score=0.7178, src=path_a)
  - ✓ `南方总调` → 南方总调 (rank=9, score=0.6396, src=path_a)
- Top-10 候选：
  - [table] 跳闸情况 (score=0.7767, src=path_a)
  - [dim_value] 佛山地调 (score=0.7178, src=path_a)
  - [dim_value] 广州地调 (score=0.6719, src=path_a)
  - [metric] 停电影响用户数（可为空） (score=0.6701, src=path_b)
  - [dim_value] 广东中调 (score=0.6658, src=path_a)
  - [dim_value] 佛山供电局 (score=0.6597, src=path_a)
  - [metric] 复电用户数（可为空） (score=0.6551, src=path_a)
  - [dim_value] 深圳地调 (score=0.6431, src=path_a)
  - [dim_value] 南方总调 (score=0.6396, src=path_a)
  - [dim_value] 广西中调 (score=0.6368, src=path_a)

### ✅ [6] 2025年1月1号新能源控制电量大于9000的电站是哪个？
- 期望：{'metrics': ['新能源控制电量(MWh)'], 'dimensions': ['名称'], 'values': []}
- 候选数：117, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `新能源控制电量(MWh)` → 新能源控制电量(MWh) (rank=1, score=0.8234, src=path_a)
- 维度命中：
  - ✓ `名称` → 名称 (rank=22, score=0.6565, src=path_a)
- Top-10 候选：
  - [metric] 新能源控制电量(MWh) (score=0.8234, src=path_a)
  - [table] 新能源运行情况 (score=0.7855, src=path_a)
  - [metric] 新能源控制最大电力(MW) (score=0.7569, src=path_a)
  - [table] 发受电量 (score=0.743, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.7344, src=path_a)
  - [table] 新能源信息填报 (score=0.7302, src=path_a)
  - [metric] 装机容量(MW) (score=0.7165, src=path_a)
  - [metric] 受限电量(MWh) (score=0.6887, src=path_a)
  - [metric] 统调上网电量(MWh) (score=0.687, src=path_a)
  - [metric] 发电量(MWh) (score=0.6869, src=path_a)

### ✅ [7] 去年全网各类型新能源发电量分别是多少
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['发电类型', '地区'], 'values': ['风能', '集中式光伏', '统调光伏', '总分布式光伏', '总光伏', '生物质']}
- 候选数：115, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 新能源发电量(MWh) (rank=1, score=0.8089, src=path_a)
- 维度命中：
  - ✓ `发电类型` → 发电类型 (rank=4, score=0.7529, src=path_a)
  - ✓ `地区` → 调管机构 (rank=77, score=0.5453, src=path_c)
- 维度值命中：
  - ✓ `风能` → 风能 (rank=12, score=0.6996, src=path_a)
  - ✓ `集中式光伏` → 集中式光伏 (rank=63, score=0.6503, src=path_a)
  - ✓ `统调光伏` → 统调光伏 (rank=59, score=0.6815, src=path_a)
  - ✓ `总分布式光伏` → 总分布式光伏 (rank=9, score=0.7175, src=path_a)
  - ✓ `总光伏` → 总光伏 (rank=5, score=0.743, src=path_a)
  - ✓ `生物质` → 生物质 (rank=60, score=0.677, src=path_a)
- Top-10 候选：
  - [metric] 新能源发电量(MWh) (score=0.8089, src=path_a)
  - [table] 发受电量 (score=0.8053, src=path_a)
  - [table] 新能源信息填报 (score=0.7855, src=path_a)
  - [dimension] 发电类型 (score=0.7529, src=path_a)
  - [dim_value] 总光伏 (score=0.743, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.7376, src=path_a)
  - [metric] 发电量(MWh) (score=0.7293, src=path_a)
  - [metric] 总计_统调发电 (score=0.7288, src=path_a)
  - [dim_value] 总分布式光伏 (score=0.7175, src=path_a)
  - [metric] 装机容量(MW) (score=0.714, src=path_a)

### ✅ [8] 2026年跳闸重合成功的次数是多少？
- 期望：{'metrics': ['停电时间（计数）'], 'dimensions': ['停电类型'], 'values': ['跳闸重合成功']}
- 候选数：121, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `停电时间（计数）` → 停电时间 (rank=22, score=0.574, src=path_a)
- 维度命中：
  - ✓ `停电类型` → 停电类型 (rank=11, score=0.6325, src=path_d)
- 维度值命中：
  - ✓ `跳闸重合成功` → 跳闸重合成功 (rank=2, score=0.7479, src=path_a)
- Top-10 候选：
  - [table] 跳闸情况 (score=0.7679, src=path_a)
  - [dim_value] 跳闸重合成功 (score=0.7479, src=path_a)
  - [derived_metric] 跳闸重合成功次数 (score=0.7441, src=path_d)
  - [metric] 复电用户数（可为空） (score=0.7285, src=path_a)
  - [dimension] 重合闸动作情况 (score=0.6854, src=path_a)
  - [metric] 停电影响用户数（可为空） (score=0.6808, src=path_a)
  - [metric] 已恢复负荷(MW)（可为空） (score=0.662, src=path_a)
  - [metric] 损失负荷(MW)（可为空） (score=0.6577, src=path_a)
  - [dimension] 送电情况 (score=0.6507, src=path_a)
  - [metric] 损失电量(万kWh)（固定为空）(MWh) (score=0.6429, src=path_a)

### ✅ [9] 2026年3月前3天发生跳闸的线路名称有哪些？
- 期望：{'metrics': ['停电时间'], 'dimensions': ['停电类型', '线路名称'], 'values': ['跳闸']}
- 候选数：122, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `停电时间` → 停电时间 (rank=23, score=0.6017, src=path_a)
- 维度命中：
  - ✓ `停电类型` → 停电类型 (rank=10, score=0.6523, src=path_a)
  - ✓ `线路名称` → 线路名称 (rank=16, score=0.6112, src=path_a)
- 维度值命中：
  - ✓ `跳闸` → 跳闸 (rank=6, score=0.6904, src=path_a)
- Top-10 候选：
  - [table] 跳闸情况 (score=0.815, src=path_a)
  - [metric] 复电用户数（可为空） (score=0.7126, src=path_a)
  - [metric] 停电影响用户数（可为空） (score=0.7088, src=path_a)
  - [metric] 损失负荷(MW)（可为空） (score=0.7049, src=path_a)
  - [metric] 已恢复负荷(MW)（可为空） (score=0.691, src=path_a)
  - [dim_value] 跳闸 (score=0.6904, src=path_a)
  - [metric] 损失电量(万kWh)（固定为空）(MWh) (score=0.6856, src=path_a)
  - [dim_value] 跳闸重合成功 (score=0.6597, src=path_a)
  - [table] 断面表 (score=0.6587, src=path_a)
  - [dimension] 停电类型 (score=0.6523, src=path_a)

### ✅ [10] 今年的全网新能源发电量是多少
- 期望：{'metrics': ['新能源发电量'], 'dimensions': ['地区'], 'values': ['广东', '广西', '海南', '云南', '贵州']}
- 候选数：112, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `新能源发电量` → 新能源发电量(MWh) (rank=1, score=0.8163, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=75, score=0.5172, src=path_c)
- 维度值命中：
  - ✓ `广东` → 广东-江门生物质电站 (rank=73, score=0.5298, src=path_a)
  - ✓ `广西` → 广西-南宁光伏电站 (rank=78, score=0.5076, src=path_a)
  - ✓ `海南` → 海南-东方农光互补 (rank=95, score=0.4596, src=path_a)
  - ✓ `云南` → 云南-楚雄光伏电站 (rank=83, score=0.4919, src=path_a)
  - ✓ `贵州` → 贵州-毕节风电场 (rank=89, score=0.4754, src=path_a)
- Top-10 候选：
  - [metric] 新能源发电量(MWh) (score=0.8163, src=path_a)
  - [table] 发受电量 (score=0.7893, src=path_a)
  - [table] 新能源信息填报 (score=0.7728, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.737, src=path_a)
  - [metric] 发电量(MWh) (score=0.731, src=path_a)
  - [metric] 总计_统调发电 (score=0.7203, src=path_a)
  - [metric] 装机容量(MW) (score=0.711, src=path_a)
  - [metric] 新能源控制电量(MWh) (score=0.7052, src=path_a)
  - [table] 新能源运行情况 (score=0.701, src=path_a)
  - [metric] 统调上网电量(MWh) (score=0.6958, src=path_a)

### ✅ [11] 今年一月份广东的统调发受电量和实际出力各是多少？
- 期望：{'metrics': ['统调发受电量', '实际出力(MW)'], 'dimensions': ['地区'], 'values': ['广东']}
- 候选数：133, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `统调发受电量` → 统调发受电量(MWh) (rank=2, score=0.7744, src=path_a)
  - ✓ `实际出力(MW)` → 实际出力(MW) (rank=11, score=0.721, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=59, score=0.6209, src=path_c)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=61, score=0.6043, src=path_a)
- Top-10 候选：
  - [table] 发受电量 (score=0.7911, src=path_a)
  - [metric] 统调发受电量(MWh) (score=0.7744, src=path_a)
  - [metric] 统调发受电量_中调(MWh) (score=0.7709, src=path_a)
  - [metric] 统调受电量(MWh) (score=0.7661, src=path_a)
  - [metric] 统调发电量(MWh) (score=0.7482, src=path_a)
  - [metric] 统调受电量_中调(MWh) (score=0.748, src=path_a)
  - [metric] 统调还原后发受电量(MWh) (score=0.7331, src=path_a)
  - [metric] 统调上网电量(MWh) (score=0.73, src=path_a)
  - [metric] 统调发受电量含分布式光伏(MWh) (score=0.7297, src=path_a)
  - [metric] 燃煤火电_统调发电 (score=0.7219, src=path_a)

### ✅ [12] 今年1月份和2月份广东的新能源发电量是多少？
- 期望：{'metrics': ['新能源发电量'], 'dimensions': ['地区'], 'values': ['广东']}
- 候选数：114, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `新能源发电量` → 新能源发电量(MWh) (rank=2, score=0.7672, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=78, score=0.5665, src=path_c)
- 维度值命中：
  - ✓ `广东` → 广东-江门生物质电站 (rank=60, score=0.6271, src=path_a)
- Top-10 候选：
  - [table] 发受电量 (score=0.7684, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.7672, src=path_a)
  - [table] 新能源信息填报 (score=0.7535, src=path_a)
  - [metric] 发电量(MWh) (score=0.7069, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.7002, src=path_a)
  - [metric] 总计_统调发电 (score=0.6984, src=path_a)
  - [table] 新能源运行情况 (score=0.6983, src=path_a)
  - [metric] 装机容量(MW) (score=0.6808, src=path_a)
  - [metric] 统调发电量(MWh) (score=0.673, src=path_a)
  - [metric] 风力发电_统调发电 (score=0.6716, src=path_b)

### ✅ [13] 2025年11月25日广东区域的统调核电上网电量和统调水电上网电量是多少？
- 期望：{'metrics': ['统调核电上网电量', '统调水电上网电量'], 'dimensions': ['地区'], 'values': ['广东']}
- 候选数：120, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `统调核电上网电量` → 统调核电上网电量(MWh) (rank=1, score=0.7703, src=path_a)
  - ✓ `统调水电上网电量` → 统调水电上网电量(MWh) (rank=2, score=0.7567, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=65, score=0.5929, src=path_c)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=53, score=0.6223, src=path_a)
- Top-10 候选：
  - [metric] 统调核电上网电量(MWh) (score=0.7703, src=path_a)
  - [metric] 统调水电上网电量(MWh) (score=0.7567, src=path_a)
  - [table] 发受电量 (score=0.7493, src=path_a)
  - [metric] 统调上网电量(MWh) (score=0.7461, src=path_a)
  - [metric] 核电_统调发电 (score=0.7412, src=path_a)
  - [metric] 统调火电上网电量(MWh) (score=0.7285, src=path_a)
  - [metric] 水电_统调发电 (score=0.7261, src=path_a)
  - [metric] 总计_统调发电 (score=0.7114, src=path_a)
  - [metric] 统调发电量(MWh) (score=0.6993, src=path_a)
  - [metric] 核电_中调发电 (score=0.6968, src=path_a)

### ✅ [14] 2025年3月15日广东地区的水电统调发电和火电统调发电是多少？
- 期望：{'metrics': ['水电_统调发电', '火电合计_统调发电'], 'dimensions': ['地区'], 'values': ['广东']}
- 候选数：129, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `水电_统调发电` → 水电_统调发电 (rank=1, score=0.7744, src=path_a)
  - ✓ `火电合计_统调发电` → 火电合计_统调发电 (rank=7, score=0.7233, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=55, score=0.6253, src=path_c)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=54, score=0.6274, src=path_a)
- Top-10 候选：
  - [metric] 水电_统调发电 (score=0.7744, src=path_a)
  - [table] 发受电量 (score=0.7607, src=path_a)
  - [metric] 燃煤火电_统调发电 (score=0.7449, src=path_a)
  - [metric] 总计_统调发电 (score=0.7413, src=path_a)
  - [metric] 统调发电量(MWh) (score=0.732, src=path_a)
  - [metric] 其他火电_统调发电 (score=0.7297, src=path_a)
  - [metric] 火电合计_统调发电 (score=0.7233, src=path_a)
  - [metric] 统调水电上网电量(MWh) (score=0.7195, src=path_a)
  - [metric] 统调火电上网电量(MWh) (score=0.7161, src=path_a)
  - [metric] 水电_中调发电 (score=0.7132, src=path_a)

### ✅ [15] 2025年6月1日广西地区的峰谷差地调和负荷率地调是多少？
- 期望：{'metrics': ['峰谷差_地调', '负荷率_地调'], 'dimensions': ['地区'], 'values': ['广西']}
- 候选数：121, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `峰谷差_地调` → 峰谷差_地调(MW) (rank=1, score=0.7789, src=path_a)
  - ✓ `负荷率_地调` → 负荷率_地调(%) (rank=5, score=0.6856, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=21, score=0.626, src=path_c)
- 维度值命中：
  - ✓ `广西` → 广西送广东 (rank=7, score=0.6531, src=path_a)
- Top-10 候选：
  - [metric] 峰谷差_地调(MW) (score=0.7789, src=path_a)
  - [metric] 峰谷差_中调(MW) (score=0.7441, src=path_a)
  - [metric] 峰谷差_统调（MW） (score=0.7404, src=path_a)
  - [table] 负荷与备用 (score=0.7333, src=path_a)
  - [metric] 负荷率_地调(%) (score=0.6856, src=path_a)
  - [metric] 平均_地调（MW） (score=0.656, src=path_a)
  - [dim_value] 广西送广东 (score=0.6531, src=path_a)
  - [metric] 负荷率_中调(%) (score=0.6402, src=path_b)
  - [metric] 负荷率_统调(%) (score=0.6402, src=path_b)
  - [metric] 损失负荷(MW)（可为空） (score=0.6402, src=path_b)

### ✅ [16] 2025年7月8日深圳供电局停电的线路名称和停电时间是什么？
- 期望：{'metrics': ['停电时间'], 'dimensions': ['故障所属维护单位', '线路名称'], 'values': ['深圳供电局']}
- 候选数：126, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `停电时间` → 停电时间 (rank=2, score=0.7183, src=path_a)
- 维度命中：
  - ✓ `故障所属维护单位` → 故障所属维护单位 (rank=50, score=0.5617, src=path_a)
  - ✓ `线路名称` → 线路名称 (rank=21, score=0.6154, src=path_a)
- 维度值命中：
  - ✓ `深圳供电局` → 深圳供电局 (rank=3, score=0.6921, src=path_a)
- Top-10 候选：
  - [table] 跳闸情况 (score=0.756, src=path_a)
  - [dimension] 停电时间 (score=0.7183, src=path_a)
  - [dim_value] 深圳供电局 (score=0.6921, src=path_a)
  - [dimension] 停电类型 (score=0.6848, src=path_a)
  - [table] 断面表 (score=0.6805, src=path_a)
  - [metric] 停电影响用户数（可为空） (score=0.6801, src=path_a)
  - [dimension] 停电原因 (score=0.6727, src=path_a)
  - [dimension] 用电恢复情况 (score=0.6582, src=path_a)
  - [dim_value] 跳闸 (score=0.6507, src=path_a)
  - [dim_value] 东莞供电局 (score=0.6462, src=path_a)

### ✅ [17] 3月9日到3月11日，各省的负荷率地调平均值分别是多少
- 期望：{'metrics': ['负荷率_地调'], 'dimensions': ['地区'], 'values': ['云南', '广东', '广西', '海南', '贵州']}
- 候选数：123, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `负荷率_地调` → 负荷率_地调(%) (rank=2, score=0.7441, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=34, score=0.5872, src=path_c)
- 维度值命中：
  - ✓ `云南` → 云南送广东 (rank=53, score=0.548, src=path_a)
  - ✓ `广东` → 云南送广东 (rank=53, score=0.548, src=path_a)
  - ✓ `广西` → 广西送广东 (rank=57, score=0.5364, src=path_a)
  - ✓ `海南` → 广东送海南 (rank=67, score=0.5172, src=path_a)
  - ✓ `贵州` → 贵州送广东 (rank=55, score=0.5411, src=path_a)
- Top-10 候选：
  - [table] 负荷与备用 (score=0.745, src=path_a)
  - [metric] 负荷率_地调(%) (score=0.7441, src=path_a)
  - [metric] 平均_地调（MW） (score=0.7353, src=path_a)
  - [metric] 负荷率_中调(%) (score=0.7003, src=path_a)
  - [metric] 最高_地调（MW） (score=0.6894, src=path_a)
  - [metric] 最低_地调（MW） (score=0.6846, src=path_a)
  - [metric] 负荷率_统调(%) (score=0.6841, src=path_a)
  - [metric] 平均_中调（MW） (score=0.6742, src=path_a)
  - [metric] 平均_统调（MW） (score=0.6739, src=path_a)
  - [metric] 峰谷差_地调(MW) (score=0.6579, src=path_b)

### ✅ [18] 2026年2月每天广东省的统调发电量和统调受电量是多少？
- 期望：{'metrics': ['统调发电量', '统调受电量'], 'dimensions': ['地区'], 'values': ['广东']}
- 候选数：118, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `统调发电量` → 统调发电量(MWh) (rank=2, score=0.7934, src=path_a)
  - ✓ `统调受电量` → 统调受电量(MWh) (rank=3, score=0.7799, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=54, score=0.6453, src=path_c)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=57, score=0.6279, src=path_a)
- Top-10 候选：
  - [table] 发受电量 (score=0.8214, src=path_a)
  - [metric] 统调发电量(MWh) (score=0.7934, src=path_a)
  - [metric] 统调受电量(MWh) (score=0.7799, src=path_a)
  - [metric] 统调发受电量(MWh) (score=0.7749, src=path_a)
  - [metric] 燃煤火电_统调发电 (score=0.7684, src=path_a)
  - [metric] 统调发受电量_中调(MWh) (score=0.7643, src=path_a)
  - [metric] 统调上网电量(MWh) (score=0.7632, src=path_a)
  - [metric] 总计_统调发电 (score=0.7571, src=path_a)
  - [metric] 统调受电量_中调(MWh) (score=0.7553, src=path_a)
  - [metric] 水电_统调发电 (score=0.7492, src=path_a)

### ✅ [19] 2025年6月每天海南省的最低、最高、平均统调负荷是多少？
- 期望：{'metrics': ['最低_统调', '最高_统调', '平均_统调'], 'dimensions': ['地区'], 'values': ['海南']}
- 候选数：121, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `最低_统调` → 最低_统调（MW） (rank=1, score=0.7528, src=path_a)
  - ✓ `最高_统调` → 最高_统调（MW） (rank=3, score=0.7235, src=path_a)
  - ✓ `平均_统调` → 平均_统调（MW） (rank=6, score=0.7007, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=40, score=0.589, src=path_c)
- 维度值命中：
  - ✓ `海南` → 海南送云南 (rank=42, score=0.5871, src=path_a)
- Top-10 候选：
  - [metric] 最低_统调（MW） (score=0.7528, src=path_a)
  - [table] 负荷与备用 (score=0.7271, src=path_a)
  - [metric] 最高_统调（MW） (score=0.7235, src=path_a)
  - [metric] 最低_地调（MW） (score=0.7048, src=path_a)
  - [metric] 含分布式最低_统调（MW） (score=0.7019, src=path_a)
  - [metric] 平均_统调（MW） (score=0.7007, src=path_a)
  - [metric] 最低_中调（MW） (score=0.6958, src=path_a)
  - [metric] 还原后最高_统调（MW） (score=0.677, src=path_a)
  - [metric] 含分布式最高_统调（MW） (score=0.6732, src=path_a)
  - [metric] 最高_地调（MW） (score=0.6716, src=path_a)

### ✅ [20] 2026年2月各供电局每天的停电次数和受影响用户数是多少？
- 期望：{'metrics': ['停电影响用户数（可为空）', '停电时间（计数）'], 'dimensions': ['故障所属维护单位'], 'values': []}
- 候选数：110, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `停电影响用户数（可为空）` → 停电影响用户数（可为空） (rank=1, score=0.7552, src=path_a)
  - ✓ `停电时间（计数）` → 停电时间 (rank=4, score=0.6576, src=path_a)
- 维度命中：
  - ✓ `故障所属维护单位` → 故障所属维护单位 (rank=49, score=0.5555, src=path_d)
- Top-10 候选：
  - [metric] 停电影响用户数（可为空） (score=0.7552, src=path_a)
  - [table] 跳闸情况 (score=0.7441, src=path_a)
  - [metric] 复电用户数（可为空） (score=0.6927, src=path_a)
  - [dimension] 停电时间 (score=0.6576, src=path_a)
  - [derived_metric] 停电次数 (score=0.6536, src=path_d)
  - [table] 送受电量 (score=0.6465, src=path_a)
  - [dimension] 停电类型 (score=0.6403, src=path_a)
  - [dimension] 用电恢复情况 (score=0.6346, src=path_a)
  - [dim_value] 各区供电局 (score=0.6339, src=path_a)
  - [table] 发受电量 (score=0.6335, src=path_a)

### ✅ [21] 2025年各月份广东地区的不同发电类型（水电、火电、核电）的发电量是多少？
- 期望：{'metrics': ['水电_统调发电', '火电合计_统调发电', '核电_统调发电'], 'dimensions': ['地区'], 'values': ['广东']}
- 候选数：113, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `水电_统调发电` → 水电_统调发电 (rank=16, score=0.6688, src=path_a)
  - ✓ `火电合计_统调发电` → 火电合计_统调发电 (rank=20, score=0.6639, src=path_b)
  - ✓ `核电_统调发电` → 核电_统调发电 (rank=12, score=0.6753, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=68, score=0.5795, src=path_c)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=63, score=0.5975, src=path_a)
- Top-10 候选：
  - [table] 发受电量 (score=0.7638, src=path_a)
  - [metric] 总计_统调发电 (score=0.7036, src=path_a)
  - [metric] 燃煤火电_统调发电 (score=0.6936, src=path_a)
  - [table] 新能源信息填报 (score=0.6883, src=path_a)
  - [metric] 燃煤火电_中调发电 (score=0.6876, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.6865, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6846, src=path_a)
  - [dimension] 发电类型 (score=0.6808, src=path_a)
  - [metric] 发电量(MWh) (score=0.6775, src=path_a)
  - [metric] 其他火电_统调发电 (score=0.6771, src=path_a)

### ✅ [22] 2025年1月1号到1月10号云南省平均地调的变化情况？
- 期望：{'metrics': ['平均_地调'], 'dimensions': ['地区'], 'values': ['云南']}
- 候选数：116, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `平均_地调` → 平均_地调（MW） (rank=1, score=0.6476, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=24, score=0.5562, src=path_c)
- 维度值命中：
  - ✓ `云南` → 云南送广东 (rank=2, score=0.6401, src=path_a)
- Top-10 候选：
  - [metric] 平均_地调（MW） (score=0.6476, src=path_a)
  - [dim_value] 云南送广东 (score=0.6401, src=path_a)
  - [table] 负荷与备用 (score=0.6275, src=path_a)
  - [dim_value] 云南送贵州 (score=0.6229, src=path_a)
  - [dim_value] 云南送广西 (score=0.6218, src=path_a)
  - [dim_value] 云南送海南 (score=0.6075, src=path_a)
  - [metric] 负荷率_地调(%) (score=0.6015, src=path_a)
  - [metric] 统调发受电量_中调(MWh) (score=0.5931, src=path_a)
  - [metric] 统调受电量_中调(MWh) (score=0.5904, src=path_a)
  - [metric] 统调受电量(MWh) (score=0.5883, src=path_a)

### ✅ [23] 2025年广东地区统调负荷率的月变化趋势
- 期望：{'metrics': ['负荷率_统调'], 'dimensions': ['地区'], 'values': ['广东']}
- 候选数：121, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `负荷率_统调` → 负荷率_统调(%) (rank=2, score=0.6729, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=34, score=0.5728, src=path_c)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=37, score=0.5611, src=path_a)
- Top-10 候选：
  - [table] 负荷与备用 (score=0.7047, src=path_a)
  - [metric] 负荷率_统调(%) (score=0.6729, src=path_a)
  - [metric] 负荷率_中调(%) (score=0.6494, src=path_a)
  - [metric] 负荷率_地调(%) (score=0.6493, src=path_a)
  - [metric] 平均_统调（MW） (score=0.6369, src=path_a)
  - [metric] 峰谷差_统调（MW） (score=0.6332, src=path_b)
  - [metric] 峰谷差_中调(MW) (score=0.6332, src=path_b)
  - [metric] 峰谷差_地调(MW) (score=0.6332, src=path_b)
  - [metric] 损失负荷(MW)（可为空） (score=0.6332, src=path_b)
  - [metric] 最大出力(MW) (score=0.6332, src=path_b)

### ✅ [24] 2025年1月到6月广东风力发电量的发展趋势
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['地区', '发电类型'], 'values': ['广东', '风能']}
- 候选数：120, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 发电量(MWh) (rank=9, score=0.6276, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=72, score=0.5338, src=path_c)
  - ✓ `发电类型` → 发电类型 (rank=68, score=0.545, src=path_a)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=28, score=0.5947, src=path_a)
  - ✓ `风能` → 风能 (rank=65, score=0.5519, src=path_a)
- Top-10 候选：
  - [metric] 风力发电_中调发电 (score=0.6835, src=path_a)
  - [table] 发受电量 (score=0.6795, src=path_a)
  - [metric] 风力发电_统调发电 (score=0.6781, src=path_a)
  - [table] 新能源信息填报 (score=0.6414, src=path_a)
  - [metric] 统调风力发电上网电量(MWh) (score=0.636, src=path_a)
  - [metric] 实际出力(MW) (score=0.6342, src=path_a)
  - [table] 送受电量 (score=0.6299, src=path_a)
  - [metric] 总计_统调发电 (score=0.6297, src=path_a)
  - [metric] 发电量(MWh) (score=0.6276, src=path_a)
  - [metric] 火电合计_中调发电 (score=0.624, src=path_a)

### ✅ [25] 2025年各月份广东光伏发电量的环比增长情况
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['地区', '发电类型'], 'values': ['广东', '总光伏']}
- 候选数：104, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 新能源发电量(MWh) (rank=8, score=0.5577, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=57, score=0.4584, src=path_c)
  - ✓ `发电类型` → 发电类型 (rank=45, score=0.4872, src=path_a)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=20, score=0.5264, src=path_a)
  - ✓ `总光伏` → 总光伏 (rank=2, score=0.5835, src=path_a)
- Top-10 候选：
  - [table] 发受电量 (score=0.5868, src=path_a)
  - [dim_value] 总光伏 (score=0.5835, src=path_a)
  - [table] 新能源信息填报 (score=0.5786, src=path_a)
  - [table] 送受电量 (score=0.5696, src=path_a)
  - [dim_value] 总分布式光伏 (score=0.5664, src=path_a)
  - [metric] 统调集中式光伏 (score=0.5663, src=path_a)
  - [metric] 太阳能_中调发电 (score=0.5593, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.5577, src=path_a)
  - [metric] 总计含分布式光伏_统调发电 (score=0.5577, src=path_a)
  - [metric] 统调发受电量含分布式光伏(MWh) (score=0.5522, src=path_a)

### ✅ [26] 去年各季度全网统调发电量的变化趋势
- 期望：{'metrics': ['统调发电量'], 'dimensions': ['地区'], 'values': ['广东', '广西', '海南', '云南', '贵州']}
- 候选数：118, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `统调发电量` → 统调发电量(MWh) (rank=1, score=0.7532, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=55, score=0.5757, src=path_c)
- 维度值命中：
  - ✓ `广东` → 云南送广东 (rank=69, score=0.5034, src=path_a)
  - ✓ `广西` → 云南送广西 (rank=75, score=0.4831, src=path_a)
  - ✓ `海南` → 云南送海南 (rank=72, score=0.4876, src=path_a)
  - ✓ `云南` → 云南送广东 (rank=69, score=0.5034, src=path_a)
  - ✓ `贵州` → 贵州送广东 (rank=73, score=0.4872, src=path_a)
- Top-10 候选：
  - [metric] 统调发电量(MWh) (score=0.7532, src=path_a)
  - [metric] 统调火电上网电量(MWh) (score=0.7415, src=path_a)
  - [metric] 燃煤火电_统调发电 (score=0.741, src=path_a)
  - [table] 发受电量 (score=0.7367, src=path_a)
  - [metric] 统调上网电量(MWh) (score=0.7275, src=path_a)
  - [metric] 火电合计_统调发电 (score=0.7172, src=path_a)
  - [metric] 总计_统调发电 (score=0.71, src=path_a)
  - [metric] 核电_统调发电 (score=0.7093, src=path_a)
  - [metric] 其他火电_统调发电 (score=0.7092, src=path_a)
  - [metric] 统调风力发电上网电量(MWh) (score=0.7027, src=path_a)

### ✅ [27] 2025年1月1号全天实际电量最多的是哪两个方向？
- 期望：{'metrics': ['全天实际电量（MWh）'], 'dimensions': ['送受电方向'], 'values': []}
- 候选数：159, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `全天实际电量（MWh）` → 全天实际电量（MWh） (rank=1, score=0.7783, src=path_a)
- 维度命中：
  - ✓ `送受电方向` → 送受电方向 (rank=6, score=0.6848, src=path_a)
- Top-10 候选：
  - [metric] 全天实际电量（MWh） (score=0.7783, src=path_a)
  - [table] 送受电量 (score=0.7219, src=path_a)
  - [metric] 全天计划电量（MWh） (score=0.7168, src=path_a)
  - [metric] 7-23点实际电量（MWh） (score=0.7056, src=path_a)
  - [metric] 23-7点实际电量（MWh） (score=0.6867, src=path_a)
  - [dimension] 送受电方向 (score=0.6848, src=path_a)
  - [metric] 实际值_最大有功功率（MW） (score=0.6797, src=path_a)
  - [table] 新能源运行情况 (score=0.6759, src=path_a)
  - [table] 发受电量 (score=0.6756, src=path_a)
  - [metric] 全电量_中调(MWh) (score=0.6755, src=path_a)

### ✅ [28] 2025年3月跳闸次数最多的前三个供电局是哪些？
- 期望：{'metrics': ['停电时间（计数）'], 'dimensions': ['停电类型', '故障所属维护单位'], 'values': ['跳闸']}
- 候选数：126, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `停电时间（计数）` → 停电时间 (rank=22, score=0.5775, src=path_a)
- 维度命中：
  - ✓ `停电类型` → 停电类型 (rank=10, score=0.6303, src=path_a)
  - ✓ `故障所属维护单位` → 故障所属维护单位 (rank=36, score=0.5484, src=path_a)
- 维度值命中：
  - ✓ `跳闸` → 跳闸 (rank=4, score=0.6596, src=path_a)
- Top-10 候选：
  - [table] 跳闸情况 (score=0.7991, src=path_a)
  - [metric] 复电用户数（可为空） (score=0.7124, src=path_a)
  - [metric] 停电影响用户数（可为空） (score=0.7113, src=path_a)
  - [dim_value] 跳闸 (score=0.6596, src=path_a)
  - [metric] 损失电量(万kWh)（固定为空）(MWh) (score=0.658, src=path_a)
  - [derived_metric] 跳闸次数 (score=0.655, src=path_d)
  - [metric] 损失负荷(MW)（可为空） (score=0.6544, src=path_a)
  - [metric] 已恢复负荷(MW)（可为空） (score=0.6431, src=path_a)
  - [dim_value] 各区供电局 (score=0.6413, src=path_a)
  - [dimension] 停电类型 (score=0.6303, src=path_a)

### ✅ [29] 2025年1月实际出力排名前三的省份有哪些？
- 期望：{'metrics': ['实际出力(MW)'], 'dimensions': ['地区'], 'values': []}
- 候选数：104, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `实际出力(MW)` → 实际出力(MW) (rank=1, score=0.751, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=45, score=0.5531, src=path_c)
- Top-10 候选：
  - [metric] 实际出力(MW) (score=0.751, src=path_a)
  - [metric] 最大出力(MW) (score=0.6909, src=path_a)
  - [table] 发受电量 (score=0.6755, src=path_a)
  - [metric] 最小出力(MW) (score=0.675, src=path_a)
  - [table] 送受电量 (score=0.6705, src=path_a)
  - [metric] 新能源最大出力(MW) (score=0.6652, src=path_c)
  - [table] 新能源信息填报 (score=0.6602, src=path_a)
  - [metric] 最大受限出力(MW) (score=0.6549, src=path_a)
  - [metric] 装机容量(MW) (score=0.6223, src=path_a)
  - [metric] 风力发电_统调发电 (score=0.6219, src=path_a)

### ✅ [30] 2025年3月12日广东地区统调发电量最大的电源类型是什么？
- 期望：{'metrics': ['总计_统调发电'], 'dimensions': ['地区', '发电类型'], 'values': ['广东']}
- 候选数：125, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `总计_统调发电` → 总计_统调发电 (rank=3, score=0.7175, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=69, score=0.5987, src=path_c)
  - ✓ `发电类型` → 发电类型 (rank=10, score=0.6704, src=path_a)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=59, score=0.6265, src=path_a)
- Top-10 候选：
  - [table] 发受电量 (score=0.7584, src=path_a)
  - [metric] 其他_统调发电 (score=0.7292, src=path_a)
  - [metric] 总计_统调发电 (score=0.7175, src=path_a)
  - [metric] 统调发电量(MWh) (score=0.711, src=path_a)
  - [metric] 燃煤火电_统调发电 (score=0.7076, src=path_a)
  - [metric] 其他火电_统调发电 (score=0.6897, src=path_a)
  - [dim_value] 统调光伏 (score=0.6769, src=path_a)
  - [metric] 核电_统调发电 (score=0.6756, src=path_a)
  - [metric] 其他_中调 (score=0.6709, src=path_a)
  - [dimension] 发电类型 (score=0.6704, src=path_a)

### ✅ [31] 2026年停电次数最多的月份是哪个月？
- 期望：{'metrics': ['停电时间（计数）'], 'dimensions': ['停电类型'], 'values': []}
- 候选数：122, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `停电时间（计数）` → 停电时间 (rank=1, score=0.7071, src=path_a)
- 维度命中：
  - ✓ `停电类型` → 停电类型 (rank=5, score=0.6564, src=path_a)
- Top-10 候选：
  - [dimension] 停电时间 (score=0.7071, src=path_a)
  - [table] 跳闸情况 (score=0.6958, src=path_a)
  - [dimension] 停电原因 (score=0.6691, src=path_a)
  - [derived_metric] 停电次数 (score=0.6624, src=path_d)
  - [dimension] 停电类型 (score=0.6564, src=path_a)
  - [metric] 停电影响用户数（可为空） (score=0.6551, src=path_a)
  - [table] 负荷与备用 (score=0.6375, src=path_a)
  - [table] 新能源运行情况 (score=0.6341, src=path_a)
  - [dimension] 用电恢复情况 (score=0.6325, src=path_a)
  - [metric] 复电用户数（可为空） (score=0.6175, src=path_a)

### ✅ [32] 2026年哪个省份的装机容量最大？值是多少？
- 期望：{'metrics': ['装机容量(MW)'], 'dimensions': ['地区'], 'values': []}
- 候选数：105, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `装机容量(MW)` → 装机容量(MW) (rank=1, score=0.669, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=58, score=0.5234, src=path_c)
- Top-10 候选：
  - [metric] 装机容量(MW) (score=0.669, src=path_a)
  - [table] 新能源信息填报 (score=0.6431, src=path_a)
  - [table] 发受电量 (score=0.6151, src=path_a)
  - [table] 送受电量 (score=0.6101, src=path_a)
  - [metric] 最大出力(MW) (score=0.5928, src=path_a)
  - [dim_value] 总光伏 (score=0.5845, src=path_a)
  - [dimension] 发电类型 (score=0.5738, src=path_a)
  - [metric] 新能源最大出力(MW) (score=0.5737, src=path_c)
  - [dim_value] 总分布式光伏 (score=0.5722, src=path_a)
  - [metric] 最大受限出力(MW) (score=0.5721, src=path_a)

### ✅ [33] 全网2月份的新能源发电量环比1月份新增多少？
- 期望：{'metrics': ['新能源发电量'], 'dimensions': ['地区'], 'values': ['广东', '广西', '海南', '云南', '贵州']}
- 候选数：113, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `新能源发电量` → 新能源发电量(MWh) (rank=1, score=0.7634, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=79, score=0.4741, src=path_c)
- 维度值命中：
  - ✓ `广东` → 广东-惠州农光互补电站 (rank=77, score=0.4805, src=path_a)
  - ✓ `广西` → 广西-南宁光伏电站 (rank=76, score=0.4824, src=path_a)
  - ✓ `海南` → 海南-三亚光伏电站 (rank=91, score=0.437, src=path_a)
  - ✓ `云南` → 云南-楚雄光伏电站 (rank=87, score=0.4528, src=path_a)
  - ✓ `贵州` → 贵州-遵义风电 (rank=97, score=0.4313, src=path_a)
- Top-10 候选：
  - [metric] 新能源发电量(MWh) (score=0.7634, src=path_a)
  - [table] 新能源信息填报 (score=0.7348, src=path_a)
  - [table] 发受电量 (score=0.7106, src=path_a)
  - [metric] 发电量(MWh) (score=0.6953, src=path_a)
  - [table] 新能源运行情况 (score=0.6785, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6742, src=path_a)
  - [metric] 装机容量(MW) (score=0.6737, src=path_a)
  - [derived_metric] 新能源发电量 (score=0.6625, src=path_d)
  - [metric] 新能源控制电量(MWh) (score=0.6588, src=path_a)
  - [metric] 总计_统调发电 (score=0.6564, src=path_a)

### ✅ [34] 广东省2026年2月份风能的发电量是多少？环比1月份新增多少
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['地区', '发电类型'], 'values': ['广东', '风能']}
- 候选数：112, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 新能源发电量(MWh) (rank=5, score=0.6792, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=84, score=0.5074, src=path_c)
  - ✓ `发电类型` → 发电类型 (rank=64, score=0.5741, src=path_a)
- 维度值命中：
  - ✓ `广东` → 广东-珠海分散式风电 (rank=11, score=0.6351, src=path_a)
  - ✓ `风能` → 风能 (rank=56, score=0.6231, src=path_a)
- Top-10 候选：
  - [metric] 风力发电_统调发电 (score=0.7284, src=path_a)
  - [metric] 风力发电_中调发电 (score=0.7221, src=path_a)
  - [table] 发受电量 (score=0.7113, src=path_a)
  - [table] 新能源信息填报 (score=0.687, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.6792, src=path_a)
  - [metric] 统调风力发电上网电量(MWh) (score=0.6752, src=path_a)
  - [metric] 发电量(MWh) (score=0.6732, src=path_a)
  - [table] 新能源运行情况 (score=0.6476, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6364, src=path_a)
  - [metric] 总计_统调发电 (score=0.6351, src=path_a)

### ✅ [35] 今年广东省一季度风能的发电量是多少？同比去年一季度新增多少？
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['地区', '发电类型'], 'values': ['广东', '风能']}
- 候选数：113, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 新能源发电量(MWh) (rank=3, score=0.6851, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=80, score=0.5074, src=path_c)
  - ✓ `发电类型` → 发电类型 (rank=61, score=0.5764, src=path_a)
- 维度值命中：
  - ✓ `广东` → 广东-珠海分散式风电 (rank=56, score=0.5982, src=path_a)
  - ✓ `风能` → 风能 (rank=13, score=0.6193, src=path_a)
- Top-10 候选：
  - [metric] 风力发电_统调发电 (score=0.7303, src=path_a)
  - [metric] 风力发电_中调发电 (score=0.7154, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.6851, src=path_a)
  - [table] 发受电量 (score=0.6842, src=path_a)
  - [table] 新能源信息填报 (score=0.6781, src=path_a)
  - [metric] 发电量(MWh) (score=0.672, src=path_a)
  - [metric] 统调风力发电上网电量(MWh) (score=0.6716, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6505, src=path_a)
  - [metric] 装机容量(MW) (score=0.6454, src=path_a)
  - [metric] 实际出力(MW) (score=0.6285, src=path_a)

### ✅ [36] 3月广东省最大统调负荷是多少？环比上个月变化多少
- 期望：{'metrics': ['最高_统调'], 'dimensions': ['地区'], 'values': ['广东']}
- 候选数：144, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `最高_统调` → 最高_统调（MW） (rank=2, score=0.705, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=41, score=0.6074, src=path_c)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=50, score=0.5946, src=path_a)
- Top-10 候选：
  - [table] 负荷与备用 (score=0.7454, src=path_a)
  - [metric] 最高_统调（MW） (score=0.705, src=path_a)
  - [metric] 还原后最高_统调（MW） (score=0.6859, src=path_a)
  - [metric] 含分布式最高_统调（MW） (score=0.684, src=path_a)
  - [metric] 平均_统调（MW） (score=0.6713, src=path_a)
  - [table] 发受电量 (score=0.665, src=path_a)
  - [metric] 负荷率_统调(%) (score=0.6607, src=path_b)
  - [metric] 峰谷差_统调（MW） (score=0.6607, src=path_b)
  - [metric] 峰谷差_中调(MW) (score=0.6607, src=path_b)
  - [metric] 负荷率_地调(%) (score=0.6607, src=path_b)

### ✅ [37] 3月12日全网统调发电量是多少？环比前日变化多少
- 期望：{'metrics': ['统调发电量'], 'dimensions': ['地区'], 'values': ['广东', '广西', '海南', '云南', '贵州']}
- 候选数：119, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `统调发电量` → 统调发电量(MWh) (rank=1, score=0.7721, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=56, score=0.617, src=path_c)
- 维度值命中：
  - ✓ `广东` → 云南送广东 (rank=80, score=0.5419, src=path_a)
  - ✓ `广西` → 云南送广西 (rank=87, score=0.5283, src=path_a)
  - ✓ `海南` → 云南送海南 (rank=84, score=0.5337, src=path_a)
  - ✓ `云南` → 云南送广东 (rank=80, score=0.5419, src=path_a)
  - ✓ `贵州` → 贵州送广东 (rank=86, score=0.5284, src=path_a)
- Top-10 候选：
  - [metric] 统调发电量(MWh) (score=0.7721, src=path_a)
  - [metric] 统调上网电量(MWh) (score=0.7695, src=path_a)
  - [table] 发受电量 (score=0.768, src=path_a)
  - [metric] 燃煤火电_统调发电 (score=0.7661, src=path_a)
  - [metric] 统调火电上网电量(MWh) (score=0.7634, src=path_a)
  - [metric] 总计_统调发电 (score=0.744, src=path_a)
  - [metric] 统调发受电量(MWh) (score=0.7392, src=path_a)
  - [metric] 统调发受电量_中调(MWh) (score=0.7389, src=path_a)
  - [metric] 核电_统调发电 (score=0.7386, src=path_a)
  - [metric] 火电合计_统调发电 (score=0.7379, src=path_a)

### ✅ [38] 3月全网统调发电量是多少？环比上月变化多少
- 期望：{'metrics': ['统调发电量'], 'dimensions': ['地区'], 'values': ['广东', '广西', '海南', '云南', '贵州']}
- 候选数：119, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `统调发电量` → 统调发电量(MWh) (rank=4, score=0.7858, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=59, score=0.6024, src=path_c)
- 维度值命中：
  - ✓ `广东` → 云南送广东 (rank=67, score=0.5479, src=path_a)
  - ✓ `广西` → 云南送广西 (rank=84, score=0.5304, src=path_a)
  - ✓ `海南` → 云南送海南 (rank=85, score=0.5279, src=path_a)
  - ✓ `云南` → 云南送广东 (rank=67, score=0.5479, src=path_a)
  - ✓ `贵州` → 贵州送广东 (rank=81, score=0.5354, src=path_a)
- Top-10 候选：
  - [metric] 统调上网电量(MWh) (score=0.7879, src=path_a)
  - [metric] 统调火电上网电量(MWh) (score=0.786, src=path_a)
  - [metric] 燃煤火电_统调发电 (score=0.7859, src=path_a)
  - [metric] 统调发电量(MWh) (score=0.7858, src=path_a)
  - [table] 发受电量 (score=0.7748, src=path_a)
  - [metric] 总计_统调发电 (score=0.7709, src=path_a)
  - [metric] 火电合计_统调发电 (score=0.7632, src=path_a)
  - [metric] 核电_统调发电 (score=0.7624, src=path_a)
  - [metric] 统调水电上网电量(MWh) (score=0.7552, src=path_a)
  - [metric] 统调核电上网电量(MWh) (score=0.7547, src=path_a)

### ✅ [39] 2026年一季度广东受广西的实际电量是多少？同比增长多少？
- 期望：{'metrics': ['全天实际电量（MWh）'], 'dimensions': ['送受电方向'], 'values': ['广东受广西']}
- 候选数：125, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `全天实际电量（MWh）` → 全天实际电量（MWh） (rank=11, score=0.654, src=path_a)
- 维度命中：
  - ✓ `送受电方向` → 送受电方向 (rank=27, score=0.6141, src=path_a)
- 维度值命中：
  - ✓ `广东受广西` → 广东受广西 (rank=3, score=0.6974, src=path_a)
- Top-10 候选：
  - [table] 送受电量 (score=0.7505, src=path_a)
  - [dim_value] 广西送广东 (score=0.7355, src=path_a)
  - [dim_value] 广东受广西 (score=0.6974, src=path_a)
  - [table] 发受电量 (score=0.6943, src=path_a)
  - [dim_value] 广西受云南 (score=0.6622, src=path_a)
  - [dim_value] 广西送贵州 (score=0.6618, src=path_a)
  - [dim_value] 广东送海南 (score=0.661, src=path_a)
  - [dim_value] 广东受云南 (score=0.6591, src=path_a)
  - [dim_value] 广东受贵州 (score=0.6564, src=path_a)
  - [dim_value] 贵州送广东 (score=0.656, src=path_a)

### ✅ [40] 2026年2月17日停电时间超过1天的线路有哪些？
- 期望：{'metrics': ['停电时间', '复电时间'], 'dimensions': ['线路名称'], 'values': []}
- 候选数：124, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `停电时间` → 停电时间 (rank=2, score=0.7356, src=path_a)
  - ✓ `复电时间` → 复电时间 (rank=11, score=0.6341, src=path_a)
- 维度命中：
  - ✓ `线路名称` → 线路名称 (rank=21, score=0.6034, src=path_a)
- Top-10 候选：
  - [table] 跳闸情况 (score=0.738, src=path_a)
  - [dimension] 停电时间 (score=0.7356, src=path_a)
  - [dimension] 停电类型 (score=0.6921, src=path_a)
  - [metric] 停电影响用户数（可为空） (score=0.6755, src=path_a)
  - [dimension] 停电原因 (score=0.6723, src=path_a)
  - [table] 断面表 (score=0.6656, src=path_a)
  - [dimension] 用电恢复情况 (score=0.6655, src=path_a)
  - [metric] 复电用户数（可为空） (score=0.646, src=path_a)
  - [dim_value] 跳闸 (score=0.6452, src=path_a)
  - [dimension] 送电情况 (score=0.6438, src=path_a)

### ✅ [41] 2025年6月1日负荷率低于80%的地区有哪些？
- 期望：{'metrics': ['负荷率_统调'], 'dimensions': ['地区'], 'values': []}
- 候选数：140, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `负荷率_统调` → 负荷率_统调(%) (rank=4, score=0.6944, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=33, score=0.5823, src=path_a)
- Top-10 候选：
  - [metric] 负荷率_地调(%) (score=0.7492, src=path_a)
  - [table] 负荷与备用 (score=0.7284, src=path_a)
  - [metric] 负荷率_中调(%) (score=0.7119, src=path_a)
  - [metric] 负荷率_统调(%) (score=0.6944, src=path_a)
  - [metric] 负载率 (score=0.6786, src=path_a)
  - [metric] 平均_地调（MW） (score=0.6673, src=path_a)
  - [metric] 最低_地调（MW） (score=0.6667, src=path_a)
  - [metric] 最高_地调（MW） (score=0.6545, src=path_a)
  - [metric] 峰谷差_地调(MW) (score=0.6518, src=path_b)
  - [metric] 峰谷差_中调(MW) (score=0.6518, src=path_b)

### ✅ [42] 2025年新能源渗透率大于99.88%的日期有哪些？
- 期望：{'metrics': ['新能源最大渗透率(%)'], 'dimensions': ['日期'], 'values': []}
- 候选数：97, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `新能源最大渗透率(%)` → 新能源最大渗透率(%) (rank=1, score=0.7719, src=path_a)
- 维度命中：
  - ✓ `日期` → 日期 (rank=37, score=0.5237, src=path_a)
- Top-10 候选：
  - [metric] 新能源最大渗透率(%) (score=0.7719, src=path_a)
  - [table] 新能源运行情况 (score=0.6917, src=path_a)
  - [table] 新能源信息填报 (score=0.6451, src=path_a)
  - [metric] 新能源控制电量(MWh) (score=0.6109, src=path_a)
  - [metric] 装机容量(MW) (score=0.603, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.5999, src=path_a)
  - [metric] 新能源最大出力(MW) (score=0.5902, src=path_a)
  - [dimension] 停电时间 (score=0.5884, src=path_c)
  - [metric] 新能源控制最大电力(MW) (score=0.588, src=path_a)
  - [dimension] 用电恢复情况 (score=0.5876, src=path_c)

### ✅ [43] 2025年4月12日，峰谷差大于1000MW的地区有哪些？
- 期望：{'metrics': ['峰谷差_统调'], 'dimensions': ['地区'], 'values': []}
- 候选数：127, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `峰谷差_统调` → 峰谷差_统调（MW） (rank=2, score=0.7591, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=25, score=0.5929, src=path_c)
- Top-10 候选：
  - [metric] 峰谷差_地调(MW) (score=0.7707, src=path_a)
  - [metric] 峰谷差_统调（MW） (score=0.7591, src=path_a)
  - [metric] 峰谷差_中调(MW) (score=0.7587, src=path_a)
  - [table] 负荷与备用 (score=0.7081, src=path_a)
  - [table] 送受电量 (score=0.6578, src=path_a)
  - [table] 发受电量 (score=0.6528, src=path_a)
  - [metric] 最大出力(MW) (score=0.6263, src=path_c)
  - [metric] 统调上网电量(MWh) (score=0.6141, src=path_a)
  - [metric] 总计_统调发电 (score=0.6126, src=path_a)
  - [metric] 新能源最大出力(MW) (score=0.609, src=path_c)

### ✅ [44] 2026年2月14日12点到18点停电的线路中，属于东莞局的有哪些？
- 期望：{'metrics': ['停电时间'], 'dimensions': ['故障所属维护单位', '线路名称'], 'values': ['东莞供电局']}
- 候选数：126, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `停电时间` → 停电时间 (rank=3, score=0.6998, src=path_a)
- 维度命中：
  - ✓ `故障所属维护单位` → 故障所属维护单位 (rank=47, score=0.5739, src=path_a)
  - ✓ `线路名称` → 线路名称 (rank=19, score=0.6124, src=path_a)
- 维度值命中：
  - ✓ `东莞供电局` → 东莞供电局 (rank=1, score=0.7172, src=path_a)
- Top-10 候选：
  - [dim_value] 东莞供电局 (score=0.7172, src=path_a)
  - [table] 跳闸情况 (score=0.7134, src=path_a)
  - [dimension] 停电时间 (score=0.6998, src=path_a)
  - [dimension] 停电类型 (score=0.6728, src=path_a)
  - [dimension] 停电原因 (score=0.6619, src=path_a)
  - [table] 断面表 (score=0.6571, src=path_a)
  - [dimension] 用电恢复情况 (score=0.6564, src=path_a)
  - [dim_value] 深圳供电局 (score=0.6478, src=path_a)
  - [metric] 停电影响用户数（可为空） (score=0.6476, src=path_a)
  - [dim_value] 广州供电局 (score=0.6403, src=path_a)

### ✅ [45] 2025年1月广东风能发电量的变化趋势？
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['发电类型', '地区'], 'values': ['风能', '广东']}
- 候选数：111, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 发电量(MWh) (rank=5, score=0.6661, src=path_a)
- 维度命中：
  - ✓ `发电类型` → 发电类型 (rank=67, score=0.5576, src=path_a)
  - ✓ `地区` → 调管机构 (rank=89, score=0.4962, src=path_c)
- 维度值命中：
  - ✓ `风能` → 风能 (rank=14, score=0.617, src=path_a)
  - ✓ `广东` → 广东-珠海分散式风电 (rank=58, score=0.5933, src=path_a)
- Top-10 候选：
  - [metric] 风力发电_统调发电 (score=0.7244, src=path_a)
  - [metric] 风力发电_中调发电 (score=0.7179, src=path_a)
  - [table] 发受电量 (score=0.6861, src=path_a)
  - [metric] 统调风力发电上网电量(MWh) (score=0.675, src=path_a)
  - [metric] 发电量(MWh) (score=0.6661, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.6615, src=path_a)
  - [table] 新能源信息填报 (score=0.656, src=path_a)
  - [table] 新能源运行情况 (score=0.6544, src=path_a)
  - [metric] 装机容量(MW) (score=0.632, src=path_a)
  - [metric] 新能源控制电量(MWh) (score=0.6312, src=path_a)

### ✅ [46] 2025年1月广西生物质发电量的变化趋势？
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['发电类型', '地区'], 'values': ['生物质', '广西']}
- 候选数：119, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 新能源发电量(MWh) (rank=3, score=0.6342, src=path_a)
- 维度命中：
  - ✓ `发电类型` → 发电类型 (rank=61, score=0.5582, src=path_a)
  - ✓ `地区` → 调管机构 (rank=78, score=0.4848, src=path_c)
- 维度值命中：
  - ✓ `生物质` → 生物质 (rank=4, score=0.6301, src=path_a)
  - ✓ `广西` → 广西送广东 (rank=19, score=0.5856, src=path_a)
- Top-10 候选：
  - [metric] 生物质_统调发电 (score=0.7068, src=path_a)
  - [table] 发受电量 (score=0.6687, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.6342, src=path_a)
  - [dim_value] 生物质 (score=0.6301, src=path_a)
  - [metric] 发电量(MWh) (score=0.6298, src=path_a)
  - [metric] 总计_统调发电 (score=0.6253, src=path_a)
  - [metric] 总计_中调发电 (score=0.6138, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6126, src=path_a)
  - [metric] 蓄能_中调发电 (score=0.611, src=path_a)
  - [metric] 燃煤火电_中调发电 (score=0.6048, src=path_a)

### ✅ [47] 2025年第二季度，新能源发电量连续三个月增长的省份是哪些？
- 期望：{'metrics': ['新能源发电量'], 'dimensions': ['地区'], 'values': []}
- 候选数：114, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `新能源发电量` → 新能源发电量(MWh) (rank=2, score=0.6993, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=76, score=0.5087, src=path_c)
- Top-10 候选：
  - [table] 新能源信息填报 (score=0.7031, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.6993, src=path_a)
  - [table] 发受电量 (score=0.6811, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6563, src=path_a)
  - [metric] 发电量(MWh) (score=0.6464, src=path_a)
  - [metric] 装机容量(MW) (score=0.6438, src=path_a)
  - [table] 新能源运行情况 (score=0.6397, src=path_a)
  - [metric] 新能源控制电量(MWh) (score=0.6318, src=path_a)
  - [dimension] 发电类型 (score=0.6185, src=path_a)
  - [metric] 总计_统调发电 (score=0.6182, src=path_a)

### ✅ [48] 2026年2月连续四天停电次数增加的供电局有哪些？
- 期望：{'metrics': ['停电时间（计数）'], 'dimensions': ['故障所属维护单位'], 'values': []}
- 候选数：126, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `停电时间（计数）` → 停电时间 (rank=3, score=0.6771, src=path_a)
- 维度命中：
  - ✓ `故障所属维护单位` → 故障所属维护单位 (rank=52, score=0.5576, src=path_d)
- Top-10 候选：
  - [table] 跳闸情况 (score=0.7377, src=path_a)
  - [metric] 停电影响用户数（可为空） (score=0.69, src=path_a)
  - [dimension] 停电时间 (score=0.6771, src=path_a)
  - [dimension] 停电类型 (score=0.6692, src=path_a)
  - [metric] 复电用户数（可为空） (score=0.6618, src=path_a)
  - [derived_metric] 停电次数 (score=0.656, src=path_d)
  - [dimension] 停电原因 (score=0.6477, src=path_a)
  - [dimension] 用电恢复情况 (score=0.6446, src=path_a)
  - [table] 送受电量 (score=0.6418, src=path_a)
  - [table] 断面表 (score=0.6414, src=path_a)

### ✅ [49] 2025年上半年，哪些省份的负荷率连续三个月高于85%？
- 期望：{'metrics': ['负荷率_统调'], 'dimensions': ['地区'], 'values': []}
- 候选数：140, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `负荷率_统调` → 负荷率_统调(%) (rank=4, score=0.6808, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=34, score=0.5275, src=path_c)
- Top-10 候选：
  - [table] 负荷与备用 (score=0.7027, src=path_a)
  - [metric] 负荷率_中调(%) (score=0.6864, src=path_a)
  - [metric] 负荷率_地调(%) (score=0.6858, src=path_a)
  - [metric] 负荷率_统调(%) (score=0.6808, src=path_a)
  - [metric] 负载率 (score=0.638, src=path_a)
  - [metric] 峰谷差_统调（MW） (score=0.6334, src=path_b)
  - [metric] 峰谷差_中调(MW) (score=0.6334, src=path_b)
  - [metric] 峰谷差_地调(MW) (score=0.6334, src=path_b)
  - [metric] 损失负荷(MW)（可为空） (score=0.6334, src=path_b)
  - [metric] 最大出力(MW) (score=0.6334, src=path_b)

### ❌ [50] 2025年6月15日湖南地区新能源发电量占比是多少？
- 期望：{'metrics': ['新能源发电量'], 'dimensions': ['地区'], 'values': ['湖南（注：湖南不在南方电网管辖范围内）']}
- 候选数：112, 指标=1.0 维度=1.0 维度值=0.0
- 指标命中：
  - ✓ `新能源发电量` → 新能源发电量(MWh) (rank=1, score=0.6805, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=67, score=0.5171, src=path_c)
- 维度值命中：
  - ✗ `湖南（注：湖南不在南方电网管辖范围内）`
- Top-10 候选：
  - [metric] 新能源发电量(MWh) (score=0.6805, src=path_a)
  - [table] 发受电量 (score=0.6738, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6619, src=path_a)
  - [table] 新能源信息填报 (score=0.657, src=path_a)
  - [metric] 总计_统调发电 (score=0.6426, src=path_a)
  - [metric] 发电量(MWh) (score=0.6327, src=path_a)
  - [metric] 利用小时数(h) (score=0.6116, src=path_a)
  - [metric] 统调发电量(MWh) (score=0.6115, src=path_a)
  - [dim_value] 总光伏 (score=0.608, src=path_a)
  - [metric] 装机容量(MW) (score=0.606, src=path_a)

### ✅ [51] 2025年1月1号广东风能的最大出力与最小出力相差多少？
- 期望：{'metrics': ['最大出力(MW)', '最小出力(MW)'], 'dimensions': ['地区', '发电类型'], 'values': ['广东', '风能']}
- 候选数：121, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `最大出力(MW)` → 最大出力(MW) (rank=1, score=0.7268, src=path_a)
  - ✓ `最小出力(MW)` → 最小出力(MW) (rank=2, score=0.7264, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=45, score=0.5387, src=path_c)
  - ✓ `发电类型` → 发电类型 (rank=30, score=0.5586, src=path_a)
- 维度值命中：
  - ✓ `广东` → 广西送广东 (rank=29, score=0.5605, src=path_a)
  - ✓ `风能` → 风能 (rank=27, score=0.5724, src=path_a)
- Top-10 候选：
  - [metric] 最大出力(MW) (score=0.7268, src=path_a)
  - [metric] 最小出力(MW) (score=0.7264, src=path_a)
  - [metric] 新能源最大出力(MW) (score=0.7186, src=path_a)
  - [metric] 最大受限出力(MW) (score=0.7033, src=path_a)
  - [metric] 实际出力(MW) (score=0.6996, src=path_a)
  - [table] 新能源运行情况 (score=0.6927, src=path_a)
  - [table] 新能源信息填报 (score=0.674, src=path_a)
  - [metric] 新能源控制最大电力(MW) (score=0.6699, src=path_a)
  - [table] 送受电量 (score=0.6414, src=path_a)
  - [metric] 风力发电_统调发电 (score=0.6294, src=path_c)

### ✅ [52] 2025年1月1号广东风能的发电量占其当月风能发电量的百分比是多少？
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['地区', '发电类型'], 'values': ['广东', '风能']}
- 候选数：110, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 新能源发电量(MWh) (rank=4, score=0.7099, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=77, score=0.5326, src=path_c)
  - ✓ `发电类型` → 发电类型 (rank=33, score=0.6142, src=path_a)
- 维度值命中：
  - ✓ `广东` → 广东-珠海分散式风电 (rank=69, score=0.5634, src=path_a)
  - ✓ `风能` → 风能 (rank=17, score=0.6466, src=path_a)
- Top-10 候选：
  - [metric] 风力发电_统调发电 (score=0.7293, src=path_a)
  - [table] 发受电量 (score=0.7209, src=path_a)
  - [metric] 风力发电_中调发电 (score=0.715, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.7099, src=path_a)
  - [metric] 发电量(MWh) (score=0.6944, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6919, src=path_a)
  - [metric] 统调风力发电上网电量(MWh) (score=0.6867, src=path_a)
  - [table] 新能源信息填报 (score=0.6846, src=path_a)
  - [table] 新能源运行情况 (score=0.6712, src=path_a)
  - [metric] 总计_统调发电 (score=0.6707, src=path_a)

### ✅ [53] 2025年1月6号广西生物质发电量占其当月生物质发电量的百分比是多少？
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['地区', '发电类型'], 'values': ['广西', '生物质']}
- 候选数：119, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 非化石能源发电量(MWh) (rank=3, score=0.6298, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=78, score=0.4759, src=path_c)
  - ✓ `发电类型` → 发电类型 (rank=33, score=0.5536, src=path_a)
- 维度值命中：
  - ✓ `广西` → 广西送广东 (rank=14, score=0.5858, src=path_a)
  - ✓ `生物质` → 生物质 (rank=5, score=0.6241, src=path_a)
- Top-10 候选：
  - [metric] 生物质_统调发电 (score=0.6925, src=path_a)
  - [table] 发受电量 (score=0.6515, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6298, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.6284, src=path_a)
  - [dim_value] 生物质 (score=0.6241, src=path_a)
  - [metric] 发电量(MWh) (score=0.6198, src=path_a)
  - [metric] 总计_统调发电 (score=0.6156, src=path_a)
  - [metric] 总计_中调发电 (score=0.5973, src=path_a)
  - [metric] 蓄能_中调发电 (score=0.5956, src=path_a)
  - [metric] 统调发电量(MWh) (score=0.593, src=path_a)

### ✅ [54] 2025年全年，风电发电量在新能源中的占比是多少？
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['发电类型'], 'values': ['风能', '集中式光伏', '统调光伏', '总分布式光伏', '总光伏', '生物质']}
- 候选数：112, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 新能源发电量(MWh) (rank=1, score=0.713, src=path_a)
- 维度命中：
  - ✓ `发电类型` → 发电类型 (rank=15, score=0.6096, src=path_a)
- 维度值命中：
  - ✓ `风能` → 风能 (rank=12, score=0.629, src=path_a)
  - ✓ `集中式光伏` → 集中式光伏 (rank=72, score=0.5324, src=path_a)
  - ✓ `统调光伏` → 统调光伏 (rank=69, score=0.5376, src=path_a)
  - ✓ `总分布式光伏` → 总分布式光伏 (rank=18, score=0.6019, src=path_a)
  - ✓ `总光伏` → 总光伏 (rank=14, score=0.6105, src=path_a)
  - ✓ `生物质` → 生物质 (rank=73, score=0.5323, src=path_a)
- Top-10 候选：
  - [metric] 新能源发电量(MWh) (score=0.713, src=path_a)
  - [metric] 风力发电_统调发电 (score=0.696, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6832, src=path_a)
  - [metric] 风力发电_中调发电 (score=0.6821, src=path_a)
  - [table] 新能源信息填报 (score=0.6792, src=path_a)
  - [metric] 新能源控制电量(MWh) (score=0.6719, src=path_a)
  - [table] 发受电量 (score=0.6715, src=path_a)
  - [metric] 统调风力发电上网电量(MWh) (score=0.6582, src=path_a)
  - [metric] 装机容量(MW) (score=0.6571, src=path_a)
  - [metric] 发电量(MWh) (score=0.6557, src=path_a)

### ✅ [55] 2025年1月1号新能源控制电量大于9000的电站是哪个？其当天的新能源最大出力是多少？
- 期望：{'metrics': ['新能源控制电量(MWh)', '新能源最大出力(MW)'], 'dimensions': ['名称'], 'values': []}
- 候选数：114, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `新能源控制电量(MWh)` → 新能源控制电量(MWh) (rank=2, score=0.7982, src=path_a)
  - ✓ `新能源最大出力(MW)` → 新能源最大出力(MW) (rank=4, score=0.764, src=path_a)
- 维度命中：
  - ✓ `名称` → 名称 (rank=25, score=0.6463, src=path_a)
- Top-10 候选：
  - [table] 新能源运行情况 (score=0.8339, src=path_a)
  - [metric] 新能源控制电量(MWh) (score=0.7982, src=path_a)
  - [metric] 新能源控制最大电力(MW) (score=0.7946, src=path_a)
  - [metric] 新能源最大出力(MW) (score=0.764, src=path_a)
  - [table] 新能源信息填报 (score=0.7583, src=path_a)
  - [table] 发受电量 (score=0.7402, src=path_a)
  - [metric] 最大出力(MW) (score=0.7284, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.7146, src=path_a)
  - [metric] 装机容量(MW) (score=0.7124, src=path_a)
  - [metric] 最大受限出力(MW) (score=0.7073, src=path_a)

### ✅ [56] 2025年1月实际出力最大的省份的装机容量是多少?
- 期望：{'metrics': ['实际出力(MW)', '装机容量(MW)'], 'dimensions': ['地区'], 'values': []}
- 候选数：154, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `实际出力(MW)` → 实际出力(MW) (rank=1, score=0.7364, src=path_a)
  - ✓ `装机容量(MW)` → 装机容量(MW) (rank=4, score=0.7044, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=87, score=0.5356, src=path_c)
- Top-10 候选：
  - [metric] 实际出力(MW) (score=0.7364, src=path_a)
  - [metric] 最大出力(MW) (score=0.7205, src=path_a)
  - [table] 新能源信息填报 (score=0.7057, src=path_a)
  - [metric] 装机容量(MW) (score=0.7044, src=path_a)
  - [metric] 新能源最大出力(MW) (score=0.6975, src=path_a)
  - [table] 送受电量 (score=0.68, src=path_a)
  - [table] 新能源运行情况 (score=0.6795, src=path_a)
  - [metric] 最大受限出力(MW) (score=0.6745, src=path_a)
  - [metric] 最小出力(MW) (score=0.6579, src=path_a)
  - [metric] 实际值_最大有功功率（MW） (score=0.6306, src=path_a)

### ✅ [57] 2026年装机容量最大的省份的发电量是多少？
- 期望：{'metrics': ['发电量(MWh)', '装机容量(MW)'], 'dimensions': ['地区'], 'values': []}
- 候选数：122, 指标=1.0 维度=1.0 维度值=None
- 指标命中：
  - ✓ `发电量(MWh)` → 非化石能源发电量(MWh) (rank=6, score=0.6507, src=path_a)
  - ✓ `装机容量(MW)` → 装机容量(MW) (rank=3, score=0.676, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=82, score=0.5234, src=path_c)
- Top-10 候选：
  - [table] 发受电量 (score=0.7025, src=path_a)
  - [table] 新能源信息填报 (score=0.676, src=path_a)
  - [metric] 装机容量(MW) (score=0.676, src=path_a)
  - [metric] 燃煤火电_统调发电 (score=0.6565, src=path_a)
  - [metric] 总计_统调发电 (score=0.656, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6507, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.6492, src=path_a)
  - [table] 送受电量 (score=0.6416, src=path_a)
  - [metric] 燃煤火电_中调发电 (score=0.6395, src=path_a)
  - [metric] 统调发电量(MWh) (score=0.6389, src=path_a)

### ✅ [58] 2025年1月12日广东地区各类型新能源发电量，先计算总发电量，再计算各类型占比，然后找出占比超过20%且发电量环比昨日增长的
- 期望：{'metrics': ['发电量(MWh)'], 'dimensions': ['地区', '发电类型'], 'values': ['广东']}
- 候选数：118, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 新能源发电量(MWh) (rank=3, score=0.7498, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=79, score=0.5483, src=path_c)
  - ✓ `发电类型` → 发电类型 (rank=9, score=0.6815, src=path_a)
- 维度值命中：
  - ✓ `广东` → 广东-珠海分散式风电 (rank=68, score=0.5933, src=path_a)
- Top-10 候选：
  - [table] 发受电量 (score=0.7604, src=path_a)
  - [table] 新能源信息填报 (score=0.752, src=path_a)
  - [metric] 新能源发电量(MWh) (score=0.7498, src=path_a)
  - [metric] 发电量(MWh) (score=0.6994, src=path_a)
  - [metric] 总计_统调发电 (score=0.6963, src=path_a)
  - [dim_value] 总光伏 (score=0.6938, src=path_a)
  - [metric] 非化石能源发电量(MWh) (score=0.6935, src=path_a)
  - [dim_value] 总分布式光伏 (score=0.6874, src=path_a)
  - [dimension] 发电类型 (score=0.6815, src=path_a)
  - [table] 新能源运行情况 (score=0.678, src=path_a)

### ✅ [59] 2025年1月12日总光伏发电量最大的地区的装机容量是多少
- 期望：{'metrics': ['发电量(MWh)', '装机容量(MW)'], 'dimensions': ['地区', '发电类型'], 'values': ['总光伏']}
- 候选数：125, 指标=1.0 维度=1.0 维度值=1.0
- 指标命中：
  - ✓ `发电量(MWh)` → 新能源发电量(MWh) (rank=12, score=0.6172, src=path_a)
  - ✓ `装机容量(MW)` → 装机容量(MW) (rank=3, score=0.6741, src=path_a)
- 维度命中：
  - ✓ `地区` → 调管机构 (rank=86, score=0.5229, src=path_c)
  - ✓ `发电类型` → 发电类型 (rank=26, score=0.5864, src=path_a)
- 维度值命中：
  - ✓ `总光伏` → 总光伏 (rank=2, score=0.6871, src=path_a)
- Top-10 候选：
  - [table] 新能源信息填报 (score=0.6953, src=path_a)
  - [dim_value] 总光伏 (score=0.6871, src=path_a)
  - [metric] 装机容量(MW) (score=0.6741, src=path_a)
  - [dim_value] 总分布式光伏 (score=0.6595, src=path_a)
  - [table] 发受电量 (score=0.6554, src=path_a)
  - [dim_value] 统调光伏 (score=0.6369, src=path_a)
  - [metric] 最大出力(MW) (score=0.6312, src=path_a)
  - [metric] 太阳能_中调发电 (score=0.6244, src=path_a)
  - [dim_value] 集中式光伏 (score=0.6221, src=path_a)
  - [metric] 统调集中式光伏 (score=0.6214, src=path_a)
