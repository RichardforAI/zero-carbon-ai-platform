"""Seed data for initial knowledge base population."""
from datetime import datetime, timezone

# Scene tags for filtering
SCENE_TAGS = ["建筑运行", "能源管理", "交通物流", "水资源管理", "废弃物管理", "碳汇管理", "供应链碳管理", "园区综合规划"]

BUILDING_SCENE_TOOLS = [1, 2, 7, 8, 9, 10, 11, 17]  # Tool IDs relevant to building operations

CATEGORIES = [
    {"id": 1, "name": "预测类", "name_en": "Forecasting", "description": "利用历史数据与AI模型预测未来趋势", "icon": "🔮", "color": "#40e495"},
    {"id": 2, "name": "优化类", "name_en": "Optimization", "description": "在多重约束条件下求解最优策略", "icon": "⚡", "color": "#5b9cf5"},
    {"id": 3, "name": "控制类", "name_en": "Control", "description": "基于AI算法实时调节设备运行参数", "icon": "🎛️", "color": "#a78bfa"},
    {"id": 4, "name": "诊断类", "name_en": "Diagnostics", "description": "自动识别异常状态并定位根因", "icon": "🔧", "color": "#f5706a"},
    {"id": 5, "name": "核算类", "name_en": "Accounting", "description": "碳排放的量化、追踪与资产管理", "icon": "📐", "color": "#38bdf8"},
    {"id": 6, "name": "识别类", "name_en": "Recognition", "description": "基于图像/信号的智能识别与分类", "icon": "👁️", "color": "#f5c842"},
    {"id": 7, "name": "调度类", "name_en": "Scheduling", "description": "资源在时空维度的优化配置", "icon": "📅", "color": "#fb923c"},
    {"id": 8, "name": "知识类", "name_en": "Knowledge", "description": "知识检索、分析与智能问答", "icon": "📚", "color": "#4ade80"},
    {"id": 9, "name": "创新类", "name_en": "Innovation", "description": "前沿技术探索与情景模拟", "icon": "🚀", "color": "#e879f9"},
]

