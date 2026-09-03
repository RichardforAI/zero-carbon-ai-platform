"""One-click Update API — LLM-powered data refresh with demo fallback."""
import random
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Policy, Tool, Case, News, Category, UpdateLog
from ..schemas import UpdateRequest, UpdateResult, UpdateDetail
from ..services.llm_service import chat_json, is_configured

router = APIRouter(prefix="/api/update", tags=["update"])

# Demo data pools for when LLM is not configured
DEMO_POLICIES = [
    {"title": "关于进一步推动零碳园区数字化管理的指导意见", "issuing_body": "国家发改委、国家数据局", "publish_date": "2026-08-10", "category": "国家", "topic": "零碳园区", "summary": "推动零碳园区数字化管理平台建设，明确数据采集标准、AI应用要求、碳排放在线监测等技术规范，要求2027年底前省级零碳园区全部接入国家级数字化管理平台。", "source_name": "中国政府网", "source_url": "", "tags": ["数字化", "零碳园区", "AI应用", "数据标准"]},
    {"title": "国际可持续发展准则理事会(ISSB)发布AI碳排放披露指南", "issuing_body": "ISSB", "publish_date": "2026-08-05", "category": "国际", "topic": "碳核算", "summary": "ISSB发布AI技术在碳排放披露中应用的专项指南，明确使用AI进行碳排放核算时的数据质量要求、模型透明度标准和审计追溯规范。", "source_name": "IFRS Foundation", "source_url": "https://www.ifrs.org", "tags": ["ISSB", "碳核算", "AI", "披露", "国际标准"]},
    {"title": "科技部发布'AI+双碳'重点研发计划2027年度项目申报指南", "issuing_body": "科技部", "publish_date": "2026-08-02", "category": "国家", "topic": "能源转型", "summary": "科技部发布2027年度'AI+双碳'重点研发计划指南，设置AI能源预测、碳捕集材料智能设计、零碳园区数字孪生、碳市场AI监管等8个重点方向，单个项目支持额度最高5000万元。", "source_name": "科技部", "source_url": "", "tags": ["科技部", "AI", "双碳", "重点研发", "资助"]},
]

DEMO_TOOLS = [
    {"name": "工业余热回收AI优化", "category_id": 2, "maturity": 3, "description": "利用AI模型优化工业余热回收系统的运行参数，最大化余热利用效率。适用于钢铁、化工、水泥等高耗能行业的余热发电和余热供暖场景。", "scenario": "工业园区存在大量中低温工业余热未被有效利用（利用率<30%），通过AI优化余热回收系统可以显著提升能源利用效率。", "ai_method": "基于热力学模型+数据驱动的混合AI方法，实时优化余热回收系统的换热参数、循环水流量和储热策略。", "tech_path": ["热力学仿真+AI", "深度强化学习", "多目标优化", "数字孪生"], "value_props": ["余热利用率提升至50-60%", "年节能收益超1000万元", "减少碳排放10-15%"], "prerequisites": "余热资源调研数据，换热系统运行参数（温度/流量/压力）", "implementation_tips": "建议先开展余热资源普查，确定余热品位和可利用量，再部署AI优化系统。", "operation_phase": "工业生产过程", "applicable_park_types": ["重化工近零碳型", "先进制造型"], "scene_tags": ["能源管理"], "case_count": 2, "version": "1.0"},
    {"name": "绿色建筑AI设计优化", "category_id": 9, "maturity": 3, "description": "基于AI生成式设计技术，在建筑设计阶段自动优化建筑形态、围护结构、遮阳系统和自然通风方案，最大化建筑全生命周期碳减排潜力。", "scenario": "适用于园区新建或改造建筑的前期设计阶段，通过AI辅助生成低碳建筑方案。", "ai_method": "生成式AI+建筑性能模拟（能耗/采光/通风/碳排放）的集成优化框架，实现设计-模拟-优化闭环。", "tech_path": ["生成式AI(GAN/扩散模型)", "建筑性能模拟(EnergyPlus)", "多目标优化", "参数化设计"], "value_props": ["建筑全生命周期碳排放降低20-35%", "设计效率提升10倍", "建筑运营能耗降低30%+"], "prerequisites": "项目用地信息、当地气候数据、建筑功能需求和面积指标", "implementation_tips": "建议在概念设计阶段即引入AI优化，与传统设计流程并行推进。", "operation_phase": "综合规划决策", "applicable_park_types": ["生态高新技术型", "先进制造型"], "scene_tags": ["建筑运行", "园区综合规划"], "case_count": 1, "version": "1.0"},
    {"name": "碳资产AI量化交易策略", "category_id": 5, "maturity": 2, "description": "利用AI量化分析模型预测碳配额价格走势，辅助园区制定碳配额交易策略和碳资产配置方案。", "scenario": "园区需要进行碳配额买卖决策，希望通过AI分析优化交易时机和交易量，降低履约成本。", "ai_method": "多因子量化模型+时序预测+强化学习的集成方法，综合考虑碳市场供需、政策变化、能源价格和宏观经济指标。", "tech_path": ["时序预测(LSTM/Transformer)", "多因子量化模型", "强化学习", "NLP政策分析"], "value_props": ["降低碳履约成本10-20%", "碳价预测准确率>80%", "碳资产收益率提升15%+"], "prerequisites": "碳市场历史交易数据（至少2年），园区碳配额仓位数据", "implementation_tips": "建议先以模拟交易验证策略有效性，再逐步投入实盘交易。", "operation_phase": "碳核算与交易", "applicable_park_types": ["重化工近零碳型", "先进制造型", "新材料型"], "scene_tags": ["园区综合规划"], "case_count": 0, "version": "1.0"},
]

