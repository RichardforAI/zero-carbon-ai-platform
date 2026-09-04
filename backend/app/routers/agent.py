"""AI Agent API — LLM-powered matching and report generation."""
import json
import re
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Park, Tool, Category, Policy
from ..schemas import (
    AgentMatchRequest,
    AgentMatchResult,
    AgentReportRequest,
    AgentReportResult,
    RecommendedTool,
    ReportSection,
    ParkBrief,
)
from ..services.llm_service import chat, chat_json, is_configured

router = APIRouter(prefix="/api/agent", tags=["agent"])


def _build_tool_summary(tools: list[Tool], categories: dict[int, Category]) -> str:
    """Build a compact text summary of all tools for the LLM prompt."""
    lines = []
    for t in tools:
        cat = categories.get(t.category_id)
        cat_name = cat.name if cat else "未分类"
        lines.append(
            f"ID:{t.id} | {t.name} | 分类:{cat_name} | 成熟度:{t.maturity}/5 | "
            f"运营环节:{t.operation_phase or '未指定'} | "
            f"适用园区类型:{','.join(t.applicable_park_types) if t.applicable_park_types else '全部'} | "
            f"描述:{t.description or ''[:80]}"
        )
    return "\n".join(lines)


def _build_tool_detail(tools: list[Tool], categories: dict[int, Category]) -> str:
    """Build a detailed summary of all tools for report generation."""
    lines = []
    for t in tools:
        cat = categories.get(t.category_id)
        cat_name = cat.name if cat else "未分类"
        lines.append(f"""
### {t.name} (ID:{t.id})
- **分类**: {cat_name}
- **成熟度**: {'★' * t.maturity}{'☆' * (5 - t.maturity)} ({t.maturity}/5)
- **运营环节**: {t.operation_phase or '未指定'}
- **适用园区类型**: {', '.join(t.applicable_park_types) if t.applicable_park_types else '全部'}
- **描述**: {t.description or ''}
- **应用场景**: {t.scenario or ''}
- **AI方法**: {t.ai_method or ''}
- **技术路径**: {', '.join(t.tech_path) if t.tech_path else ''}
- **价值主张**: {', '.join(t.value_props) if t.value_props else ''}
- **前提条件**: {t.prerequisites or ''}
- **案例数量**: {t.case_count}
""")
    return "\n".join(lines)


