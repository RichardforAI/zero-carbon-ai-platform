"""Whitepaper API — aggregates all platform data."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import Tool, Park, Case, Policy, Category
from ..schemas import WhitepaperData, ReportSection

router = APIRouter(prefix="/api/whitepaper", tags=["whitepaper"])


@router.get("")
def get_whitepaper(db: Session = Depends(get_db)):
    """Aggregate all platform data into whitepaper structure."""
    tools = db.query(Tool).order_by(Tool.maturity.desc()).all()
    parks = db.query(Park).order_by(Park.id).all()
    cases = db.query(Case).all()
    policies = db.query(Policy).order_by(Policy.publish_date.desc()).all()
    categories = {c.id: c for c in db.query(Category).all()}

    now = datetime.now(timezone.utc).strftime("%Y年%m月%d日")

    chapters = []

    # Chapter 1: Overview
    ch1 = f"""## 零碳园区建设背景与意义

全球气候变化已成为人类面临的最严峻挑战之一。截至2026年，全球已有超过140个国家提出碳中和目标。中国于2020年提出"2030年前碳达峰、2060年前碳中和"的"双碳"目标，零碳园区建设是实现这一目标的重要抓手。

零碳园区是指在一定时期内，通过能源结构优化、产业转型升级、碳捕集与封存等手段，实现园区内碳排放与碳吸收平衡的产业园区。广东省作为中国经济第一大省和制造业重镇，于2026年3月发布了首批15个省级零碳园区建设名单。

## AI技术在零碳园区的应用价值

人工智能技术在零碳园区建设中发挥关键作用。平台梳理的**{len(tools)}个AI工具**覆盖**{len(categories)}大技术分类**，从预测、优化、控制到诊断和核算，为园区提供全方位的AI赋能方案。AI技术可以：
- **提升能效**：通过智能预测与优化，实现能源系统效率提升15-30%
- **降低碳排放**：精准碳核算与碳资产管理，辅助碳减排决策
- **优化运维**：设备故障预警与智能诊断，减少非计划停机40-60%
- **辅助决策**：零碳路径情景模拟，科学规划碳中和技术路线

## 本白皮书编制说明

本白皮书基于"AI赋能零碳园区策略平台"实时数据自动生成，数据更新时间：**{now}**。白皮书汇集了平台的政策法规库、园区信息库、AI工具库和商业案例库的核心内容，旨在为园区管理者、政策制定者和行业研究者提供系统化的参考。"""

    chapters.append(ReportSection(title="第一章  概述", level=1, content=ch1))

    # Chapter 2: Policy Landscape
    intl_policies = [p for p in policies if p.category == "国际"]
    national_policies = [p for p in policies if p.category == "国家"]
    local_policies = [p for p in policies if p.category == "地方"]
    standards = [p for p in policies if p.category == "行业标准"]

    ch2 = f"""## 国际双碳政策概览

当前国际双碳政策体系以欧盟为核心，主要包括碳排放交易体系(EU ETS)、碳边境调节机制(CBAM)以及国际海事组织(IMO)的航运减排战略。

"""
    for p in intl_policies[:3]:
        ch2 += f"### {p.title}\n\n{p.summary}\n\n"

    ch2 += f"""## 中国双碳政策体系

中国政府围绕"双碳"目标构建了完整的政策体系。截至目前，平台收录国家级双碳政策**{len(national_policies)}项**，涵盖碳市场建设、零碳园区/工厂创建、碳排放核算标准等关键领域。

"""
    for p in national_policies[:4]:
        ch2 += f"### {p.title}\n\n发布机构：{p.issuing_body} | 发布日期：{p.publish_date}\n\n{p.summary}\n\n"

    ch2 += f"""## 广东省零碳园区政策专项

广东省作为首批零碳园区试点省份，在政策制定和实践探索方面走在前列。平台收录广东省及地方双碳政策**{len(local_policies)}项**，行业标准**{len(standards)}项**。