DEMO_CASES = [
    {"tool_id": 15, "park_id": None, "platform_name": "西井科技Qomolo无人驾驶重卡", "summary": "在天津港零碳码头部署AI无人驾驶集装箱卡车", "effect": "替代柴油集卡，年减碳超1万吨，运营效率提升30%", "source_url": ""},
    {"tool_id": 17, "park_id": None, "platform_name": "远景方舟能碳管理平台V3.0", "summary": "在鄂尔多斯零碳产业园部署全景能碳AI管理", "effect": "实现100%绿电覆盖，年碳减排超100万吨", "source_url": ""},
    {"tool_id": 20, "park_id": None, "platform_name": "落基山研究所(RMI)零碳路径模拟器", "summary": "为深圳市提供全市零碳转型路径AI情景模拟", "effect": "量化12条技术路径的减碳贡献，优化投资组合超千亿", "source_url": ""},
    {"tool_id": 18, "park_id": None, "platform_name": "智谱AI碳政策知识库", "summary": "为广东省发改委搭建双碳政策智能问答系统", "effect": "政策查询效率提升90%，覆盖3000+政策文件", "source_url": ""},
    {"tool_id": 6, "park_id": None, "platform_name": "普锐特(Primetals)氢基炼钢AI优化", "summary": "在奥地利林茨钢厂部署氢基直接还原AI控制系统", "effect": "氢气消耗降低8%，DRI金属化率提升至96%", "source_url": ""},
]

DEMO_NEWS = [
    {"title": "OpenAI与Bloomberg合作开发碳市场AI分析工具", "summary": "OpenAI与Bloomberg宣布合作，基于GPT-5架构开发碳市场AI分析工具，可实时解析全球碳市场政策变化、预测碳价走势、生成碳交易策略建议。首批覆盖EU ETS、中国全国碳市场和加州碳市场三大交易体系。", "source_name": "The Verge", "source_url": "https://www.theverge.com", "publish_date": "2026-08-10", "category": "AI+碳市场", "topic": "企业动态", "tags": ["OpenAI", "碳市场", "AI分析", "GPT-5"]},
    {"title": "中国AI零碳园区解决方案出海东南亚，首批落地越南新加坡", "summary": "远景科技、朗新科技等中国企业联合出海，将中国零碳园区AI解决方案输出至东南亚。首批项目落地越南海防工业园和新加坡裕廊创新区，输出AI能碳管理、光伏预测和储能调度等核心模块。", "source_name": "新华网", "source_url": "https://www.xinhuanet.com", "publish_date": "2026-08-08", "category": "AI+零碳园区", "topic": "行业应用", "tags": ["出海", "零碳园区", "东南亚", "远景科技", "朗新"]},
    {"title": "谷歌DeepMind发布'碳中和城市'AI规划工具CityCarbon", "summary": "DeepMind发布CityCarbon工具，基于强化学习和多智能体模拟，为城市规划者提供碳排放最优的城市/园区空间布局方案。工具已在哥本哈根、阿姆斯特丹和深圳进行试点测试，规划方案平均可降低城市运营碳排放18-25%。", "source_name": "Nature Cities", "source_url": "https://www.nature.com", "publish_date": "2026-08-03", "category": "国际动态", "topic": "技术突破", "tags": ["DeepMind", "碳中和城市", "AI规划", "强化学习"]},
    {"title": "特斯拉发布Autobidder 3.0，AI储能交易覆盖中国碳市场", "summary": "特斯拉发布Autobidder 3.0 AI储能交易平台，新增中国碳市场和CCER交易接口。平台利用深度强化学习同时优化储能在电力现货市场、辅助服务市场和碳市场的多市场套利策略，已在上海、广东试点接入。", "source_name": "Electrek", "source_url": "https://electrek.co", "publish_date": "2026-07-31", "category": "AI+能源", "topic": "企业动态", "tags": ["特斯拉", "储能", "AI交易", "碳市场", "Autobidder"]},
    {"title": "世界经济论坛联合清华发布《全球零碳园区AI应用最佳实践2026》", "summary": "WEF与清华大学碳中和研究院联合发布年度报告，收录了来自15个国家36个零碳园区的AI应用最佳实践案例。报告提出'AI零碳成熟度模型'，将园区AI应用水平分为初始级、应用级、集成级和自主级四个阶段。", "source_name": "World Economic Forum", "source_url": "https://www.weforum.org", "publish_date": "2026-07-25", "category": "国际动态", "topic": "研究报告", "tags": ["WEF", "清华", "零碳园区", "AI", "最佳实践"]},
]