@router.post("/match")
def agent_match(req: AgentMatchRequest, db: Session = Depends(get_db)):
    """AI-powered intelligent tool matching for a park."""
    park = db.query(Park).filter(Park.id == req.park_id).first()
    if not park:
        raise HTTPException(status_code=404, detail="园区不存在")

    tools = db.query(Tool).all()
    categories = {c.id: c for c in db.query(Category).all()}

    # Build prompt
    park_info = f"""园区名称: {park.name}
所在城市: {park.city}
园区类型: {park.park_type}
建设类型: {park.build_type}
建设周期: {park.period}
主导产业: {park.industry}
重点方向: {', '.join(park.key_directions) if park.key_directions else '未指定'}
园区描述: {park.description or '无'}
级别: {park.level}"""

    tool_summary = _build_tool_summary(tools, categories)

    system_prompt = """你是一个零碳园区AI工具匹配专家。你的任务是基于园区的产业类型、关键方向和建设周期，从工具库中推荐最合适的AI工具。

请严格按照JSON格式返回结果，不要包含其他文字。返回格式如下：
{
  "match_reasoning": "整体匹配分析，100-150字，说明匹配策略和关键考虑因素",
  "confidence": 0.85,
  "core_recommendations": [
    {"tool_id": 1, "relevance_score": 95, "reasoning": "推荐理由50-80字", "implementation_priority": "immediate"}
  ],
  "general_recommendations": [
    {"tool_id": 2, "relevance_score": 75, "reasoning": "推荐理由50-80字", "implementation_priority": "short_term"}
  ]
}

规则：
- core_recommendations: 3-5个工具，relevance_score >= 80，优先与园区产业类型和关键方向直接匹配
- general_recommendations: 5-8个工具，relevance_score >= 50，补充性的通用工具
- implementation_priority: "immediate"(立即部署), "short_term"(短期规划), "long_term"(长期储备)
- reasoning必须针对具体园区特征，不能是通用模板
- 优先推荐成熟度>=3的工具
- 考虑工具与园区运营环节的匹配度"""

    user_prompt = f"""## 目标园区信息
{park_info}

## 可选AI工具库（共{len(tools)}个工具）
{tool_summary}

## 任务
为上述园区匹配最合适的AI工具，返回JSON格式结果。"""

    # Call LLM or use demo fallback
    if is_configured():
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
            result = chat_json(messages, temperature=0.3, max_tokens=4096)
        except Exception:
            result = {}
    else:
        result = {}

    # Parse result or fall back to rule-based
    if result and "core_recommendations" in result:
        core_recs = []
        for rec in result.get("core_recommendations", [])[:5]:
            tool = db.query(Tool).filter(Tool.id == rec["tool_id"]).first()
            if tool:
                cat = categories.get(tool.category_id)
                core_recs.append(RecommendedTool(
                    tool_id=tool.id,
                    tool_name=tool.name,
                    category_name=cat.name if cat else "",
                    maturity=tool.maturity,
                    relevance_score=rec.get("relevance_score", 80),
                    reasoning=rec.get("reasoning", ""),
                    implementation_priority=rec.get("implementation_priority", "immediate"),
                ))

        general_recs = []
        for rec in result.get("general_recommendations", [])[:8]:
            tool = db.query(Tool).filter(Tool.id == rec["tool_id"]).first()
            if tool:
                cat = categories.get(tool.category_id)
                general_recs.append(RecommendedTool(
                    tool_id=tool.id,
                    tool_name=tool.name,
                    category_name=cat.name if cat else "",
                    maturity=tool.maturity,
                    relevance_score=rec.get("relevance_score", 50),
                    reasoning=rec.get("reasoning", ""),
                    implementation_priority=rec.get("implementation_priority", "short_term"),
                ))

        return AgentMatchResult(
            park=ParkBrief.model_validate(park),
            match_reasoning=result.get("match_reasoning", ""),
            confidence=result.get("confidence", 0.8),
            core_recommendations=core_recs,
            general_recommendations=general_recs,
        )

    # Fallback: use rule-based matching
    from .match import PARK_TYPE_PRIORITY_TOOLS
    priority_ids = PARK_TYPE_PRIORITY_TOOLS.get(park.park_type, [1, 7, 4])
    all_tools_map = {t.id: t for t in tools}

    core_recs = []
    for tid in priority_ids:
        t = all_tools_map.get(tid)
        if t and t.applicable_park_types and park.park_type in t.applicable_park_types:
            cat = categories.get(t.category_id)
            core_recs.append(RecommendedTool(
                tool_id=t.id, tool_name=t.name,
                category_name=cat.name if cat else "",
                maturity=t.maturity,
                relevance_score=90,
                reasoning="基于规则匹配（AI服务未配置，使用默认推荐）",
                implementation_priority="immediate",
            ))
            if len(core_recs) >= 5:
                break

    general_recs = []
    universal_phases = ["电力/能源管理", "建筑用能优化"]
    for t in tools:
        already_in = {r.tool_id for r in core_recs}
        if t.id not in already_in and t.operation_phase in universal_phases and t.maturity >= 4:
            cat = categories.get(t.category_id)
            general_recs.append(RecommendedTool(
                tool_id=t.id, tool_name=t.name,
                category_name=cat.name if cat else "",
                maturity=t.maturity,
                relevance_score=70,
                reasoning="基于规则匹配（通用推荐）",
                implementation_priority="short_term",
            ))
            if len(general_recs) >= 8:
                break

    return AgentMatchResult(
        park=ParkBrief.model_validate(park),
        match_reasoning=f"规则匹配模式（AI API未配置）：园区类型为{park.park_type}，使用预定义优先级列表进行匹配。配置LLM_API_KEY后可启用AI智能匹配。",
        confidence=0.6,
        core_recommendations=core_recs,
        general_recommendations=general_recs,
    )