"""
    for p in local_policies[:2]:
        ch2 += f"### {p.title}\n\n{p.summary}\n\n"

    chapters.append(ReportSection(title="第二章  政策环境", level=1, content=ch2))

    # Chapter 3: Park Classification
    primary_types = {}
    for park in parks:
        pt = park.park_type_primary or "其他"
        if pt not in primary_types:
            primary_types[pt] = []
        primary_types[pt].append(park)

    ch3 = f"""## 园区类型体系

基于对广东省15个省级零碳园区的系统分析，平台将园区分为**{len(primary_types)}大一级分类**，每个分类下设若干二级细分类型。

"""
    pt_descriptions = {
        "工业园区": "以工业生产制造为核心，包括重化工、装备制造、电子信息等细分类型。能耗以电力和工业用热为主，碳排放集中在工艺过程和电力消耗。",
        "公建园区": "以公共建筑群为核心，包括政务中心、商务楼宇、医院、学校等。能耗以建筑用电（空调+照明+IT）为主，碳排放主要来自外购电力。",
        "高新园区": "以科技研发和创新孵化为主导，包括科技园、孵化器、数据中心集群等。数据中心PUE优化和实验室能效管理是核心挑战。",
        "物流/农业园区": "以物流仓储和现代农业为主导，包括仓储物流中心、现代农业产业园。港口岸电、冷链制冷和物流车辆电动化是主要减碳路径。",
    }
    for pt_name, pt_parks in primary_types.items():
        desc = pt_descriptions.get(pt_name, "")
        ch3 += f"### {pt_name}（{len(pt_parks)}个园区）\n\n{desc}\n\n"
        # Get secondary types
        secondary = list(set(p.park_type_secondary for p in pt_parks if p.park_type_secondary))
        ch3 += f"细分类型：{'、'.join(secondary)}\n\n"
        for park in pt_parks[:3]:
            ch3 += f"- **{park.name}**（{park.city}）：{park.industry or ''}。{park.core_challenges or ''[:80]}...\n"

    # Statistics per type
    ch3 += "\n## 各类型园区零碳建设重点\n\n"
    for pt_name, pt_parks in primary_types.items():
        ch3 += f"### {pt_name}\n\n"
        for park in pt_parks:
            ch3 += f"**{park.name}**\n"
            if park.key_directions:
                ch3 += f"- 关键方向：{'、'.join(park.key_directions)}\n"
            if park.energy_profile:
                ch3 += f"- 能耗特征：{park.energy_profile[:120]}...\n"
            if park.core_challenges:
                ch3 += f"- 核心挑战：{park.core_challenges[:120]}...\n"
            ch3 += "\n"

    chapters.append(ReportSection(title="第三章  零碳园区分类与特征", level=1, content=ch3))

    # Chapter 4: AI Tool Catalog
    ch4 = f"""## 九大AI工具分类总览

平台目前收录**{len(tools)}个AI工具**，覆盖**{len(categories)}大技术分类**。以下是各分类的工具数量和代表性工具：

"""
    for cat in sorted(categories.values(), key=lambda c: c.id):
        cat_tools = [t for t in tools if t.category_id == cat.id]
        top_tool = cat_tools[0] if cat_tools else None
        ch4 += f"### {cat.icon} {cat.name}（{len(cat_tools)}个工具）\n\n{cat.description}\n\n"
        if top_tool:
            ch4 += f"代表工具：**{top_tool.name}**（成熟度：{'★'*top_tool.maturity}{'☆'*(5-top_tool.maturity)}）\n\n"

    # Top 10 tools
    ch4 += "## 典型AI工具详解（Top 10）\n\n"
    top_tools = tools[:10]
    for t in top_tools:
        cat = categories.get(t.category_id)
        ch4 += f"""### {t.name}

- **分类**：{cat.name if cat else '未分类'} | **成熟度**：{'★'*t.maturity}{'☆'*(5-t.maturity)}（{t.maturity}/5）
- **运营环节**：{t.operation_phase or '未指定'}
- **适用园区类型**：{'、'.join(t.applicable_park_types) if t.applicable_park_types else '全部'}
- **描述**：{t.description or ''}
- **应用场景**：{t.scenario or ''}
- **AI方法**：{t.ai_method or ''}
- **技术路径**：{'、'.join(t.tech_path) if t.tech_path else ''}
- **价值主张**：{'、'.join(t.value_props) if t.value_props else ''}
- **前置条件**：{t.prerequisites or ''}
- **已有案例**：{t.case_count}个