TOOLS = [
    # 预测类 (id:1)
    {"id": 1, "name": "电力负荷预测", "category_id": 1, "maturity": 5, "scene_tags": ["建筑运行"], "description": "利用历史用电数据、气象信息、生产计划等进行短期/中期/长期电力负荷预测", "scenario": "当园区需要精准预测电力负荷以支撑购电计划、需量管理和储能调度时使用", "ai_method": "利用深度学习模型学习负荷变化规律与外部因素关联，实现高精度预测并输出置信区间", "tech_path": ["LSTM时序预测", "XGBoost梯度提升", "Transformer时序模型", "Prophet趋势分解", "LightGBM"], "value_props": ["预测精度MAPE<5%", "降低需量电费10-20%", "减少备用容量成本约15%", "提升绿电消纳率12-18%"], "prerequisites": "至少1年历史用电数据（建议15分钟粒度），当地历史气象数据", "operation_phase": "电力/能源管理", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型", "临港特色产业型", "生态高新技术型"], "case_count": 12},
    {"id": 2, "name": "光伏出力预测", "category_id": 1, "maturity": 5, "scene_tags": ["建筑运行"], "description": "结合气象预报和历史发电数据预测分布式光伏出力曲线", "scenario": "当园区配备分布式光伏系统，需要精准预测发电量以优化新能源消纳和储能调度时使用", "ai_method": "利用气象数据（辐照度、温度、云量等）和历史发电数据训练模型预测光伏出力", "tech_path": ["CNN-LSTM混合模型", "XGBoost", "Transformer", "物理+数据驱动融合"], "value_props": ["预测精度MAPE<8%", "提升光伏消纳率15-20%", "优化储能配置"], "prerequisites": "至少6个月光伏发电数据（15分钟粒度），当地辐照度数据", "operation_phase": "电力/能源管理", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型", "临港特色产业型", "生态高新技术型"], "case_count": 8},
    {"id": 3, "name": "风电功率预测", "category_id": 1, "maturity": 4, "scene_tags": ["能源管理"], "description": "基于气象预报和历史发电数据预测风力发电功率", "scenario": "适用于配备风力发电的园区，特别是阳江等海上风电装备制造型园区", "ai_method": "利用NWP数值天气预报和风机SCADA数据训练深度学习预测模型", "tech_path": ["LSTM", "CNN", "物理模型+AI融合", "集成学习"], "value_props": ["预测精度MAPE<10%", "降低弃风率", "优化储能调度"], "prerequisites": "至少1年风机SCADA数据，NWP气象数据", "operation_phase": "电力/能源管理", "applicable_park_types": ["新能源装备制造型", "临港特色产业型"], "case_count": 5},

    # 优化类 (id:2)
    {"id": 4, "name": "储能充放电策略优化", "category_id": 2, "maturity": 4, "scene_tags": ["能源管理"], "description": "根据分时电价、负荷预测和光伏出力动态制定储能系统的充放电策略", "scenario": "当园区配置储能系统，希望利用峰谷电价差套利并提升新能源利用率时使用", "ai_method": "利用强化学习或混合整数规划在电价、负荷、发电等多约束下求解最优充放电计划", "tech_path": ["深度强化学习(DRL)", "混合整数线性规划(MILP)", "模型预测控制(MPC)", "动态规划"], "value_props": ["降低用电成本10-25%", "提升新能源自消纳率15-30%", "延长储能寿命"], "prerequisites": "分时电价数据，储能系统参数，负荷和发电预测数据", "operation_phase": "电力/能源管理", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型", "临港特色产业型", "生态高新技术型"], "case_count": 8},
    {"id": 5, "name": "多能流调度优化", "category_id": 2, "maturity": 3, "scene_tags": ["能源管理", "园区综合规划"], "description": "协调电、冷、热等多种能源的供应与存储，实现园区层面能效最优", "scenario": "适用于具有多种能源形式（冷热电联供、多能互补）的复杂园区", "ai_method": "构建多能流耦合模型，利用AI优化算法求解最优能源调度方案", "tech_path": ["混合整数规划", "多目标优化", "深度强化学习", "随机规划"], "value_props": ["综合能效提升10-20%", "降低能源成本15%", "减少碳排放10-15%"], "prerequisites": "各能源系统的运行参数和负荷数据", "operation_phase": "电力/能源管理", "applicable_park_types": ["先进制造型", "重化工近零碳型", "生态高新技术型"], "case_count": 5},
    {"id": 6, "name": "氢基竖炉工艺AI优化", "category_id": 2, "maturity": 3, "scene_tags": ["园区综合规划"], "description": "利用AI优化氢基直接还原铁工艺参数", "scenario": "适用于湛江东海岛等采用氢基竖炉近零碳技术的钢铁园区", "ai_method": "基于工艺机理和数据驱动混合模型，实时优化还原气配比、温度和压力参数", "tech_path": ["机理+数据混合模型", "贝叶斯优化", "强化学习", "数字孪生"], "value_props": ["降低氢气消耗5-10%", "提升产品品质一致性", "减排50-80%"], "prerequisites": "氢基竖炉工艺参数和运行数据，氢气供应参数", "operation_phase": "工业生产过程", "applicable_park_types": ["重化工近零碳型"], "case_count": 2},

    # 控制类 (id:3)
    {"id": 7, "name": "暖通空调AI节能控制", "category_id": 3, "maturity": 5, "scene_tags": ["建筑运行"], "description": "根据室内外环境参数、人流变化和设备特性优化空调系统运行参数", "scenario": "所有园区建筑的中央空调系统节能优化", "ai_method": "利用模型预测控制(MPC)和深度强化学习实时调节冷冻水温度、冷却塔频率、风机转速等参数", "tech_path": ["模型预测控制(MPC)", "深度强化学习(DRL)", "模糊控制", "PID自整定"], "value_props": ["综合节能15-30%", "冷站SCOP达4.5-6.3", "投资回收期1-2年"], "prerequisites": "BMS系统数据接口，冷站运行参数，室内外温湿度传感器", "operation_phase": "建筑用能优化", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型", "临港特色产业型", "生态高新技术型"], "case_count": 21},
    {"id": 8, "name": "照明智能调控", "category_id": 3, "maturity": 5, "scene_tags": ["建筑运行"], "description": "结合自然光照度、人员分布和使用习惯制定分区分时照明控制策略", "scenario": "适用于园区办公楼、厂房、仓库等空间的照明节能", "ai_method": "利用计算机视觉检测人员分布，结合光照传感器数据实现自适应调光", "tech_path": ["计算机视觉", "时间序列预测", "模糊控制", "IoT传感器网络"], "value_props": ["照明节能40-70%", "延长灯具寿命30%", "提升照明舒适度"], "prerequisites": "智能照明系统，人员感应器/摄像头，光照传感器", "operation_phase": "建筑用能优化", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型", "临港特色产业型", "生态高新技术型"], "case_count": 15},

    # 诊断类 (id:4)
    {"id": 9, "name": "设备能效异常诊断", "category_id": 4, "maturity": 4, "scene_tags": ["建筑运行"], "description": "通过分析设备运行数据识别能效异常、性能衰减和运行偏差", "scenario": "当园区需要自动监测关键设备能效状态并定位异常时使用", "ai_method": "利用历史数据建立设备正常运行基线，通过偏离检测和根因分析算法识别异常", "tech_path": ["孤立森林", "LSTM自编码器", "统计过程控制", "根因分析(RCA)"], "value_props": ["异常定位时间缩短60%", "减少非计划停机30-50%", "延长设备寿命20%"], "prerequisites": "设备运行数据（至少6个月），设备参数和额定性能指标", "operation_phase": "设备运维管理", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型"], "case_count": 10},
    {"id": 10, "name": "设备故障预警与健康管理", "category_id": 4, "maturity": 4, "scene_tags": ["建筑运行"], "description": "基于设备运行趋势和退化模型提前预警关键设备潜在故障", "scenario": "适用于冷机、水泵、风机、压缩机等关键设备的预测性维护", "ai_method": "构建设备健康指数和退化模型，通过时序异常检测提前预警故障风险", "tech_path": ["时序异常检测", "生存分析", "LSTM预测", "振动频谱分析"], "value_props": ["减少非计划停机40-60%", "维护成本降低25%", "备件库存优化30%"], "prerequisites": "设备运行数据（振动、温度、电流等），历史维修记录", "operation_phase": "设备运维管理", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型", "临港特色产业型"], "case_count": 7},

    # 核算类 (id:5)
    {"id": 11, "name": "碳足迹核算", "category_id": 5, "maturity": 3, "scene_tags": ["建筑运行"], "description": "协助园区自动采集活动数据、匹配排放因子，完成碳排放核算与报告", "scenario": "园区需要进行Scope 1/2/3碳排放核算和报告时使用", "ai_method": "AI自动匹配排放因子数据库，智能识别数据异常并修正，自动生成碳核算报告", "tech_path": ["NLP文档解析", "知识图谱", "异常检测", "排放因子自动匹配"], "value_props": ["核算效率提升80%", "核算误差<1.5%", "自动生成合规报告"], "prerequisites": "园区活动数据（能源消耗、生产过程、交通等），排放因子数据库", "operation_phase": "碳核算与交易", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型", "临港特色产业型", "生态高新技术型"], "case_count": 6},
    {"id": 12, "name": "产品碳标签生成", "category_id": 5, "maturity": 3, "scene_tags": ["供应链碳管理"], "description": "为园区企业产品自动生成国际互认的碳标签", "scenario": "园区企业需要为出口产品提供碳足迹认证以应对CBAM等绿色贸易壁垒时使用", "ai_method": "基于LCA方法学和供应链数据，AI辅助计算产品全生命周期碳足迹并生成标准碳标签", "tech_path": ["生命周期评估(LCA)", "供应链数据整合", "排放因子数据库", "报告自动生成"], "value_props": ["碳标签生成效率提升5倍", "支持国际互认标准", "助力企业应对绿色贸易壁垒"], "prerequisites": "产品BOM和工艺数据，供应链碳排放数据", "operation_phase": "供应链碳管理", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型"], "case_count": 3},

    # 识别类 (id:6)
    {"id": 13, "name": "危化品泄漏AI检测", "category_id": 6, "maturity": 4, "scene_tags": ["园区综合规划"], "description": "利用计算机视觉实时监测危化品存储和使用区域的泄漏风险", "scenario": "适用于茂名、湛江等涉及危化品的重化工园区的安全监测", "ai_method": "红外热成像+可见光融合的AI视觉检测，识别气体泄漏和液体泄漏", "tech_path": ["计算机视觉(CV)", "红外图像处理", "目标检测(YOLO)", "异常行为识别"], "value_props": ["泄漏检出率>95%", "响应时间缩短至秒级", "减少安全事故风险"], "prerequisites": "监控摄像头（含红外），危化品存储和使用区域覆盖", "operation_phase": "设备运维管理", "applicable_park_types": ["重化工近零碳型", "新材料型"], "case_count": 4},
    {"id": 14, "name": "植被碳汇遥感评估", "category_id": 6, "maturity": 3, "scene_tags": ["碳汇管理"], "description": "利用卫星遥感和AI技术评估园区植被碳汇量", "scenario": "适用于生态高新技术型园区评估绿化碳汇贡献", "ai_method": "基于多光谱卫星影像的AI地物分类和生物量反演模型", "tech_path": ["遥感影像处理", "深度学习语义分割", "生物量反演模型", "GIS空间分析"], "value_props": ["碳汇评估精度提升30%", "节省人工勘察成本80%", "支持年度碳汇追踪"], "prerequisites": "高分辨率卫星影像数据，园区植被类型资料", "operation_phase": "碳汇管理", "applicable_park_types": ["生态高新技术型", "先进制造型"], "case_count": 3},

    # 调度类 (id:7)
    {"id": 15, "name": "新能源车队智能调度", "category_id": 7, "maturity": 4, "scene_tags": ["交通物流"], "description": "优化园区内新能源车辆（电动叉车、物流车等）的调度和充电计划", "scenario": "适用于有大量新能源物流车辆的园区，提升运输效率并降低碳排放", "ai_method": "基于运筹优化和强化学习的车辆路径规划+充电调度联合优化", "tech_path": ["车辆路径规划(VRP)", "强化学习", "遗传算法", "实时调度优化"], "value_props": ["运输效率提升20%", "充电成本降低15%", "车辆利用率提升25%"], "prerequisites": "车辆GPS和电量数据，物流订单和路线数据", "operation_phase": "交通物流", "applicable_park_types": ["先进制造型", "临港特色产业型", "新能源装备制造型"], "case_count": 6},
    {"id": 16, "name": "岸电智能调度", "category_id": 7, "maturity": 3, "scene_tags": ["交通物流"], "description": "智能调度港口岸电供应，优化船舶靠港期间的电力使用", "scenario": "适用于汕头、汕尾等临港园区，减少船舶靠港期间的燃油消耗", "ai_method": "基于船舶到港预测和电力负荷预测的岸电资源优化调度", "tech_path": ["船舶到港预测", "负荷预测", "资源调度优化", "IoT监控"], "value_props": ["减少港口碳排放30-50%", "岸电利用率提升40%", "降低船舶用能成本"], "prerequisites": "船舶AIS数据，岸电设施参数，港口调度系统数据", "operation_phase": "交通物流", "applicable_park_types": ["临港特色产业型"], "case_count": 2},

    # 知识类 (id:8)
    {"id": 17, "name": "能碳指标智能分析", "category_id": 8, "maturity": 4, "scene_tags": ["建筑运行"], "description": "多维度拆解能耗与碳排数据关联，自动定位高耗区域和减排机会", "scenario": "园区管理者需要系统化了解园区能碳状况和改善方向时使用", "ai_method": "利用统计分析+LLM推理，自动生成多维度能碳分析报告和改善建议", "tech_path": ["多维数据分析", "大语言模型推理", "时间序列分解", "归因分析"], "value_props": ["能碳分析效率提升10倍", "自动生成改善建议", "发现隐性节能机会"], "prerequisites": "园区能耗和碳排放数据（分区域/分设备），历史趋势数据", "operation_phase": "综合规划决策", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型", "临港特色产业型", "生态高新技术型"], "case_count": 5},
    {"id": 18, "name": "政策标准知识问答", "category_id": 8, "maturity": 3, "scene_tags": ["园区综合规划"], "description": "基于零碳园区相关政策、标准、技术规范的智能问答系统", "scenario": "园区管理者和政策制定者需要快速查询零碳园区相关政策和标准时使用", "ai_method": "基于RAG架构和向量检索的领域知识问答", "tech_path": ["RAG检索增强生成", "向量数据库", "大语言模型", "文档解析"], "value_props": ["政策查询效率提升90%", "支持自然语言问答", "知识库实时更新"], "prerequisites": "零碳园区政策文件、标准规范文档库", "operation_phase": "综合规划决策", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型", "临港特色产业型", "生态高新技术型"], "case_count": 2},

    # 创新类 (id:9)
    {"id": 19, "name": "CCUS碳捕集效率AI模拟", "category_id": 9, "maturity": 2, "scene_tags": ["能源管理"], "description": "利用AI模拟和优化碳捕集、利用与封存全流程工艺", "scenario": "适用于湛江等规划CCUS示范工程的园区", "ai_method": "基于物理模拟+AI代理模型的CCUS流程优化", "tech_path": ["计算流体力学(CFD)+AI", "代理模型", "贝叶斯优化", "数字孪生"], "value_props": ["碳捕集能耗降低10-20%", "加速工艺参数优化", "降低试错成本"], "prerequisites": "CCUS工艺设计参数，地质封存数据，运行数据（如有）", "operation_phase": "工业生产过程", "applicable_park_types": ["重化工近零碳型"], "case_count": 1},
    {"id": 20, "name": "零碳路径情景模拟", "category_id": 9, "maturity": 2, "scene_tags": ["园区综合规划"], "description": "为园区多目标优化设计零碳转型路径和技术组合方案", "scenario": "园区规划零碳转型路线图时进行多情景对比分析", "ai_method": "基于系统动力学和多目标优化的零碳路径推演与情景模拟", "tech_path": ["系统动力学", "多目标优化", "蒙特卡洛模拟", "情景分析"], "value_props": ["科学规划零碳路径", "量化各方案减碳效果", "优化投资组合"], "prerequisites": "园区能源和碳排放基线数据，技术经济参数", "operation_phase": "综合规划决策", "applicable_park_types": ["先进制造型", "重化工近零碳型", "新能源装备制造型", "新材料型", "临港特色产业型", "生态高新技术型"], "case_count": 2},
]

PARKS = [
    # === 工业园区-装备制造 (7个) ===
    {"id": 1, "name": "广州南沙大岗先进制造业基地", "city": "广州",
     "park_type": "先进制造型", "park_type_primary": "工业园区", "park_type_secondary": "装备制造",
     "build_type": "园中园", "period": "2026-2030", "industry": "先进制造业",
     "key_directions": ["绿电直供", "能效提升", "智能制造降碳"],
     "energy_profile": "以电力消耗为主，年用电量约8-12亿kWh，重点用能环节为数控加工、焊接、喷涂等制造工艺及厂房空调系统",
     "carbon_structure": "Scope1(直接排放):15% 天然气燃烧+柴油; Scope2(间接排放):75% 外购电力; Scope3:10% 供应链物流",
     "core_challenges": "绿电消纳比例不足30%、制造产线能效与国际先进水平差距15-20%、碳足迹追溯链条不完整",
     "level": "省级"},
    {"id": 3, "name": "佛山高新区狮山产业园", "city": "佛山",
     "park_type": "先进制造型", "park_type_primary": "工业园区", "park_type_secondary": "装备制造",
     "build_type": "园中园", "period": "2026-2030", "industry": "先进制造+绿电+氢能",
     "key_directions": ["绿电直供", "绿色蒸汽", "氢能"],
     "energy_profile": "电+热+蒸汽多能需求，年用电量约10亿kWh，蒸汽用量约50万吨/年，是典型多能流耦合园区",
     "carbon_structure": "Scope1:20% 天然气锅炉+工艺余热; Scope2:65% 外购电力; Scope3:15% 原材料与产品运输",
     "core_challenges": "氢能储运成本高、多能流协同调度缺乏AI支撑、绿色蒸汽供应不稳定、碳资产尚未实现精细化管理",
     "level": "省级"},
    {"id": 6, "name": "惠州惠城高新技术产业开发区", "city": "惠州",
     "park_type": "先进制造型", "park_type_primary": "工业园区", "park_type_secondary": "装备制造",
     "build_type": "园区整体", "period": "2025-2030", "industry": "先进制造业",
     "key_directions": ["绿电直供", "能效提升", "智能制造降碳"],
     "energy_profile": "以电力为主，年用电量约6-8亿kWh，电子制造与精密加工为主要用电大户，空调系统能耗占比约30%",
     "carbon_structure": "Scope1:10% 备用柴油发电机; Scope2:80% 外购电力; Scope3:10% 员工通勤+物流",
     "core_challenges": "能效监测颗粒度不足(仅到产线级)、部分老旧厂房空调系统COP<3.0、缺乏实时碳排放在线监测系统",
     "level": "省级"},
    {"id": 8, "name": "中山翠亨新区产业园区", "city": "中山",
     "park_type": "先进制造型", "park_type_primary": "工业园区", "park_type_secondary": "装备制造",
     "build_type": "园中园", "period": "2026-2030", "industry": "先进制造业",
     "key_directions": ["绿电直供", "能效提升", "智能制造降碳"],
     "energy_profile": "电力主导型，年用电量约5-7亿kWh，以精密仪器与智能制造产线为主要用能单元",
     "carbon_structure": "Scope1:12% 天然气; Scope2:78% 外购电力; Scope3:10% 物流运输",
     "core_challenges": "园区能效对标基准缺失、分布式光伏渗透率仅15%、智能制造降碳效果缺乏量化评估工具",
     "level": "省级"},
    {"id": 9, "name": "江门台山产业园区", "city": "江门",
     "park_type": "先进制造型", "park_type_primary": "工业园区", "park_type_secondary": "装备制造",
     "build_type": "园中园", "period": "2026-2030", "industry": "先进制造业",
     "key_directions": ["绿电直供", "能效提升", "智能制造降碳"],
     "energy_profile": "电力+天然气为主，年用电量约4-6亿kWh，通用设备制造与金属加工为主要产业",
     "carbon_structure": "Scope1:18% 天然气+少量柴油; Scope2:72% 外购电力; Scope3:10% 供应链",
     "core_challenges": "中小企业占比高、能效管理意识不足、缺乏统一的能碳管理平台、碳资产管理能力弱",
     "level": "省级"},
    {"id": 10, "name": "阳江滨海新区（高新区）", "city": "阳江",
     "park_type": "新能源装备制造型", "park_type_primary": "工业园区", "park_type_secondary": "装备制造",
     "build_type": "园中园", "period": "2025-2030", "industry": "海上风电装备+合金材料",
     "key_directions": ["清洁能源装备", "绿色交通", "海上风电"],
     "energy_profile": "电力主导+港口物流能耗，年用电量约7-9亿kWh，风电装备吊装与合金冶炼为高耗能环节",
     "carbon_structure": "Scope1:15% 港口机械柴油; Scope2:70% 外购电力; Scope3:15% 大型装备运输",
     "core_challenges": "海上风电出力波动导致园区微网不稳定、合金冶炼余热回收率<30%、重型装备物流碳排强度高",
     "level": "省级"},
    {"id": 13, "name": "肇庆大旺新能源智能汽车产业城", "city": "肇庆",
     "park_type": "新能源装备制造型", "park_type_primary": "工业园区", "park_type_secondary": "装备制造",
     "build_type": "园中园", "period": "2026-2030", "industry": "新能源智能汽车",
     "key_directions": ["清洁能源装备", "绿色交通", "新能源汽车"],
     "energy_profile": "电力+压缩空气+工艺冷却，年用电量约10-15亿kWh，电池产线与涂装车间为主要耗能环节",
     "carbon_structure": "Scope1:20% 涂装烘干天然气+工艺溶剂; Scope2:70% 外购电力; Scope3:10% 电池原材料",
     "core_challenges": "动力电池生产碳足迹核算标准不统一、涂装工艺VOCs与碳排放双高、园区充电桩负荷冲击大",
     "level": "省级"},

    # === 工业园区-重化工 (2个) ===
    {"id": 11, "name": "湛江经开区（东海岛）", "city": "湛江",
     "park_type": "重化工近零碳型", "park_type_primary": "工业园区", "park_type_secondary": "重化工",
     "build_type": "园中园", "period": "2026-2030", "industry": "钢铁（近零碳）",
     "key_directions": ["氢基冶炼", "CCUS", "近零碳钢铁"],
     "energy_profile": "高能耗重工业，年用电量约50-80亿kWh，煤炭+焦炭为主要一次能源，氢基竖炉为转型方向",
     "carbon_structure": "Scope1:75% 高炉/焦炉煤气+煤炭燃烧; Scope2:15% 外购电力; Scope3:10% 铁矿石/废钢运输",
     "core_challenges": "长流程炼钢碳排强度高达1.8tCO2/t钢、氢基直接还原铁技术成熟度仅3-4级、CCUS全流程成本高(300-500元/tCO2)",
     "level": "省级"},
    {"id": 12, "name": "茂名滨海新区绿色化工和氢能产业园", "city": "茂名",
     "park_type": "重化工近零碳型", "park_type_primary": "工业园区", "park_type_secondary": "重化工",
     "build_type": "园区整体", "period": "2026-2030", "industry": "绿色化工+氢能",
     "key_directions": ["绿氢替代", "CCUS", "绿色化工"],
     "energy_profile": "化工工艺用热+电力并重，年用电量约30-40亿kWh，蒸汽需求量约200万吨/年，裂解炉为主要能耗设备",
     "carbon_structure": "Scope1:65% 裂解炉燃料+工艺排放; Scope2:20% 外购电力; Scope3:15% 原油/石脑油原料",
     "core_challenges": "裂解炉电气化改造难度大、绿氢成本是灰氢2-3倍、化工产品碳标签国际互认待突破、碳捕集溶剂能耗高",
     "level": "省级"},

    # === 工业园区-电子信息 (1个) ===
    {"id": 14, "name": "潮州市新材料产业园", "city": "潮州",
     "park_type": "新材料型", "park_type_primary": "工业园区", "park_type_secondary": "电子信息",
     "build_type": "园中园", "period": "2025-2030", "industry": "新材料",
     "key_directions": ["低碳材料工艺", "循环利用"],
     "energy_profile": "电力主导+高温工艺热，年用电量约5-8亿kWh，电子陶瓷与功能材料烧结工艺为主要用能环节",
     "carbon_structure": "Scope1:25% 窑炉天然气+工艺尾气; Scope2:60% 外购电力; Scope3:15% 原料开采与运输",
     "core_challenges": "高温窑炉能效提升空间大(当前热效率仅40-50%)、低碳材料配方研发周期长、循环利用体系尚未闭环",
     "level": "省级"},

    # === 物流/农业园区-仓储物流中心 (2个) ===
    {"id": 2, "name": "汕头潮阳产业园区", "city": "汕头",
     "park_type": "临港特色产业型", "park_type_primary": "物流/农业园区", "park_type_secondary": "仓储物流中心",
     "build_type": "园中园", "period": "2026-2030", "industry": "粤东临港特色产业",
     "key_directions": ["岸电替代", "港口低碳化"],
     "energy_profile": "港口电力+冷链制冷+物流车辆柴油，年用电量约3-5亿kWh，冷藏集装箱和岸桥为主要用能设备",
     "carbon_structure": "Scope1:40% 港口机械+物流车辆柴油; Scope2:50% 外购电力(含冷藏箱); Scope3:10% 船舶停靠",
     "core_challenges": "靠港船舶岸电使用率不足30%、冷链仓储制冷系统能效低(COP<3.0)、港口新能源车辆替换进度慢",
     "level": "省级"},
    {"id": 7, "name": "汕尾红海湾产业园区", "city": "汕尾",
     "park_type": "临港特色产业型", "park_type_primary": "物流/农业园区", "park_type_secondary": "仓储物流中心",
     "build_type": "园中园", "period": "2026-2030", "industry": "粤东临港产业",
     "key_directions": ["岸电替代", "港口低碳化"],
     "energy_profile": "港口作业+仓储照明+物流车辆，年用电量约2-4亿kWh，码头作业区与保税仓储区为主要用能区域",
     "carbon_structure": "Scope1:35% 港作车辆+小型船舶; Scope2:55% 外购电力; Scope3:10% 靠港船舶",
     "core_challenges": "港口岸电设施覆盖率不足50%、仓储屋顶光伏开发率低、物流路径优化缺少AI调度、潮汐能利用未开发",
     "level": "省级"},

    # === 高新园区-科技园 (3个) ===
    {"id": 4, "name": "河源市高新技术开发区", "city": "河源",
     "park_type": "生态高新技术型", "park_type_primary": "高新园区", "park_type_secondary": "科技园",
     "build_type": "园区整体", "period": "2026-2028", "industry": "生态友好型高新技术",
     "key_directions": ["生态保护", "低碳产业协同"],
     "energy_profile": "以建筑用电为主(办公楼+实验室+小型中试车间)，年用电量约1-3亿kWh，空调系统占能耗40%以上",
     "carbon_structure": "Scope1:5% 实验用气; Scope2:85% 外购电力; Scope3:10% 通勤+IT设备",
     "core_challenges": "实验室能效管理精细化程度低、建筑可再生能源渗透率提升空间大(当前<10%)、碳汇价值尚未量化开发",
     "level": "省级"},
    {"id": 5, "name": "梅州融湾产业园区", "city": "梅州",
     "park_type": "生态高新技术型", "park_type_primary": "高新园区", "park_type_secondary": "科技园",
     "build_type": "园中园", "period": "2025-2030", "industry": "北部生态发展区产业",
     "key_directions": ["生态保护", "低碳产业协同"],
     "energy_profile": "建筑用电+轻型制造用电，年用电量约1-2亿kWh，空调+照明+IT设备为主要负荷",
     "carbon_structure": "Scope1:5% 备用发电机; Scope2:85% 外购电力; Scope3:10% 交通通勤",
     "core_challenges": "园区碳汇资源丰富但缺乏AI量化评估工具、低碳产业筛选缺少数据驱动决策支持、零碳建筑标准落地缓慢",
     "level": "省级"},
    {"id": 15, "name": "云浮新兴产业园区", "city": "云浮",
     "park_type": "生态高新技术型", "park_type_primary": "高新园区", "park_type_secondary": "科技园",
     "build_type": "园区整体", "period": "2026-2030", "industry": "新兴产业",
     "key_directions": ["生态保护", "低碳产业协同"],
     "energy_profile": "以办公楼宇+数据中心+研发实验室用电为主，年用电量约1.5-2.5亿kWh，PUE值偏高(>1.6)",
     "carbon_structure": "Scope1:3% 实验用气+备用电源; Scope2:87% 外购电力; Scope3:10% IT设备供应链",
     "core_challenges": "数据中心PUE优化空间大、建筑光伏一体化推进缓慢、生态碳汇资产尚未纳入园区碳管理、缺乏智慧能源管理系统",
     "level": "省级"},

    # === 公建园区-政务中心 (1个) ===
    {"id": 16, "name": "广州市政务服务中心零碳改造示范", "city": "广州",
     "park_type": "生态高新技术型", "park_type_primary": "公建园区", "park_type_secondary": "政务中心",
     "build_type": "单栋建筑群", "period": "2026-2028", "industry": "公共政务服务",
     "key_directions": ["建筑节能改造", "光伏建筑一体化", "智慧用能管理"],
     "energy_profile": "以建筑用电为主(空调+照明+办公设备)，年用电量约800-1200万kWh，空调系统能耗占比超45%",
     "carbon_structure": "Scope1:5% 备用发电机; Scope2:85% 外购电力; Scope3:10% 员工通勤+纸张消耗",
     "core_challenges": "建筑年代较早(B级能效)、空调系统COP仅2.8、屋顶光伏开发率不足20%、用能行为管理粗放",
     "level": "省级"},

    # === 公建园区-商务楼宇 (1个) ===
    {"id": 17, "name": "深圳福田CBD零碳楼宇示范区", "city": "深圳",
     "park_type": "生态高新技术型", "park_type_primary": "公建园区", "park_type_secondary": "商务楼宇",
     "build_type": "多栋楼宇群", "period": "2026-2029", "industry": "商务办公+商业服务",
     "key_directions": ["超低能耗建筑", "绿电直供", "碳普惠机制"],
     "energy_profile": "高层办公+商业综合体用电为主导，年用电量约3000-5000万kWh，空调+照明+IT设备为三大耗能主体",
     "carbon_structure": "Scope1:3% 燃气锅炉供暖; Scope2:90% 外购电力; Scope3:7% 员工通勤+IT设备供应链",
     "core_challenges": "超高层建筑幕墙能效改造难度大、租户用能行为分散难以统一管理、商业区峰谷负荷差超过60%、碳普惠机制缺乏量化工具支撑",
     "level": "省级"},

    # === 公建园区-医院 (1个) ===
    {"id": 18, "name": "广州国际健康中心零碳医院示范", "city": "广州",
     "park_type": "生态高新技术型", "park_type_primary": "公建园区", "park_type_secondary": "医院",
     "build_type": "园区整体", "period": "2026-2030", "industry": "医疗卫生健康",
     "key_directions": ["高效用能系统", "医疗废弃物低碳处理", "智慧能源管理"],
     "energy_profile": "24h不间断运行型用能，年用电量约2000-3500万kWh，空调净化+医疗设备+热水蒸汽为三大耗能环节",
     "carbon_structure": "Scope1:15% 天然气锅炉蒸汽+消毒; Scope2:80% 外购电力; Scope3:5% 医疗废弃物处理+救护车",
     "core_challenges": "洁净空调24h运行能耗极高、医用气体系统能效低、蒸汽消毒碳排放强度大、医疗废弃物焚烧产生额外碳排放",
     "level": "省级"},

    # === 公建园区-学校 (1个) ===
    {"id": 19, "name": "珠海大学城零碳校园示范区", "city": "珠海",
     "park_type": "生态高新技术型", "park_type_primary": "公建园区", "park_type_secondary": "学校",
     "build_type": "多校区联合", "period": "2026-2030", "industry": "高等教育+科研",
     "key_directions": ["绿色校园", "分布式光伏", "智慧照明与空调"],
     "energy_profile": "教学楼+宿舍+实验室+图书馆多元用电，年用电量约1500-2500万kWh，寒暑假负荷波动大(假期仅为峰值40%)",
     "carbon_structure": "Scope1:8% 食堂天然气+实验室用气; Scope2:82% 外购电力; Scope3:10% 师生通勤+教材纸张",
     "core_challenges": "寒暑假能源系统空转浪费严重、实验室通风橱24h运行能耗高、老旧建筑围护结构能效差、师生节能意识有待提升",
     "level": "省级"},

    # === 物流/农业园区-现代农业产业园 (1个) ===
    {"id": 20, "name": "湛江现代农业智慧零碳产业园", "city": "湛江",
     "park_type": "临港特色产业型", "park_type_primary": "物流/农业园区", "park_type_secondary": "现代农业产业园",
     "build_type": "园区整体", "period": "2026-2030", "industry": "现代农业+农产品加工",
     "key_directions": ["农业碳汇开发", "智慧能源农业", "农产品低碳冷链"],
     "energy_profile": "农业生产+冷链仓储+加工车间综合用电，年用电量约2000-4000万kWh，灌溉+冷链+设施农业为三大耗能环节",
     "carbon_structure": "Scope1:20% 农机柴油+温室锅炉; Scope2:65% 外购电力; Scope3:15% 肥料施用+冷链运输",
     "core_challenges": "农田碳汇方法学缺乏标准化、冷链制冷能效低(COP<2.5)、光伏农业大棚渗透率不足10%、灌溉系统电力浪费严重",
     "level": "省级"},

    # === 工业园区-电子信息 (1个) ===
    {"id": 21, "name": "东莞松山湖电子信息零碳产业园", "city": "东莞",
     "park_type": "先进制造型", "park_type_primary": "工业园区", "park_type_secondary": "电子信息",
     "build_type": "园中园", "period": "2026-2030", "industry": "电子信息+半导体",
     "key_directions": ["绿电直供", "智能制造降碳", "半导体工艺节能"],
     "energy_profile": "电子洁净车间+半导体产线为主要用能单元，年用电量约12-20亿kWh，洁净空调+超纯水系统+工艺设备为三大耗电环节",
     "carbon_structure": "Scope1:10% 工艺气体+特种化学品; Scope2:75% 外购电力; Scope3:15% 电子化学品+晶圆运输",
     "core_challenges": "洁净车间温湿度控制精度导致空调能耗极高(占40%+)、超纯水制备电耗大、半导体工艺碳足迹追溯复杂、园区RE100达标压力大",
     "level": "省级"},
]

CASES = [
    {"id": 1, "tool_id": 1, "park_id": None, "platform_name": "远景方舟AI能碳管理平台", "summary": "在沧州沧东经开区部署AI能碳管理平台", "effect": "负荷预测精度>95%，日级MAPE<3%", "source_url": ""},
    {"id": 2, "tool_id": 1, "park_id": None, "platform_name": "研华iEMS.AI Agent", "summary": "在某电子工厂部署短期负荷预测", "effect": "短期负荷预测误差<3%，支持需量预警", "source_url": ""},
    {"id": 3, "tool_id": 7, "park_id": None, "platform_name": "达实智能AIoT V7.1", "summary": "在深圳某园区部署AI节能控制", "effect": "建筑能耗降低>25%", "source_url": ""},
    {"id": 4, "tool_id": 4, "park_id": None, "platform_name": "朗新科技九功AI能源大模型", "summary": "在新疆甘泉堡经开区部署多能流协同", "effect": "能效提升20%，碳排放下降15%", "source_url": ""},
    {"id": 5, "tool_id": 4, "park_id": None, "platform_name": "江西电建智信能碳AI平台", "summary": "在江西零碳园区部署智能调度", "effect": "以电算碳算法，数据采集成本降90%", "source_url": ""},
    {"id": 6, "tool_id": 15, "park_id": None, "platform_name": "浪潮零碳智慧物流园区", "summary": "在苏州玄通物流园部署智慧物流系统", "effect": "L4级无人配送，5G零碳智慧园区", "source_url": ""},
    {"id": 7, "tool_id": 11, "park_id": None, "platform_name": "普洛斯ASP ESG系统", "summary": "在全国300+园区部署ESG数据管理", "effect": "AI+IoT集成，管理超25万条ESG数据", "source_url": ""},
    {"id": 8, "tool_id": 7, "park_id": None, "platform_name": "双良智慧能碳管理平台", "summary": "在多地化工园区部署能碳管理", "effect": "五大能力中心，AI算法矩阵，获红点设计奖", "source_url": ""},
    {"id": 9, "tool_id": 2, "park_id": None, "platform_name": "天合光能TrinaPro智慧能源平台", "summary": "在江苏常州工业园区部署分布式光伏AI运维系统", "effect": "光伏预测精度MAPE<6%，提升消纳率18%，年度运维成本降低25%", "source_url": ""},
    {"id": 10, "tool_id": 4, "park_id": None, "platform_name": "宁德时代EnerSmart储能云平台", "summary": "在福建宁德锂电新能源园区部署智能储能调度", "effect": "峰谷套利收益提升35%，电池循环寿命延长20%，年节约电费超2000万元", "source_url": ""},
    {"id": 11, "tool_id": 8, "park_id": None, "platform_name": "昕诺飞Interact智能照明系统", "summary": "在深圳前海自贸区办公楼群部署IoT智能照明", "effect": "照明能耗降低65%，员工满意度提升28%，灯具寿命延长至8万小时", "source_url": ""},
    {"id": 12, "tool_id": 9, "park_id": None, "platform_name": "ABB Ability能效诊断平台", "summary": "在广州某汽车制造园区部署设备能效异常诊断系统", "effect": "发现隐性能效问题23处，年度节能收益超500万元，异常定位时间缩短70%", "source_url": ""},
    {"id": 13, "tool_id": 5, "park_id": None, "platform_name": "中控技术i-Energy多能流平台", "summary": "在宁波石化经开区部署冷热电多能流协同优化", "effect": "综合能效提升18%，蒸汽成本降低12%，年减碳约3.5万吨", "source_url": ""},
    {"id": 14, "tool_id": 13, "park_id": None, "platform_name": "海康威视危化品AI检测方案", "summary": "在南京江北新材料科技园部署AI泄漏检测系统", "effect": "泄漏检出率达97%，安全事件响应时间<3秒，获应急管理部示范项目", "source_url": ""},
    {"id": 15, "tool_id": 12, "park_id": None, "platform_name": "碳阻迹Carbonstop碳标签平台", "summary": "为美的集团家电产品提供碳足迹核算与碳标签认证", "effect": "完成30+品类碳标签认证，助产品出口欧盟合规，核算效率提升80%", "source_url": ""},
]

UPDATE_LOGS = [
    {"id": 1, "tool_id": 19, "version": "1.0", "change_type": "new", "description": "新增工具：CCUS碳捕集效率AI模拟工具 — 适用重化工近零碳型园区", "created_at": datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)},
    {"id": 2, "tool_id": 2, "version": "2.3", "change_type": "update", "description": "工具更新：光伏出力预测工具 v2.3 — 新增Transformer模型支持", "created_at": datetime(2026, 7, 14, 14, 0, tzinfo=timezone.utc)},
    {"id": 3, "tool_id": 14, "version": "1.0", "change_type": "new", "description": "新增工具：园区碳汇AI遥感测算工具 — 适用生态高新技术型园区", "created_at": datetime(2026, 7, 13, 10, 0, tzinfo=timezone.utc)},
    {"id": 4, "tool_id": None, "version": None, "change_type": "case_added", "description": "案例新增：朗新科技AI水务管理系统在甘泉堡经开区上线", "created_at": datetime(2026, 7, 12, 8, 0, tzinfo=timezone.utc)},
    {"id": 5, "tool_id": 16, "version": "1.0", "change_type": "new", "description": "新增工具：港口岸电AI智能调度工具 — 适用临港特色产业型园区", "created_at": datetime(2026, 7, 10, 16, 0, tzinfo=timezone.utc)},
    {"id": 6, "tool_id": None, "version": None, "change_type": "data_update", "description": "平台更新：补齐12个AI工具供应商与专家资源（+24家），实现20个工具100%供应商覆盖", "created_at": datetime(2026, 7, 27, 10, 0, tzinfo=timezone.utc)},
    {"id": 7, "tool_id": None, "version": None, "change_type": "data_update", "description": "平台更新：新增6个园区（公建园区4个+现代农业1个+电子信息1个），实现4大类9小类全覆盖", "created_at": datetime(2026, 8, 1, 9, 0, tzinfo=timezone.utc)},
    {"id": 8, "tool_id": None, "version": None, "change_type": "data_update", "description": "数据更新：新增7个商业案例（光伏预测/储能/照明/能效诊断/多能流/危化品检测/碳标签）", "created_at": datetime(2026, 8, 2, 10, 0, tzinfo=timezone.utc)},
    {"id": 9, "tool_id": None, "version": None, "change_type": "policy_update", "description": "政策更新：新增6条2026年7-8月最新政策（碳市场扩围、零碳园区国标、碳足迹管理体系、CBAM首年、广东碳交易修订、第二批园区申报）", "created_at": datetime(2026, 8, 3, 8, 0, tzinfo=timezone.utc)},
    {"id": 10, "tool_id": None, "version": None, "change_type": "feature", "description": "功能上线：零碳白皮书一键导出PDF功能（html2pdf.js客户端生成A4标准文档）", "created_at": datetime(2026, 8, 3, 10, 0, tzinfo=timezone.utc)},
]

POLICIES = [
    # === 国际政策 ===
    {"id": 1, "title": "EU ETS 第四阶段（2021-2030）碳排放配额改革方案", "issuing_body": "欧盟委员会", "publish_date": "2023-06",
     "category": "国际", "topic": "碳市场", "summary": "欧盟碳排放交易体系(EU ETS)进入第四阶段，加速减排步伐，年线性减排因子从2.2%提升至4.3%，逐步取消免费配额，并扩展至海运等行业。",
     "source_name": "欧盟EU ETS官网", "source_url": "https://climate.ec.europa.eu/eu-action/carbon-markets/about-eu-ets_en",
     "tags": ["欧盟", "碳市场", "ETS", "配额"]},

    {"id": 2, "title": "欧盟碳边境调节机制（CBAM）正式实施", "issuing_body": "欧盟委员会", "publish_date": "2023-10",
     "category": "国际", "topic": "碳关税", "summary": "CBAM过渡期（2023-2025）要求进口商按季度报告产品隐含碳排放。2026年起正式征收碳关税，覆盖钢铁、铝、水泥、化肥、电力和氢六大行业。",
     "source_name": "欧盟CBAM官网", "source_url": "https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry-and-reporting_en",
     "tags": ["欧盟", "碳关税", "CBAM", "碳边境调节"]},

    {"id": 3, "title": "IMO 2023年船舶温室气体减排战略", "issuing_body": "国际海事组织(IMO)", "publish_date": "2023-07",
     "category": "国际", "topic": "绿色航运", "summary": "IMO通过修订版减排战略：到2050年实现国际航运净零排放，设定2030年和2040年中期减排目标，推动零碳燃料和技术应用。",
     "source_name": "IMO官网", "source_url": "https://www.imo.org/en/OurWork/Environment/Pages/2023-IMO-Strategy-on-Reduction-of-GHG-Emissions-from-Ships.aspx",
     "tags": ["IMO", "航运减排", "净零排放", "绿色航运"]},

    {"id": 4, "title": "IMO低碳和零碳航运未来燃料与技术项目", "issuing_body": "国际海事组织(IMO)", "publish_date": "2024-03",
     "category": "国际", "topic": "绿色航运", "summary": "IMO启动多项航运脱碳合作项目（GreenVoyage2050、NextGEN、FIN-SMART），推动全球航运业低碳和零碳燃料技术研发与应用示范。",
     "source_name": "IMO Future Fuels项目", "source_url": "https://futurefuels.imo.org/",
     "tags": ["IMO", "零碳燃料", "航运脱碳", "绿色走廊"]},

    # === 国家政策 ===
    {"id": 5, "title": "关于开展零碳园区建设的通知（发改环资〔2025〕910号）", "issuing_body": "国家发改委、工信部、国家能源局", "publish_date": "2025-06-30",
     "category": "国家", "topic": "零碳园区",
     "summary": "三部门联合印发零碳园区建设通知，明确零碳园区定义、建设原则、重点任务和保障措施。要求到2030年建成一批具有示范引领作用的零碳园区，推动园区能源结构优化和产业低碳转型。",
     "source_name": "中国政府网", "source_url": "https://www.gov.cn/zhengce/zhengceku/202507/content_7031090.htm",
     "tags": ["零碳园区", "发改委", "双碳", "园区建设"]},

    {"id": 6, "title": "关于开展零碳工厂建设工作的指导意见（工信部联节〔2026〕13号）", "issuing_body": "工信部、国家发改委、生态环境部、国资委、国家能源局", "publish_date": "2026-01-19",
     "category": "国家", "topic": "零碳园区",
     "summary": "五部门联合发布零碳工厂建设指导意见，明确零碳工厂评价标准、建设路径和激励措施，将零碳工厂建设纳入绿色制造体系，推动制造业领域率先实现碳达峰碳中和。",
     "source_name": "中国政府网", "source_url": "https://big5.www.gov.cn/gate/big5/www.gov.cn/lianbo/202601/content_7055270.htm",
     "tags": ["零碳工厂", "工信部", "绿色制造", "碳达峰"]},

    {"id": 7, "title": "关于做好2026年全国碳排放权交易市场有关工作的通知", "issuing_body": "生态环境部", "publish_date": "2026-02-09",
     "category": "国家", "topic": "碳市场",
     "summary": "部署2026年全国碳市场重点工作：扩大行业覆盖范围（新增水泥、电解铝）、完善配额分配方案、强化数据质量管理、推进CCER重启交易，推动碳市场健康有序发展。",
     "source_name": "生态环境部", "source_url": "https://big5.mee.gov.cn/gate/big5/www.mee.gov.cn/xxgk2018/xxgk/xxgk06/202602/t20260209_1143900.html",
     "tags": ["碳市场", "生态环境部", "碳排放权交易", "配额"]},

    {"id": 8, "title": "关于碳排放权交易收费有关问题的通知（发改价格〔2026〕667号）", "issuing_body": "国家发改委、生态环境部", "publish_date": "2026-05-18",
     "category": "国家", "topic": "碳市场",
     "summary": "明确碳排放权交易收费标准、征收方式和使用管理，规范碳市场交易成本，保障全国碳排放权交易市场平稳运行，促进碳市场长期健康发展。",
     "source_name": "全国碳市场信息网", "source_url": "https://www.cets.org.cn/tzgg/7376.jhtml",
     "tags": ["碳市场", "碳排放权", "收费", "交易"]},

    {"id": 9, "title": "关于更新《企业温室气体排放核算与报告指南 发电设施》有关技术要求的通知", "issuing_body": "生态环境部", "publish_date": "2026-06-30",
     "category": "国家", "topic": "碳核算",
     "summary": "更新发电企业温室气体排放核算方法学和核查技术要求，细化排放因子取值、数据质量控制、第三方核查等关键环节规范，提升碳市场数据质量。",
     "source_name": "全国碳市场信息网", "source_url": "https://www.cets.org.cn/tzgg/7390.jhtml",
     "tags": ["碳核算", "发电设施", "排放因子", "MRV"]},

    {"id": 10, "title": "关于开展重点排放单位第三批次配额结转相关工作的通知", "issuing_body": "生态环境部", "publish_date": "2026-06-02",
     "category": "国家", "topic": "碳市场",
     "summary": "组织开展第三批次碳排放配额结转工作，明确结转条件、操作流程和时间节点，保障碳市场配额管理的连续性和稳定性。",
     "source_name": "全国碳市场信息网", "source_url": "https://www.cets.org.cn/tzgg/7386.jhtml",
     "tags": ["碳市场", "配额结转", "重点排放单位"]},

    # === 地方政策 ===
    {"id": 11, "title": "广东省零碳园区建设名单（第一批）（粤发改资环函〔2026〕435号）", "issuing_body": "广东省发改委、省工信厅、省生态环境厅、省能源局", "publish_date": "2026-03-23",
     "category": "地方", "topic": "零碳园区",
     "summary": "广东省四部门联合印发首批15个省级零碳园区名单，覆盖14个地级市和六大产业类型。要求各地市制定实施方案，明确时间表和路线图，推动零碳园区高标准建设。",
     "source_name": "广东省发改委", "source_url": "https://drc.gd.gov.cn",
     "tags": ["广东省", "零碳园区", "首批名单", "试点"]},

    {"id": 12, "title": "广东省碳达峰实施方案", "issuing_body": "广东省人民政府", "publish_date": "2023-02",
     "category": "地方", "topic": "能源转型",
     "summary": "广东发布碳达峰实施方案，提出能源绿色低碳转型、节能降碳增效、工业领域碳达峰等十大行动，明确到2030年非化石能源消费比重达35%左右。",
     "source_name": "广东省人民政府", "source_url": "https://www.gd.gov.cn",
     "tags": ["广东省", "碳达峰", "能源转型", "实施方案"]},

    {"id": 13, "title": "深圳市碳交易管理办法", "issuing_body": "深圳市人民政府", "publish_date": "2024-06",
     "category": "地方", "topic": "碳市场",
     "summary": "深圳率先开展地方碳交易试点，明确碳排放管控单位范围、配额分配方法、MRV机制及碳金融创新，为全国碳市场建设提供先行经验。",
     "source_name": "深圳市人民政府", "source_url": "https://www.sz.gov.cn",
     "tags": ["深圳", "碳交易", "试点", "碳金融"]},

    # === 行业标准 ===
    {"id": 14, "title": "零碳园区评价标准（T/CECS 1000-2025）", "issuing_body": "中国工程建设标准化协会", "publish_date": "2025-09",
     "category": "行业标准", "topic": "零碳园区",
     "summary": "发布零碳园区评价团体标准，涵盖碳排放核算边界、零碳等级划分、评价指标体系（含能源、建筑、交通、产业四大维度），为零碳园区创建和评价提供技术依据。",
     "source_name": "中国工程建设标准化协会", "source_url": "https://www.cecs.org.cn",
     "tags": ["评价标准", "零碳园区", "团体标准", "指标体系"]},

    {"id": 15, "title": "工业园区碳排放核算指南（试行）", "issuing_body": "中国标准化研究院", "publish_date": "2024-12",
     "category": "行业标准", "topic": "碳核算",
     "summary": "发布工业园区层面碳排放核算方法指南，明确Scope 1/2/3核算边界、排放因子选取原则、数据质量分级方法，为园区碳管理提供标准化工具。",
     "source_name": "中国标准化研究院", "source_url": "https://www.cnis.ac.cn",
     "tags": ["碳核算", "工业园区", "标准化", "Scope3"]},

    {"id": 16, "title": "绿色工厂评价通则（GB/T 36132-2025修订版）", "issuing_body": "国家标准化管理委员会", "publish_date": "2025-03",
     "category": "行业标准", "topic": "零碳园区",
     "summary": "修订绿色工厂评价国家标准，新增碳排放强度、可再生能源使用比例、数字化能碳管理等评价指标，与零碳工厂建设指导意见衔接。",
     "source_name": "国家标准化管理委员会", "source_url": "https://www.sac.gov.cn",
     "tags": ["绿色工厂", "国家标准", "评价", "碳排放"]},

    {"id": 17, "title": "企业ESG信息披露指南（试行）", "issuing_body": "中国证监会、生态环境部", "publish_date": "2025-05",
     "category": "行业标准", "topic": "碳核算",
     "summary": "规范上市公司ESG信息披露要求，明确碳排放信息、气候风险、环境绩效等强制与自愿披露内容，推动资本市场绿色化发展。",
     "source_name": "中国证监会", "source_url": "https://www.csrc.gov.cn",
     "tags": ["ESG", "信息披露", "碳排放", "上市公司"]},

    {"id": 18, "title": "广东省近零碳排放区示范工程建设实施方案", "issuing_body": "广东省生态环境厅", "publish_date": "2025-11",
     "category": "地方", "topic": "零碳园区",
     "summary": "广东推进近零碳排放区示范工程建设，重点在园区、社区、校区等场景开展近零碳试点。明确技术路径选择原则、资金支持机制和考核评估方法。",
     "source_name": "广东省生态环境厅", "source_url": "https://gdee.gd.gov.cn",
     "tags": ["广东省", "近零碳", "示范工程", "试点"]},

    # === 2026年7-8月最新政策 ===
    {"id": 19, "title": "全国碳排放权交易市场扩围至水泥、电解铝行业工作方案", "issuing_body": "生态环境部", "publish_date": "2026-07-15",
     "category": "国家", "topic": "碳市场",
     "summary": "碳市场正式扩围至水泥和电解铝两大高排放行业，新增约150家重点排放单位。明确两个行业的配额分配方法、数据报告规范和核查要求，预计新增碳配额交易量约10亿吨。",
     "source_name": "生态环境部", "source_url": "https://www.mee.gov.cn",
     "tags": ["碳市场", "扩围", "水泥", "电解铝", "配额"]},

    {"id": 20, "title": "零碳园区建设标准（GB/T 51100-2026）", "issuing_body": "国家标准化管理委员会", "publish_date": "2026-07-20",
     "category": "行业标准", "topic": "零碳园区",
     "summary": "正式发布零碳园区建设国家标准，涵盖零碳园区定义、评价指标体系（含能源、建筑、交通、产业、碳汇五大维度）、等级划分（近零碳/零碳/负碳三级）和达标路径指南。标准自2027年1月1日起实施。",
     "source_name": "国家标准化管理委员会", "source_url": "https://www.sac.gov.cn",
     "tags": ["零碳园区", "国家标准", "评价指标", "等级划分"]},

    {"id": 21, "title": "关于加快推进产品碳足迹管理体系建设的意见（国市监认证发〔2026〕89号）", "issuing_body": "市场监管总局、国家发改委、生态环境部", "publish_date": "2026-07-25",
     "category": "国家", "topic": "碳核算",
     "summary": "三部门联合发文，要求到2027年建立100种重点产品碳足迹核算标准体系，到2030年实现重点行业全覆盖。推动碳标签国际互认，建设国家产品碳足迹数据库，支持企业应对CBAM等碳边境措施。",
     "source_name": "市场监管总局", "source_url": "https://www.samr.gov.cn",
     "tags": ["碳足迹", "碳标签", "产品碳核算", "国际互认"]},

    {"id": 22, "title": "EU ETS配额拍卖总收入首次突破500亿欧元——CBAM正式征收首年回顾", "issuing_body": "欧盟委员会", "publish_date": "2026-07-28",
     "category": "国际", "topic": "碳关税",
     "summary": "CBAM正式征收元年（2026）上半年进口商申报数据公布，碳关税覆盖范围扩大至氢能全产业链。中国作为欧盟最大贸易伙伴之一，出口钢铁、铝制品企业受冲击明显，需加强碳足迹核算能力建设。",
     "source_name": "欧盟CBAM官网", "source_url": "https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en",
     "tags": ["欧盟", "CBAM", "碳关税", "碳市场", "国际贸易"]},

    {"id": 23, "title": "广东省碳排放权交易管理办法（修订）（粤府令第389号）", "issuing_body": "广东省人民政府", "publish_date": "2026-08-01",
     "category": "地方", "topic": "碳市场",
     "summary": "修订省级碳交易管理办法，将碳交易覆盖行业从电力、钢铁、水泥扩展至数据中心和石化行业，新增零碳园区碳配额奖励机制，对通过零碳认证的园区给予每年5%的配额递增奖励。",
     "source_name": "广东省人民政府", "source_url": "https://www.gd.gov.cn",
     "tags": ["广东省", "碳交易", "管理办法", "零碳园区", "配额激励"]},

    {"id": 24, "title": "关于组织开展第二批零碳园区建设工作的通知（发改环资〔2026〕1360号）", "issuing_body": "国家发改委", "publish_date": "2026-08-03",
     "category": "国家", "topic": "零碳园区",
     "summary": "发改委启动第二批零碳园区建设申报工作，明确将零碳园区试点范围从省级扩展至国家级经开区、高新区等重点区域。新增评价指标包括：AI技术应用覆盖率、可再生能源消纳率、碳足迹全链条追溯等。申报截止期为2026年10月31日。",
     "source_name": "中国政府网", "source_url": "https://www.gov.cn",
     "tags": ["零碳园区", "第二批", "申报", "国家级", "评价指标"]},
]

SUPPLIERS = [
    # 电力负荷预测 (tool_id=1)
    {"id": 1, "tool_id": 1, "name": "远景科技集团", "type": "技术提供商",
     "description": "全球领先的绿色科技企业，旗下方舟AI能碳管理平台已在国内多个经开区和零碳园区部署应用。",
     "website": "https://www.envision-group.com", "contact": "400-820-7890",
     "related_case": "在沧州沧东经开区部署AI能碳管理平台，负荷预测精度>95%，日级MAPE<3%。"},
    {"id": 2, "tool_id": 1, "name": "研华科技", "type": "技术提供商",
     "description": "工业物联网与AIoT平台领导者，iEMS.AI Agent平台提供从负荷预测到能效优化的完整方案。",
     "website": "https://www.advantech.com", "contact": "400-810-8389",
     "related_case": "在某电子工厂部署短期负荷预测，预测误差<3%。"},
    {"id": 3, "tool_id": 1, "name": "清华大学能源互联网研究院", "type": "研究机构",
     "description": "国内能源预测领域的顶尖研究机构，在负荷预测算法和电力市场方面有深入研究。",
     "website": "https://www.eiri.tsinghua.edu.cn", "contact": "", "related_case": ""},

    # 储能充放电策略优化 (tool_id=4)
    {"id": 4, "tool_id": 4, "name": "宁德时代", "type": "技术提供商",
     "description": "全球动力电池与储能系统龙头，提供储能系统+AI调度一体化解决方案，在工业园区储能领域有大量案例。",
     "website": "https://www.catl.com", "contact": "400-827-6668",
     "related_case": "为多个工业园区提供储能充放电AI优化，降低用电成本10-25%。"},
    {"id": 5, "tool_id": 4, "name": "阳光电源", "type": "技术提供商",
     "description": "全球领先的光伏逆变器和储能系统供应商，智慧能源管理平台覆盖源网荷储全场景。",
     "website": "https://www.sungrowpower.com", "contact": "400-997-7766",
     "related_case": "在多地零碳园区部署光储融合系统，提升新能源自消纳率15-30%。"},

    # 暖通空调AI节能控制 (tool_id=7)
    {"id": 6, "tool_id": 7, "name": "达实智能", "type": "技术提供商",
     "description": "智慧园区和智慧建筑领域龙头，AIoT V7.1平台实现建筑能耗降低>25%，冷站SCOP达4.5以上。",
     "website": "https://www.chn-das.com", "contact": "0755-26639961",
     "related_case": "深圳某园区部署AI节能控制后建筑能耗降低超25%，投资回收期<2年。"},
    {"id": 7, "tool_id": 7, "name": "双良集团", "type": "技术提供商",
     "description": "智慧能碳管理平台获德国红点设计奖，五大能力中心+AI算法矩阵覆盖冷热电气多能系统。",
     "website": "https://www.shuangliang.com", "contact": "0510-86688888",
     "related_case": "在多地化工园区实现冷站能效SCOP达4.5-6.3，综合节能15-30%。"},
    {"id": 8, "tool_id": 7, "name": "江森自控(Johnson Controls)", "type": "技术提供商",
     "description": "全球智慧建筑解决方案领导者，OpenBlue平台结合AI与数字孪生实现建筑全生命周期低碳运营。",
     "website": "https://www.johnsoncontrols.com", "contact": "021-23279000",
     "related_case": "为全球500+工业园区提供智慧建筑节能解决方案。"},

    # 碳足迹核算 (tool_id=11)
    {"id": 9, "tool_id": 11, "name": "碳阻迹(Carbonstop)", "type": "技术提供商",
     "description": "中国领先的碳排放管理SaaS平台，服务3000+企业客户，覆盖碳核算、碳标签、碳资产管理全链条。",
     "website": "https://www.carbonstop.net", "contact": "400-080-0800",
     "related_case": "为多家制造企业提供产品碳足迹核算和碳标签生成服务，核算效率提升80%。"},
    {"id": 10, "tool_id": 11, "name": "妙盈科技(MioTech)", "type": "技术提供商",
     "description": "AI驱动的ESG与碳管理数据平台，覆盖碳核算、气候风险分析和供应链碳管理。",
     "website": "https://www.miotech.com", "contact": "021-63333688",
     "related_case": "服务金融机构和大型企业进行碳排放数据管理和TCFD披露。"},

    # 设备故障预警与健康管理 (tool_id=10)
    {"id": 11, "tool_id": 10, "name": "树根互联", "type": "技术提供商",
     "description": "工业互联网平台龙头，根云平台提供设备全生命周期管理和预测性维护AI解决方案。",
     "website": "https://www.rootcloud.com", "contact": "400-868-1122",
     "related_case": "在三一重工等制造企业部署设备故障预警，减少非计划停机40-60%。"},
    {"id": 12, "tool_id": 10, "name": "西门子(Siemens)", "type": "技术提供商",
     "description": "全球工业数字化领导者，MindSphere工业物联网平台提供从设备连接到AI预测分析的完整方案。",
     "website": "https://www.siemens.com", "contact": "400-616-2020",
     "related_case": "全球数千个工业场景部署预测性维护方案，维护成本降低25%。"},

    # 新能源车队智能调度 (tool_id=15)
    {"id": 13, "tool_id": 15, "name": "浪潮智能终端", "type": "技术提供商",
     "description": "在智慧物流和无人配送领域有深厚积累，零碳智慧物流园区方案获多项行业认可。",
     "website": "https://www.inspur.com", "contact": "400-658-6000",
     "related_case": "在苏州玄通物流园实现L4级无人配送，5G零碳智慧园区解决方案。"},
    {"id": 14, "tool_id": 15, "name": "驭势科技(UISEE)", "type": "技术提供商",
     "description": "中国领先的自动驾驶和智慧物流方案提供商，专注园区和厂区场景的无人驾驶物流解决方案。",
     "website": "https://www.uisee.com", "contact": "400-860-0066",
     "related_case": "为多个工业园区提供无人驾驶物流车调度方案，运输效率提升20%。"},

    # 零碳路径情景模拟 (tool_id=20)
    {"id": 15, "tool_id": 20, "name": "清华四川能源互联网研究院", "type": "研究机构",
     "description": "在能源系统建模、零碳路径规划和情景模拟方面有深入研究，为多个地方政府提供零碳规划咨询。",
     "website": "https://www.tsinghua-eiri.org", "contact": "", "related_case": ""},
    {"id": 16, "tool_id": 20, "name": "落基山研究所(RMI)", "type": "研究机构",
     "description": "国际知名能源转型研究智库，在中国开展零碳园区、零碳城市等前沿研究项目。",
     "website": "https://rmi.org", "contact": "", "related_case": "为国内多个零碳园区试点项目提供技术路径规划咨询。"},

    # 能碳指标智能分析 (tool_id=17)
    {"id": 17, "tool_id": 17, "name": "朗新科技", "type": "技术提供商",
     "description": "AI能源大模型与智能体协同平台，九功AI能源大模型赋能园区全景能碳运营。",
     "website": "https://www.longshine.com", "contact": "400-618-1180",
     "related_case": "在新疆甘泉堡经开区部署AI智能体协同，能效提升20%，碳排放下降15%。"},
    {"id": 18, "tool_id": 17, "name": "江西电建", "type": "技术提供商",
     "description": "智信能碳全景AI运营平台，'以电算碳'算法创新，数据采集成本降低90%。",
     "website": "https://www.jxepc.com", "contact": "0791-86212222",
     "related_case": "在江西零碳园区/工厂部署能碳全景运营，实现低成本碳管理。"},

    # === 以下为新增供应商（补齐12个工具的供应商数据）===

    # 光伏出力预测 (tool_id=2)
    {"id": 19, "tool_id": 2, "name": "华为数字能源", "type": "技术提供商",
     "description": "全球领先的数字能源解决方案提供商，智能光伏电站解决方案结合AI预测实现光伏出力精准预测和智能运维。",
     "website": "https://digitalpower.huawei.com", "contact": "400-822-9999",
     "related_case": "在多个大型地面光伏电站和园区分布式光伏项目中部署AI功率预测，预测精度MAPE<8%。"},
    {"id": 20, "tool_id": 2, "name": "天合光能", "type": "技术提供商",
     "description": "全球光伏组件龙头企业，TrinaPro智慧能源平台集成AI光伏出力预测与智能运维，覆盖源网荷储全场景。",
     "website": "https://www.trinasolar.com", "contact": "400-994-6800",
     "related_case": "为国内多个工业园区分布式光伏提供AI运维和预测解决方案，提升消纳率15%以上。"},

    # 风电功率预测 (tool_id=3)
    {"id": 21, "tool_id": 3, "name": "金风科技", "type": "技术提供商",
     "description": "全球领先的风电整机制造商和清洁能源解决方案提供商，AI风电功率预测平台覆盖单机-风场-区域三级尺度。",
     "website": "https://www.goldwind.com", "contact": "400-850-6565",
     "related_case": "在全国500+风电场部署AI功率预测系统，预测精度行业领先，MAPE<10%。"},
    {"id": 22, "tool_id": 3, "name": "远景能源", "type": "技术提供商",
     "description": "全球领先的智能风机和智慧风场解决方案商，EnOS™智能物联网平台实现风场全生命周期AI管理。",
     "website": "https://www.envision-energy.com", "contact": "400-820-7890",
     "related_case": "为阳江等海上风电基地提供AI功率预测和智慧运维，降低运维成本20%以上。"},

    # 多能流调度优化 (tool_id=5)
    {"id": 23, "tool_id": 5, "name": "清华四川能源互联网研究院", "type": "研究机构",
     "description": "在综合能源系统建模、多能流协同优化和零碳园区规划方面有深入研究，多项成果已在实际园区示范应用。",
     "website": "https://www.tsinghua-eiri.org", "contact": "028-62520099",
     "related_case": "为成都、雄安等地综合能源园区提供多能流协同优化方案，综合能效提升10-20%。"},
    {"id": 24, "tool_id": 5, "name": "中控技术", "type": "技术提供商",
     "description": "流程工业自动化与智能化龙头，工业AI+能源优化平台实现工业园区冷热电多能流耦合优化调度。",
     "website": "https://www.supcon.com", "contact": "400-826-6618",
     "related_case": "在多个化工和制造园区部署多能流AI调度系统，降低能源成本15%以上。"},

    # 氢基竖炉工艺AI优化 (tool_id=6)
    {"id": 25, "tool_id": 6, "name": "宝武集团中央研究院", "type": "研究机构",
     "description": "全球最大钢铁企业集团的核心研发机构，在氢基直接还原铁(DRI)工艺研发和AI优化方面处于国际前沿。",
     "website": "https://www.baowugroup.com", "contact": "021-26648888",
     "related_case": "在湛江钢铁氢基竖炉示范项目中开展工艺参数AI优化研究，目标降低氢气消耗5-10%。"},
    {"id": 26, "tool_id": 6, "name": "中冶赛迪", "type": "技术提供商",
     "description": "中冶集团旗下工程技术公司，在绿色低碳钢铁工艺设计和智能化方面有丰富经验，参与多个氢冶金示范项目。",
     "website": "https://www.cisdigroup.com.cn", "contact": "023-63548888",
     "related_case": "为国内多个近零碳钢铁项目提供工艺设计和智能化解决方案，助力减排50-80%。"},

    # 照明智能调控 (tool_id=8)
    {"id": 27, "tool_id": 8, "name": "昕诺飞(Signify)", "type": "技术提供商",
     "description": "全球照明行业领导者（原飞利浦照明），Interact物联网照明平台结合AI实现自适应调光和人员感应节能。",
     "website": "https://www.signify.com", "contact": "400-920-1001",
     "related_case": "在全球2000+工业园区和办公楼宇部署智能照明系统，照明节能40-70%。"},
    {"id": 28, "tool_id": 8, "name": "欧普照明", "type": "技术提供商",
     "description": "中国照明行业龙头，智慧园区照明解决方案结合IoT传感器和AI算法实现分区分时智能调控。",
     "website": "https://www.opple.com", "contact": "400-678-3222",
     "related_case": "为国内多个园区和商业综合体提供智能照明方案，延长灯具寿命30%，提升照明舒适度。"},

    # 设备能效异常诊断 (tool_id=9)
    {"id": 29, "tool_id": 9, "name": "格创东智", "type": "技术提供商",
     "description": "TCL旗下工业互联网平台，专注半导体和电子制造领域的设备能效异常诊断和预测性维护。",
     "website": "https://www.getech.cn", "contact": "400-830-9666",
     "related_case": "在多个电子制造园区部署设备能效AI诊断系统，异常定位时间缩短60%以上。"},
    {"id": 30, "tool_id": 9, "name": "ABB中国", "type": "技术提供商",
     "description": "全球电气化和自动化技术领导者，ABB Ability™平台提供设备能效诊断、预测性维护和能源管理一体化方案。",
     "website": "https://new.abb.com/cn", "contact": "400-820-9696",
     "related_case": "为全球数千个工业场景提供设备能效管理和异常诊断方案，减少非计划停机30-50%。"},

    # 产品碳标签生成 (tool_id=12)
    {"id": 31, "tool_id": 12, "name": "中国质量认证中心(CQC)", "type": "研究机构",
     "description": "国家级认证机构，国内碳标签认证领域的权威机构，提供产品碳足迹核算、核查与碳标签颁发一站式服务。",
     "website": "https://www.cqc.com.cn", "contact": "010-83886666",
     "related_case": "已为数百个产品品类提供碳足迹认证和碳标签服务，覆盖钢铁、化工、电子等多个行业。"},
    {"id": 32, "tool_id": 12, "name": "必维集团(Bureau Veritas)", "type": "咨询机构",
     "description": "全球领先的检验、检测和认证机构，提供符合ISO 14067和PAS 2050国际标准的产品碳足迹认证和碳标签服务。",
     "website": "https://www.bureauveritas.cn", "contact": "400-683-1828",
     "related_case": "为出口欧盟企业提供CBAM合规碳核查和产品碳标签国际互认服务，助力应对绿色贸易壁垒。"},

    # 危化品泄漏AI检测 (tool_id=13)
    {"id": 33, "tool_id": 13, "name": "海康威视", "type": "技术提供商",
     "description": "全球领先的智能安防和AI视觉解决方案商，危化品场景AI检测方案结合红外热成像和可见光实现全天候泄漏监测。",
     "website": "https://www.hikvision.com", "contact": "400-800-5998",
     "related_case": "在多个化工园区部署危化品泄漏AI检测系统，泄漏检出率>95%，响应时间缩短至秒级。"},
    {"id": 34, "tool_id": 13, "name": "大华股份", "type": "技术提供商",
     "description": "全球领先的以视频为核心的智慧物联解决方案商，化工园区安全AI方案涵盖泄漏检测、行为识别和应急联动。",
     "website": "https://www.dahuatech.com", "contact": "400-672-8166",
     "related_case": "为茂名、连云港等大型石化园区提供AI安全监测方案，减少安全事故风险，保障园区安全运营。"},

    # 植被碳汇遥感评估 (tool_id=14)
    {"id": 35, "tool_id": 14, "name": "航天宏图(PIE)", "type": "技术提供商",
     "description": "国内领先的遥感与地理信息服务商，PIE-Engine平台结合AI实现多尺度植被碳汇遥感评估和动态监测。",
     "website": "https://www.piesat.cn", "contact": "010-82685959",
     "related_case": "为多个省市生态碳汇监测项目提供AI遥感评估服务，碳汇评估精度较传统方法提升30%以上。"},
    {"id": 36, "tool_id": 14, "name": "中国科学院空天信息创新研究院", "type": "研究机构",
     "description": "国内遥感与地球观测领域的顶级研究机构，在生态系统碳汇遥感反演和AI深度学习应用方面有深厚积累。",
     "website": "https://www.aircas.ac.cn", "contact": "010-82178000",
     "related_case": "承担国家重点研发计划'生态系统碳汇遥感监测'项目，研发多项碳汇AI评估算法。"},

    # 岸电智能调度 (tool_id=16)
    {"id": 37, "tool_id": 16, "name": "上海振华重工(ZPMC)", "type": "技术提供商",
     "description": "全球港口机械龙头，智慧港口解决方案涵盖岸电系统集成、智能调度和能源管理，助力绿色港口建设。",
     "website": "https://www.zpmc.com", "contact": "021-31196818",
     "related_case": "在全球300+港口部署智慧港口解决方案，岸电利用率提升40%以上，减少港口碳排放30-50%。"},
    {"id": 38, "tool_id": 16, "name": "中交集团", "type": "技术提供商",
     "description": "全球领先的港口与交通基础设施综合服务商，绿色智慧港口方案涵盖岸电建设、新能源替代和AI调度优化。",
     "website": "https://www.ccccltd.cn", "contact": "010-65279999",
     "related_case": "参与汕头、汕尾等广东沿海港口绿色化改造项目，推动港口岸电和新能源替代。"},

    # 政策标准知识问答 (tool_id=18)
    {"id": 39, "tool_id": 18, "name": "百度智能云", "type": "技术提供商",
     "description": "国内领先的AI云服务商，千帆大模型平台+向量数据库方案可快速搭建双碳政策和标准领域知识问答系统。",
     "website": "https://cloud.baidu.com", "contact": "400-920-8999",
     "related_case": "为多个政府部门和企业搭建领域知识库和智能问答系统，查询效率提升90%以上。"},
    {"id": 40, "tool_id": 18, "name": "科大讯飞", "type": "技术提供商",
     "description": "国内AI领军企业，星火认知大模型+RAG方案支持零碳园区政策知识库搭建和自然语言智能问答。",
     "website": "https://www.iflytek.com", "contact": "400-019-9199",
     "related_case": "为政务、能源等行业客户提供智能问答和知识管理方案，支持领域知识库的快速构建和实时更新。"},

    # CCUS碳捕集效率AI模拟 (tool_id=19)
    {"id": 41, "tool_id": 19, "name": "华能集团清洁能源技术研究院", "type": "研究机构",
     "description": "国内CCUS技术研发的先行者，运营国内首个燃煤电厂10万吨级碳捕集示范项目，在AI-物理融合模拟方面有深入研究。",
     "website": "https://www.hnceri.com", "contact": "010-62881999",
     "related_case": "承担多项国家重点研发计划CCUS项目，研发AI+CFD碳捕集效率模拟方法，捕集能耗降低10-20%。"},
    {"id": 42, "tool_id": 19, "name": "中石化石油化工科学研究院(RIPP)", "type": "研究机构",
     "description": "中国石化核心研发机构，在炼化行业碳捕集和利用技术方面处于国内领先，运用AI加速CCUS工艺开发与优化。",
     "website": "https://ripp.sinopec.com", "contact": "010-82368800",
     "related_case": "在齐鲁石化等基地开展百万吨级CCUS项目，利用AI代理模型加速碳捕集溶剂筛选和工艺参数优化。"},
]

NEWS = [
    # === AI+双碳 (4条) ===
    {"id": 1, "title": "DeepMind发布材料发现AI，加速碳捕集新材料研发", "summary": "Google DeepMind发布新一代材料发现AI模型GNoME扩展版，成功预测38万种新型稳定晶体材料，其中数百种可用于高效碳捕集(CCUS)吸附剂，将碳捕集材料研发周期从数年缩短至数月。", "source_name": "MIT Technology Review", "source_url": "https://www.technologyreview.com", "publish_date": "2026-08-02", "category": "AI+双碳", "topic": "技术突破", "tags": ["AI", "碳捕集", "材料发现", "CCUS", "DeepMind"]},

    {"id": 2, "title": "百度联合生态环境部发布碳核算AI大模型'文心·碳策'", "summary": "百度与生态环境部信息中心联合发布'文心·碳策'AI大模型，专门针对企业碳核算场景进行训练。模型可自动解析企业能源账单、生产报表等非结构化数据，一键生成符合国家标准的碳排放报告。首批试点企业覆盖电力、钢铁、水泥三大行业120家。", "source_name": "36氪", "source_url": "https://36kr.com", "publish_date": "2026-07-28", "category": "AI+双碳", "topic": "行业应用", "tags": ["百度", "碳核算", "AI大模型", "生态环境部"]},

    {"id": 3, "title": "微软签署史上最大碳移除协议，AI优化碳信用筛选", "summary": "微软宣布与三家碳移除(CDR)供应商签署总计500万吨碳移除购买协议，创下行业纪录。微软利用自研AI平台对全球200+碳移除项目进行质量评估和风险定价，将尽职调查周期从6个月压缩至3周。", "source_name": "Bloomberg", "source_url": "https://www.bloomberg.com", "publish_date": "2026-07-15", "category": "AI+双碳", "topic": "企业动态", "tags": ["微软", "碳移除", "AI", "碳信用", "CDR"]},

    {"id": 4, "title": "IEA报告：AI技术到2030年可贡献全球碳减排量的10-15%", "summary": "国际能源署(IEA)发布《AI与能源转型》专题报告，系统评估了AI在能源系统脱碳中的潜力。报告指出：AI优化可提升全球能源效率5-8%、加速新能源材料研发50-70%、提升碳市场流动性20-30%，预计到2030年AI技术可贡献全球碳减排量的10-15%。", "source_name": "IEA", "source_url": "https://www.iea.org", "publish_date": "2026-07-10", "category": "AI+双碳", "topic": "研究报告", "tags": ["IEA", "AI", "碳减排", "能源转型", "报告"]},

    # === AI+能源 (4条) ===
    {"id": 5, "title": "华为推出'盘古能源大模型2.0'，光伏预测精度再提升", "summary": "华为云发布盘古能源大模型2.0版本，在光伏出力预测方面取得突破：15分钟级预测精度MAPE降至4.2%，首次引入时序Transformer+物理约束融合架构。新模型已在国内22个省级电网调度系统部署测试，预测精度较传统方法提升30%以上。", "source_name": "机器之心", "source_url": "https://www.jiqizhixin.com", "publish_date": "2026-08-01", "category": "AI+能源", "topic": "技术突破", "tags": ["华为", "能源大模型", "光伏预测", "Transformer"]},

    {"id": 6, "title": "蔚来能源云部署AI储能调度，换电站参与电网调峰", "summary": "蔚来能源云(NIO Power Cloud)部署AI储能调度系统，将全国3000+换电站的储能电池聚合为虚拟电厂，参与省级电网调峰辅助服务。系统基于深度强化学习实时优化每个换电站的充放电策略，年调峰收益预计超5亿元。", "source_name": "36氪", "source_url": "https://36kr.com", "publish_date": "2026-07-24", "category": "AI+能源", "topic": "行业应用", "tags": ["蔚来", "储能调度", "虚拟电厂", "强化学习", "换电站"]},

    {"id": 7, "title": "宁德时代与施耐德电气合作开发工业AI能效优化平台", "summary": "宁德时代与施耐德电气宣布战略合作，整合宁德时代的储能技术和施耐德的工业自动化能力，共同开发面向工业园区的AI能效优化平台。平台覆盖电力监控、储能调度、设备运维和碳排放管理四大模块，计划2027年Q1商用发布。", "source_name": "Reuters", "source_url": "https://www.reuters.com", "publish_date": "2026-07-18", "category": "AI+能源", "topic": "企业动态", "tags": ["宁德时代", "施耐德", "工业AI", "能效优化"]},

    {"id": 8, "title": "麦肯锡：AI驱动的智慧电网运维可降低运营成本20-35%", "summary": "麦肯锡发布《AI赋能电网：从智能运维到自主运营》报告，分析了全球30+电网运营商的AI应用实践。报告指出，AI驱动的预测性维护、智能巡检和自动故障定位可将电网运维成本降低20-35%，供电可靠率提升至99.99%以上。", "source_name": "McKinsey", "source_url": "https://www.mckinsey.com", "publish_date": "2026-07-08", "category": "AI+能源", "topic": "研究报告", "tags": ["麦肯锡", "智慧电网", "预测性维护", "AI", "报告"]},

    # === AI+零碳园区 (4条) ===
    {"id": 9, "title": "腾讯云发布'零碳园区AI大脑'解决方案，首批落地5个园区", "summary": "腾讯云正式发布面向零碳园区的'AI大脑'解决方案，集成能源预测、设备控制、碳排放核算和智能决策四大AI Agent。方案采用边云协同架构，已在深圳南山科技园、苏州工业园区等5个园区落地测试，综合能效提升18-25%。", "source_name": "InfoQ", "source_url": "https://www.infoq.cn", "publish_date": "2026-07-30", "category": "AI+零碳园区", "topic": "行业应用", "tags": ["腾讯云", "零碳园区", "AI大脑", "AI Agent"]},

    {"id": 10, "title": "阿里云中标广东省零碳园区AI能碳管理平台项目", "summary": "阿里云以1.2亿元中标'广东省零碳园区AI能碳管理平台'建设项目，将为广东省首批15个零碳园区提供统一的AI能碳管理平台。平台覆盖碳排放在线监测、能效AI诊断、碳资产管理、AI工具集市等核心功能，2027年6月前完成部署。", "source_name": "甲子光年", "source_url": "https://www.jazzyear.com", "publish_date": "2026-07-22", "category": "AI+零碳园区", "topic": "企业动态", "tags": ["阿里云", "零碳园区", "广东", "能碳管理", "中标"]},

    {"id": 11, "title": "达实智能发布AIoT V8.0，新增园区级数字孪生碳管理", "summary": "达实智能发布AIoT智慧园区平台V8.0版本，新增园区级数字孪生碳管理功能。平台基于数字孪生技术构建园区1:1三维模型，实时映射建筑、设备、能源和碳排放数据，支持'所见即所得'的碳管理决策。已获红点设计奖和IF设计奖双料认证。", "source_name": "雷锋网", "source_url": "https://www.leiphone.com", "publish_date": "2026-07-12", "category": "AI+零碳园区", "topic": "技术突破", "tags": ["达实智能", "数字孪生", "AIoT", "碳管理", "园区"]},

    {"id": 12, "title": "德勤：中国零碳园区AI技术应用市场规模2026-2030年CAGR达45%", "summary": "德勤发布《中国零碳园区AI技术应用市场白皮书》，预测中国零碳园区AI应用市场规模将从2026年的约280亿元增至2030年的约1500亿元，年复合增长率达45%。报告识别了AI在能源管理、碳核算、设备运维三大核心赛道的投资机会。", "source_name": "Deloitte", "source_url": "https://www.deloitte.com", "publish_date": "2026-07-05", "category": "AI+零碳园区", "topic": "研究报告", "tags": ["德勤", "零碳园区", "AI", "市场规模", "白皮书"]},

    # === AI+碳市场 (4条) ===
    {"id": 13, "title": "全国碳市场启动AI辅助配额分配试点", "summary": "生态环境部宣布在全国碳市场启动AI辅助配额分配试点工作。利用机器学习模型分析重点排放单位历史排放数据、产能利用率和能效对标数据，自动生成配额分配方案建议。试点覆盖电力、水泥、电解铝三大行业约2000家企业，目标将配额分配争议率降低50%。", "source_name": "全国碳市场信息网", "source_url": "https://www.cets.org.cn", "publish_date": "2026-07-26", "category": "AI+碳市场", "topic": "政策解读", "tags": ["碳市场", "AI", "配额分配", "生态环境部", "试点"]},

    {"id": 14, "title": "欧盟CBAM AI工具需求激增，碳足迹核算SaaS融资火热", "summary": "随着欧盟CBAM正式征收元年推进，面向出口企业的AI碳足迹核算SaaS工具需求激增。2026年上半年该赛道全球融资超15亿美元，CarbonChain、Watershed、Plan A三家头部企业均完成超1亿美元B轮融资。中国市场碳阻迹、妙盈科技也相继获得大额融资，估值翻倍。", "source_name": "TechCrunch", "source_url": "https://techcrunch.com", "publish_date": "2026-07-20", "category": "AI+碳市场", "topic": "企业动态", "tags": ["CBAM", "碳足迹", "SaaS", "融资", "碳核算"]},

    {"id": 15, "title": "深圳碳市场引入AI做市商算法，流动性提升35%", "summary": "深圳碳排放权交易所率先引入AI做市商算法，利用强化学习模型优化报价策略和库存管理。运行三个月数据显示：碳配额买卖价差缩小28%、日均成交量提升35%、市场深度增加50%，为中国碳市场引入AI交易机制提供先行经验。", "source_name": "21世纪经济报道", "source_url": "https://www.21jingji.com", "publish_date": "2026-07-14", "category": "AI+碳市场", "topic": "技术突破", "tags": ["深圳", "碳市场", "AI做市商", "强化学习", "流动性"]},

    {"id": 16, "title": "全球碳市场AI交易平台CarbonX获软银愿景基金领投2亿美元", "summary": "全球碳市场AI交易平台CarbonX宣布完成2亿美元C轮融资，软银愿景基金领投。CarbonX利用NLP解析全球碳市场政策文本、计算机视觉监测减排项目卫星影像、ML模型预测碳价走势，为机构投资者提供一站式碳资产AI交易服务。", "source_name": "Financial Times", "source_url": "https://www.ft.com", "publish_date": "2026-07-02", "category": "AI+碳市场", "topic": "企业动态", "tags": ["碳市场", "AI交易", "融资", "CarbonX", "软银"]},

    # === 国际动态 (4条) ===
    {"id": 17, "title": "美国能源部投入12亿美元建设'AI for Net-Zero'国家实验室集群", "summary": "美国能源部(DOE)宣布投入12亿美元建设'AI for Net-Zero'国家实验室集群，联合NREL、ORNL、LBNL等6大国家实验室，聚焦AI驱动的清洁能源材料发现、电网智能调度、碳捕集工艺优化三大方向。计划2028年前部署超过100个AI模型到实际工业场景。", "source_name": "DOE News", "source_url": "https://www.energy.gov", "publish_date": "2026-07-29", "category": "国际动态", "topic": "政策解读", "tags": ["美国", "DOE", "AI", "净零", "国家实验室"]},

    {"id": 18, "title": "欧盟启动'AI4GreenDeal'计划，20亿欧元支持AI助力碳中和", "summary": "欧盟委员会正式启动'AI4GreenDeal'研究与创新计划，总预算20亿欧元，资助AI在工业脱碳、智慧能源、可持续农业和循环经济四大领域的应用研究。计划特别强调AI工具必须符合欧盟AI Act的可信AI标准，确保在环境领域AI应用的安全性和公平性。", "source_name": "European Commission", "source_url": "https://ec.europa.eu", "publish_date": "2026-07-17", "category": "国际动态", "topic": "政策解读", "tags": ["欧盟", "AI4GreenDeal", "碳中和", "AI Act", "绿色新政"]},

    {"id": 19, "title": "英伟达发布Earth-3气候AI基础模型，碳排放监测精度达米级", "summary": "英伟达在GTC 2026夏季大会上发布Earth-3气候AI基础模型，基于1000亿参数的Transformer架构在PB级卫星和气象数据上训练。模型首次实现全球碳排放源的米级分辨率实时监测，可识别单个工厂、发电站甚至大型建筑的碳排放异常，为碳市场监管和减排验证提供技术支撑。", "source_name": "Wired", "source_url": "https://www.wired.com", "publish_date": "2026-07-06", "category": "国际动态", "topic": "技术突破", "tags": ["英伟达", "气候AI", "碳排放监测", "基础模型", "Earth-3"]},

    {"id": 20, "title": "世界经济论坛：AI+气候科技入选2026年十大新兴技术之首", "summary": "世界经济论坛(WEF)发布《2026年十大新兴技术》报告，AI+气候科技位列榜首。报告指出，AI与气候科技的融合将是未来十年最具变革性的技术浪潮，预计到2035年AI将为全球碳中和转型创造超过10万亿美元的经济价值。零碳园区AI工具、碳市场AI交易、新能源AI预测被列为三大核心应用场景。", "source_name": "World Economic Forum", "source_url": "https://www.weforum.org", "publish_date": "2026-06-29", "category": "国际动态", "topic": "研究报告", "tags": ["WEF", "AI", "气候科技", "十大技术", "报告"]},
]