@router.post("/report")
def agent_report(req: AgentReportRequest, db: Session = Depends(get_db)):
    """AI-powered analysis report generation for a park."""
    park = db.query(Park).filter(Park.id == req.park_id).first()
    if not park:
        raise HTTPException(status_code=404, detail="园区不存在")

    tools = db.query(Tool).all()
    categories = {c.id: c for c in db.query(Category).all()}

    park_info = f"""园区名称: {park.name}
所在城市: {park.city}
园区类型: {park.park_type}
建设类型: {park.build_type}
建设周期: {park.period}
主导产业: {park.industry}
重点方向: {', '.join(park.key_directions) if park.key_directions else '未指定'}
园区描述: {park.description or '无'}
级别: {park.level}"""

    tool_detail = _build_tool_detail(tools, categories)

    # Count tools applicable to this park type
    applicable_count = sum(
        1 for t in tools
        if t.applicable_park_types and park.park_type in t.applicable_park_types
    )

    park_type_peers = {
        "先进制造型": "广州南沙大岗、佛山狮山、惠州惠城、中山翠亨、江门台山",
        "重化工近零碳型": "湛江东海岛、茂名滨海新区",
        "新能源装备制造型": "阳江滨海新区、肇庆大旺",
        "新材料型": "潮州新材料产业园",
        "临港特色产业型": "汕头潮阳、汕尾红海湾",
        "生态高新技术型": "河源高新区、梅州融湾、云浮新兴产业",
    }
    peers = park_type_peers.get(park.park_type, "同类型园区")

    # Phase coverage summary
    phases = {}
    for t in tools:
        if t.operation_phase:
            phases[t.operation_phase] = phases.get(t.operation_phase, 0) + 1
    phase_summary = "\n".join([f"- {k}: {v}个工具" for k, v in sorted(phases.items(), key=lambda x: -x[1])])

    report_title = f"{park.name} — AI赋能零碳转型分析报告"

    if not is_configured():
        # Demo mode — return template-based report
        policies = db.query(Policy).all()
        sections = _generate_demo_report(park, tools, categories, applicable_count, phase_summary, peers, policies)
        return AgentReportResult(
            park=ParkBrief.model_validate(park),
            report_title=report_title,
            generated_at=datetime.now(timezone.utc),
            sections=sections,
        )

    # AI-generated report
    system_prompt = """你是一个资深的零碳园区AI咨询专家，具有以下专业背景：
- 碳核算（Scope 1/2/3）、能源管理、可再生能源集成
- 工业AI应用：预测性维护、工艺优化、数字孪生
- 中国国家和广东省零碳园区政策与标准
- 工业园区运营最佳实践

你的任务是基于提供的园区数据和AI工具库，生成一份专业的分析报告。
使用Markdown格式组织内容。语言专业、精准、可操作。始终使用简体中文。"""

    sections = []

    # Section 1: 园区概况
    s1_prompt = f"""基于以下园区信息，生成结构化的园区概况分析（200-300字）：

{park_info}

内容包含：
1. 园区基本情况（名称、位置、类型、产业）
2. 零碳建设重点方向解读
3. 园区在广东省零碳园区体系中的定位"""
    try:
        s1 = chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": s1_prompt},
        ], temperature=0.5, max_tokens=2048)
        sections.append(ReportSection(title="一、园区概况", level=1, content=s1.strip()))
    except Exception as e:
        sections.append(ReportSection(title="一、园区概况", level=1, content=f"生成失败: {str(e)}"))

    # Section 2: 核心AI工具推荐
    s2_prompt = f"""## 目标园区
{park_info}

## 可选AI工具库（共{len(tools)}个工具）
{tool_detail}

## 任务
为该园区推荐5-8个最核心的AI工具。对每个推荐工具，说明：
- 为什么该工具适合此园区（基于园区类型、产业、关键方向）
- 预期实施效果
- 实施的紧急程度（立即/短期/长期）

按优先级排列，使用Markdown格式。每个工具有清晰的小标题。"""
    try:
        s2 = chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": s2_prompt},
        ], temperature=0.3, max_tokens=4096)
        sections.append(ReportSection(title="二、核心AI工具推荐", level=1, content=s2.strip()))
    except Exception as e:
        sections.append(ReportSection(title="二、核心AI工具推荐", level=1, content=f"生成失败: {str(e)}"))

    # Section 3: 技术缺口分析
    s3_prompt = f"""基于以下信息，进行园区AI赋能差距分析（200-300字）：

## 园区
{park_info}

## AI工具覆盖
- 园区类型: {park.park_type}
- 适用工具数: {applicable_count}/{len(tools)}
- 各运营环节覆盖:
{phase_summary}

## 同类型园区参考
{peers}

分析包含：
1. 当前AI工具覆盖的薄弱环节
2. 相比同类型园区的潜在差距
3. 最需要补足的AI能力方向"""
    try:
        s3 = chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": s3_prompt},
        ], temperature=0.4, max_tokens=2048)
        sections.append(ReportSection(title="三、技术缺口分析", level=1, content=s3.strip()))
    except Exception as e:
        sections.append(ReportSection(title="三、技术缺口分析", level=1, content=f"生成失败: {str(e)}"))

    # Section 4: 实施路线图
    s4_prompt = f"""基于以上分析和推荐，为{park.name}生成分阶段的AI工具实施路线图。

园区信息:
- 建设周期: {park.period}
- 关键方向: {', '.join(park.key_directions) if park.key_directions else '未指定'}

生成三阶段路线图（Markdown格式）：
- 第一阶段：基础建设期（近期，6-12个月）
- 第二阶段：核心部署期（中期，1-2年）
- 第三阶段：优化提升期（远期，2-3年）

每个阶段包含：部署的AI工具、预期里程碑、所需资源和前置条件。"""
    try:
        s4 = chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": s4_prompt},
        ], temperature=0.4, max_tokens=3072)
        sections.append(ReportSection(title="四、实施路线图", level=1, content=s4.strip()))
    except Exception as e:
        sections.append(ReportSection(title="四、实施路线图", level=1, content=f"生成失败: {str(e)}"))

    # Section 5: 总结与建议
    s5_prompt = f"""为{park.name}生成150-200字的总结与建议：

{{
  "park": "{park.name}",
  "type": "{park.park_type}",
  "industry": "{park.industry or ''}",
  "key_directions": {json.dumps(park.key_directions, ensure_ascii=False)}
}}

包含：
1. 核心结论
2. 优先行动建议（2-3条具体建议）
3. 风险提示"""
    try:
        s5 = chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": s5_prompt},
        ], temperature=0.4, max_tokens=2048)
        sections.append(ReportSection(title="五、总结与建议", level=1, content=s5.strip()))
    except Exception as e:
        sections.append(ReportSection(title="五、总结与建议", level=1, content=f"生成失败: {str(e)}"))

    return AgentReportResult(
        park=ParkBrief.model_validate(park),
        report_title=report_title,
        generated_at=datetime.now(timezone.utc),
        sections=sections,
    )