"""

    chapters.append(ReportSection(title="第四章  AI工具赋能体系", level=1, content=ch4))

    # Chapter 5: Cases
    ch5 = f"""## 国内外标杆平台案例

平台收录了**{len(cases)}个**国内外零碳/AI能碳管理领域的标杆平台案例，涵盖了园区综合能碳管理、工业AI优化、智慧物流等多个应用方向。

"""
    for c in cases:
        tool_name = ""
        for t in tools:
            if t.id == c.tool_id:
                tool_name = t.name
                break
        ch5 += f"""### {c.platform_name or '未命名案例'}

- **关联工具**：{tool_name}
- **实施效果**：{c.effect or ''}
- **案例描述**：{c.summary or ''}

"""

    ch5 += """## 园区AI应用效果量化数据

根据平台收录的案例数据，AI工具在零碳园区中的应用已取得显著效果：

- **能效提升**：暖通空调AI节能控制可实现综合节能**15-30%**，投资回收期**1-2年**
- **碳排降低**：碳足迹核算与管理工具可帮助企业降低碳排放**10-20%**
- **运维优化**：设备故障预警系统可减少非计划停机**40-60%**
- **预测精度**：电力负荷预测MAPE可控制在**5%以内**
- **成本节约**：储能优化策略可降低用电成本**10-25%**

这些数据表明，AI技术在零碳园区中的应用不仅能带来可量化的环境效益，也具有显著的经济可行性。"""

    chapters.append(ReportSection(title="第五章  案例与最佳实践", level=1, content=ch5))

    # Chapter 6: Recommendations
    ch6 = """## 分阶段实施建议

### 第一阶段：基础建设期（近期，6-12个月）
- **数据采集体系**：部署IoT传感器和能源监测系统，建立园区级数据基础
- **成熟工具先行**：优先部署成熟度≥4的工具（电力负荷预测、空调节能控制、照明调控）
- **碳核算体系**：建立Scope 1/2碳排放核算机制，摸清碳家底

### 第二阶段：核心部署期（中期，1-2年）
- **能源系统优化**：部署储能调度优化、多能流协同等高级优化工具
- **设备运维升级**：关键设备接入故障预警与健康管理系统
- **碳资产经营**：开展碳交易、碳标签、碳足迹认证等碳资产管理

### 第三阶段：优化提升期（远期，2-3年）
- **全场景覆盖**：补足碳汇管理、供应链碳管理、水资源优化等薄弱环节
- **智能化升级**：利用数字孪生、情景模拟等前沿工具实现智能决策
- **生态构建**：形成园区间碳管理协同机制，输出可复制的零碳园区模式

## 关键成功因素

1. **数据基础**：高质量、高频次的能源与碳排放数据是所有AI工具发挥价值的前提
2. **人才保障**：建立具备AI运维和碳管理能力的专业团队
3. **政策协同**：充分利用国家和地方双碳政策红利，获取资金和技术支持
4. **分步实施**：按照"基础建设→核心部署→优化提升"三阶段有序推进，避免资源分散

## 未来趋势展望

1. **AI Agent自主运营**：AI Agent将实现园区能源系统的自主监测、自主决策和自主调优
2. **园区碳资产金融化**：碳配额、CCER等碳资产将深度融入园区运营管理体系
3. **数字孪生全息管理**：园区级数字孪生将实现物理世界与数字世界的实时映射与协同优化
4. **跨园区协同网络**：多园区间的能源调度、碳配额调剂和数据共享将成为趋势"""

    chapters.append(ReportSection(title="第六章  实施建议与展望", level=1, content=ch6))

    return WhitepaperData(
        title="AI赋能零碳园区建设白皮书（2026年版）",
        last_updated=now,
        chapters=chapters,
    )