@router.post("/all")
def update_all(data: UpdateRequest, db: Session = Depends(get_db)):
    """One-click update: refresh policies, tools, cases, and news data."""
    modules = data.modules or ["policies", "tools", "cases", "news"]
    count = data.count_per_module or 2
    use_llm = is_configured()

    summary = {"new_policies": 0, "new_tools": 0, "new_cases": 0, "new_news": 0}
    details: list[UpdateDetail] = []

    # --- Policies ---
    if "policies" in modules:
        try:
            if use_llm:
                result = chat_json([
                    {"role": "system", "content": f"你是一个双碳政策数据库。请生成{count}条最新的（2026年7-8月）中国双碳政策/零碳园区政策，每条包含title,issuing_body,publish_date,category(国家/地方/行业标准/国际),topic(碳市场/零碳园区/碳核算/能源转型/绿色航运/碳关税),summary(80-150字),source_name,source_url,tags(3-5个关键词数组)。返回JSON数组。"},
                    {"role": "user", "content": f"请生成{count}条2026年最新双碳政策数据"},
                ], temperature=0.5, max_tokens=2048)
                if isinstance(result, list):
                    for item in result[:count]:
                        item.pop("id", None)
                        item.setdefault("tags", [])
                        item.setdefault("full_text_url", "")
                        db.add(Policy(**item))
                        summary["new_policies"] += 1
                        details.append(UpdateDetail(module="policies", title=item.get("title", "")[:80], action="created"))
            else:
                # Demo mode
                pool = [p for p in DEMO_POLICIES if not db.query(Policy).filter(Policy.title == p["title"]).first()]
                for item in random.sample(pool, min(count, len(pool))):
                    item_copy = {**item}
                    item_copy.setdefault("tags", [])
                    item_copy.setdefault("full_text_url", "")
                    item_copy.setdefault("source_url", "")
                    db.add(Policy(**item_copy))
                    summary["new_policies"] += 1
                    details.append(UpdateDetail(module="policies", title=item["title"][:80], action="created"))
        except Exception as e:
            details.append(UpdateDetail(module="policies", title=f"更新失败: {str(e)[:60]}", action="error"))

    # --- Tools ---
    if "tools" in modules:
        try:
            if use_llm:
                cats = db.query(Category).all()
                cat_list = ", ".join(f"ID:{c.id}={c.name}" for c in cats)
                result = chat_json([
                    {"role": "system", "content": f"你是零碳园区AI工具专家。可用的分类ID: {cat_list}。请生成{count}个原创AI工具条目，每个包含name,category_id(1-9中选择匹配的),maturity(1-5),description,scenario,ai_method,tech_path(3-5个),value_props(3-4个),prerequisites,implementation_tips,operation_phase,applicable_park_types(从[先进制造型,重化工近零碳型,新能源装备制造型,新材料型,临港特色产业型,生态高新技术型]中选择),scene_tags(从[建筑运行,能源管理,交通物流,水资源管理,废弃物管理,碳汇管理,供应链碳管理,园区综合规划]中选择),case_count,version。返回JSON数组。"},
                    {"role": "user", "content": f"请生成{count}个原创的零碳园区AI工具"},
                ], temperature=0.6, max_tokens=2048)
                if isinstance(result, list):
                    for item in result[:count]:
                        item.pop("id", None)
                        item.setdefault("tech_path", [])
                        item.setdefault("value_props", [])
                        item.setdefault("applicable_park_types", [])
                        item.setdefault("scene_tags", [])
                        item.setdefault("case_count", 0)
                        item.setdefault("version", "1.0")
                        item.setdefault("updated_at", datetime.now(timezone.utc))
                        db.add(Tool(**item))
                        summary["new_tools"] += 1
                        details.append(UpdateDetail(module="tools", title=item.get("name", "")[:80], action="created"))
            else:
                existing_names = {t.name for t in db.query(Tool).all()}
                pool = [t for t in DEMO_TOOLS if t["name"] not in existing_names]
                for item in random.sample(pool, min(count, len(pool))):
                    item_copy = {**item}
                    item_copy.setdefault("updated_at", datetime.now(timezone.utc))
                    db.add(Tool(**item_copy))
                    summary["new_tools"] += 1
                    details.append(UpdateDetail(module="tools", title=item["name"], action="created"))
        except Exception as e:
            details.append(UpdateDetail(module="tools", title=f"更新失败: {str(e)[:60]}", action="error"))

    # --- Cases ---
    if "cases" in modules:
        try:
            if use_llm:
                result = chat_json([
                    {"role": "system", "content": f"你是零碳园区AI应用案例专家。请生成{count}个商业平台案例，每个包含platform_name,summary(50-120字),effect(50-100字),source_url。返回JSON数组。"},
                    {"role": "user", "content": f"请生成{count}个零碳园区AI应用商业案例"},
                ], temperature=0.5, max_tokens=1024)
                if isinstance(result, list):
                    for item in result[:count]:
                        item.pop("id", None)
                        item.pop("tool_id", None)
                        item.pop("park_id", None)
                        item.setdefault("tool_id", random.randint(1, 20))
                        item.setdefault("park_id", None)
                        item.setdefault("source_url", "")
                        db.add(Case(**item))
                        summary["new_cases"] += 1
                        details.append(UpdateDetail(module="cases", title=item.get("platform_name", "")[:80], action="created"))
            else:
                existing_platforms = {c.platform_name for c in db.query(Case).all()}
                pool = [c for c in DEMO_CASES if c["platform_name"] not in existing_platforms]
                for item in random.sample(pool, min(count, len(pool))):
                    db.add(Case(**item))
                    summary["new_cases"] += 1
                    details.append(UpdateDetail(module="cases", title=item["platform_name"], action="created"))
        except Exception as e:
            details.append(UpdateDetail(module="cases", title=f"更新失败: {str(e)[:60]}", action="error"))

    # --- News ---
    if "news" in modules:
        try:
            if use_llm:
                result = chat_json([
                    {"role": "system", "content": f"你是AI+双碳领域的新闻编辑。请生成{count}条最新(2026年7-8月)的全球AI+双碳/零碳/能源领域新闻，每条包含title,summary(80-150字),source_name,source_url,publish_date(格式YYYY-MM-DD),category(AI+双碳/AI+能源/AI+零碳园区/AI+碳市场/国际动态),topic(技术突破/行业应用/企业动态/研究报告/政策解读),tags(3-5个关键词数组)。返回JSON数组。"},
                    {"role": "user", "content": f"请生成{count}条2026年最新的AI+双碳领域新闻"},
                ], temperature=0.5, max_tokens=2048)
                if isinstance(result, list):
                    for item in result[:count]:
                        item.pop("id", None)
                        item.setdefault("tags", [])
                        item.setdefault("source_url", "")
                        db.add(News(**item))
                        summary["new_news"] += 1
                        details.append(UpdateDetail(module="news", title=item.get("title", "")[:80], action="created"))
            else:
                existing_titles = {n.title for n in db.query(News).all()}
                pool = [n for n in DEMO_NEWS if n["title"] not in existing_titles]
                for item in random.sample(pool, min(count, len(pool))):
                    item_copy = {**item}
                    item_copy.setdefault("tags", [])
                    item_copy.setdefault("source_url", "")
                    db.add(News(**item_copy))
                    summary["new_news"] += 1
                    details.append(UpdateDetail(module="news", title=item["title"][:80], action="created"))
        except Exception as e:
            details.append(UpdateDetail(module="news", title=f"更新失败: {str(e)[:60]}", action="error"))

    # Commit all changes (including update log)
    total = sum(summary.values())
    try:
        # Record the update event in update_logs
        if total > 0:
            desc_parts = []
            if summary.get("new_policies"): desc_parts.append(f"政策+{summary['new_policies']}")
            if summary.get("new_tools"): desc_parts.append(f"工具+{summary['new_tools']}")
            if summary.get("new_cases"): desc_parts.append(f"案例+{summary['new_cases']}")
            if summary.get("new_news"): desc_parts.append(f"新闻+{summary['new_news']}")
            db.add(UpdateLog(
                tool_id=None,
                version=None,
                change_type="data_update",
                description="一键更新：" + "、".join(desc_parts) + f"（{'AI生成' if use_llm else 'Demo模式'}）",
                created_at=datetime.now(timezone.utc),
            ))
        db.commit()
    except Exception as e:
        db.rollback()
        return UpdateResult(
            status="error",
            mode="llm" if use_llm else "demo",
            summary={"new_policies": 0, "new_tools": 0, "new_cases": 0, "new_news": 0},
            details=[UpdateDetail(module="system", title=f"数据库提交失败: {str(e)[:60]}", action="error")],
        )
    return UpdateResult(
        status="ok" if total > 0 else "partial",
        mode="llm" if use_llm else "demo",
        summary=summary,
        details=details,
    )