def _generate_demo_report(park, tools, categories, applicable_count, phase_summary, peers, policies):
    """Generate a data-rich template report when LLM is not configured."""
    applicable_tools = [t for t in tools if t.applicable_park_types and park.park_type in t.applicable_park_types]
    top_tools = sorted(applicable_tools, key=lambda t: t.maturity, reverse=True)[:8]

    # ---- 工具库整体统计 ----
    maturity_dist = {}
    for t in tools:
        maturity_dist[t.maturity] = maturity_dist.get(t.maturity, 0) + 1
    maturity_str = '、'.join(f"{k}星 {v}个" for k, v in sorted(maturity_dist.items(), reverse=True))

    category_dist = {}
    for t in tools:
        cat = categories.get(t.category_id)
        cat_name = cat.name if cat else '未分类'
        category_dist[cat_name] = category_dist.get(cat_name, 0) + 1
    category_str = '、'.join(f"{k} {v}个" for k, v in sorted(category_dist.items(), key=lambda x: -x[1]))

    total_cases = sum(t.case_count or 0 for t in tools)

    # ---- 园区字段 ----
    key_dirs = '、'.join(park.key_directions) if park.key_directions else '低碳发展'
    energy = park.energy_profile or '暂无能耗特征数据'
    carbon = park.carbon_structure or '暂无碳排结构数据'
    challenges = park.core_challenges or '暂无核心挑战数据'
    challenge_list = [c.strip() for c in (park.core_challenges or '').replace('，', '、').replace(',', '、').split('、') if c.strip()]

    primary = getattr(park, 'park_type_primary', None)
    secondary = getattr(park, 'park_type_secondary', None)
    park_type_full = f"{primary} · {secondary}" if primary and secondary else (primary or park.park_type)

    # ---- 路线图工具分层 ----
    phase1_tools = [t for t in applicable_tools if t.maturity >= 4 and t.operation_phase in ('电力/能源管理', '建筑用能优化')]
    phase2_tools = [t for t in applicable_tools if t.maturity >= 4 and t.operation_phase in ('设备运维管理', '碳核算与交易', '交通物流')]
    phase3_tools = [t for t in applicable_tools if t.maturity < 4]

    def _names(ts, limit=5):
        return '、'.join(t.name for t in ts[:limit]) or '（按园区产业特征动态选型）'

    mature_tool_names = '、'.join(t.name for t in applicable_tools if t.maturity >= 4) or '电力负荷预测、暖通空调节能控制'

    # ---- 政策引用 ----
    policy_topics = ('零碳园区', '碳市场', '碳核算', '碳关税')
    relevant = [p for p in policies if p.topic in policy_topics]
    relevant.sort(key=lambda p: 0 if p.topic == '零碳园区' else 1)
    policy_lines = '\n'.join(
        f"- **{p.title}**（{p.issuing_body}，{p.publish_date}）" for p in relevant[:5]
    )

    sections = []

    # ===== Section 1 园区概况 =====
    sections.append(ReportSection(title="一、园区概况", level=1, content=f"""
**{park.name}** 位于广东省{park.city}市，属于**{park_type_full}**园区，建设类型为{park.build_type}，建设周期为{park.period}，园区级别为{park.level}。

**主导产业**: {park.industry or '未指定'}

**零碳建设重点方向**: {key_dirs}

### 能耗特征
{energy}

### 碳排放结构
{carbon}

### 核心挑战
{challenges}

该园区是广东省首批15个省级零碳园区之一，在{park.park_type}类别中具有代表性地位。其零碳转型路径围绕{key_dirs}展开，是区域内产业绿色升级的重要载体。

> 💡 **提示**: 当前为Demo模式，报告内容基于平台数据库实时聚合生成。配置 `LLM_API_KEY` 后可启用AI生成的专业分析报告。
"""))

    # ===== Section 2 核心AI工具推荐 =====
    tool_list = ""
    for t in top_tools[:6]:
        cat = categories.get(t.category_id)
        cat_name = cat.name if cat else '未分类'
        value = t.value_props[0] if t.value_props else '提升运营效率'
        pre = t.prerequisites or '需接入园区实时数据'
        ai_method = t.ai_method or '未指定'
        stars = '★' * t.maturity + '☆' * (5 - t.maturity)
        case_note = ""
        cases = getattr(t, 'cases', None) or []
        if cases:
            c = cases[0]
            case_note = f"- **落地案例**: {c.platform_name} — {c.effect}"
        tool_list += f"""
### {t.name}
- **分类**: {cat_name} | **成熟度**: {stars} ({t.maturity}/5) | **运营环节**: {t.operation_phase or '未指定'}
- **应用场景**: {t.scenario or '未指定'}
- **AI方法**: {ai_method}
- **预期效果**: {value}
- **实施前提**: {pre}
{case_note}
"""
    sections.append(ReportSection(title="二、核心AI工具推荐", level=1, content=f"""
基于园区类型（{park.park_type}）和关键方向，平台从 **{len(tools)}** 个AI工具中筛出 **{applicable_count}** 个适用工具，按成熟度与匹配度推荐以下核心工具：

{tool_list}
> **推荐逻辑**: 优先成熟度≥4的工具（已在真实园区验证），兼顾{park.park_type}园区的产业特征与{key_dirs}方向。
"""))

    # ===== Section 3 技术缺口分析 =====
    challenge_gap = '\n'.join(f"{i}. **{c}**" for i, c in enumerate(challenge_list[:5], 1)) or "暂无"
    sections.append(ReportSection(title="三、技术缺口分析", level=1, content=f"""
### 工具库覆盖现状
- 园区类型 **{park.park_type}** 共有 **{applicable_count}** 个适用工具（覆盖率 {applicable_count}/{len(tools)}）
- **成熟度分布**: {maturity_str}
- **分类分布**: {category_str}
- **累计落地案例**: {total_cases} 个

### 各运营环节覆盖
{phase_summary}

### 核心短板（对应园区挑战）
{challenge_gap}

### 同类型园区参考
{peers}

> 💡 **提示**: 当前为Demo模式分析。AI模式下将基于LLM推理生成更精准的个性化缺口分析。
"""))

    # ===== Section 4 实施路线图 =====
    sections.append(ReportSection(title="四、实施路线图", level=1, content=f"""
结合园区建设周期（{park.period}）与核心挑战，建议按三阶段有序推进：

### 第一阶段：基础建设期（近期，6-12个月）
- **数据基础**: 部署IoT传感器与能源监测系统，建立分环节、分设备的能耗数据采集体系
- **能源与建筑节能（高成熟度工具）**: {_names(phase1_tools)}
- **预期里程碑**: 数据采集覆盖率≥80%，实现能耗实时可视化与精准负荷预测

### 第二阶段：核心部署期（中期，1-2年）
- **设备运维与碳管理（高成熟度工具）**: {_names(phase2_tools)}
- **储能与多能流协同**: 基于负荷与新能源出力预测，优化储能充放电与冷热电多能调度
- **预期里程碑**: 综合能效提升15%以上，碳排放强度下降10%，关键设备故障预警覆盖

### 第三阶段：优化提升期（远期，2-3年）
- **前沿与创新工具（低成熟度）**: {_names(phase3_tools)}
- **零碳路径闭环**: 基于情景模拟优化零碳路径，向供应链上下游延伸碳足迹管理
- **预期里程碑**: 达成零碳园区核心指标，形成可复制推广的园区级零碳模式

> 💡 **提示**: 当前为Demo模式路线图。AI模式下将基于园区实际参数生成更精准的分阶段实施方案。
"""))

    # ===== Section 5 总结与建议 =====
    sections.append(ReportSection(title="五、总结与建议", level=1, content=f"""
### 核心结论
{park.name}作为广东省{park.park_type}零碳园区的代表，具有良好的产业基础和政策支持。通过系统性部署AI工具，可在能效提升、碳排放管理和运营优化方面取得显著成效。园区碳排结构为「{carbon}」，AI赋能的关键在于源-网-荷-储协同与分环节能效精细化管理。

### 政策依据
{policy_lines}

### 优先行动建议
1. **立即启动数据基础设施建设**: 高质量数据是所有AI工具的前提，建议优先部署IoT监测和数据采集系统
2. **从成熟工具入手**: 优先部署成熟度≥4的工具（{mature_tool_names}），快速见效建立信心
3. **对标政策要求**: 紧抓零碳园区国标（GB/T 51100-2026）与广东省零碳园区建设名单要求，建立可量化、可追溯的碳管理体系

### 风险提示
- AI工具的实施效果依赖于数据质量和运维能力
- 部分前沿工具（如CCUS、零碳路径模拟）成熟度较低，建议保持关注但谨慎投入
- 建议与同类型园区（{peers}）建立交流机制，共享经验和最佳实践

> 💡 **提示**: 当前为Demo模式。配置 `LLM_API_KEY` 后可获得AI生成的专业分析报告。详见 `.env.example`。
"""))

    return sections
