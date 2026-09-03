"""AI Agent API — LLM-powered matching and report generation."""
import json
import re
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Park, Tool, Category
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
        sections = _generate_demo_report(park, tools, categories, applicable_count, phase_summary, peers)
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


def _generate_demo_report(park, tools, categories, applicable_count, phase_summary, peers):
    """Generate a template-based demo report when LLM is not configured."""
    applicable_tools = [t for t in tools if t.applicable_park_types and park.park_type in t.applicable_park_types]
    top_tools = sorted(applicable_tools, key=lambda t: t.maturity, reverse=True)[:8]

    sections = []

    # Section 1
    sections.append(ReportSection(title="一、园区概况", level=1, content=f"""
**{park.name}** 位于广东省{park.city}市，属于**{park.park_type}**园区，建设类型为{park.build_type}，建设周期为{park.period}。

**主导产业**: {park.industry or '未指定'}

**零碳建设重点方向**: {', '.join(park.key_directions) if park.key_directions else '未指定'}

该园区是广东省首批15个省级零碳园区之一，在{park.park_type}类别中具有代表性地位。其零碳转型路径围绕{'、'.join(park.key_directions) if park.key_directions else '低碳发展'}展开，是区域内产业绿色升级的重要载体。

> 💡 **提示**: 当前为Demo模式，报告内容基于模板生成。配置 `LLM_API_KEY` 后可启用AI生成的专业分析报告。
"""))

    # Section 2
    tool_list = ""
    for t in top_tools[:6]:
        cat = categories.get(t.category_id)
        tool_list += f"""
### {t.name}
- **分类**: {cat.name if cat else '未分类'} | **成熟度**: {'★' * t.maturity}{'☆' * (5 - t.maturity)}
- **应用场景**: {t.scenario or '未指定'}
- **预期效果**: {t.value_props[0] if t.value_props else '提升运营效率'}
- **推荐理由**: 该工具适用于{park.park_type}园区，与园区{'、'.join(park.key_directions) if park.key_directions else '零碳建设'}方向高度匹配。
"""
    sections.append(ReportSection(title="二、核心AI工具推荐", level=1, content=f"""
基于园区类型（{park.park_type}）和关键方向，推荐以下核心AI工具：

{tool_list}
"""))

    # Section 3
    sections.append(ReportSection(title="三、技术缺口分析", level=1, content=f"""
### 当前覆盖情况
- 园区类型 **{park.park_type}** 共有 **{applicable_count}** 个适用工具
- 工具库总计 {len(tools)} 个工具，覆盖 {applicable_count}/{len(tools)}

### 各运营环节覆盖
{phase_summary}

### 同类型园区参考
{peers}

### 主要缺口
1. **数据基础设施**: 多数AI工具需要高质量历史数据支撑，园区需优先完善数据采集体系
2. **人才储备**: AI工具的运维和调优需要专业技术团队
3. **系统集成**: 各AI工具间的数据互通和协同优化需要统一平台支撑

> 💡 **提示**: 当前为Demo模式分析。AI模式下将基于LLM推理生成更精准的个性化缺口分析。
"""))

    # Section 4
    sections.append(ReportSection(title="四、实施路线图", level=1, content=f"""
### 第一阶段：基础建设期（近期，6-12个月）
- **数据采集体系**: 部署IoT传感器和能源监测系统，建立数据基础
- **电力负荷预测**: 部署ID:1工具，建立精准负荷预测能力
- **暖通空调节能**: 在主要建筑部署AI节能控制系统
- **预期里程碑**: 完成数据采集覆盖率80%，实现能耗数据实时监控

### 第二阶段：核心部署期（中期，1-2年）
- **碳足迹核算**: 建立Scope 1/2碳排放核算体系
- **储能优化**: 根据负荷预测结果部署储能充放电优化
- **设备运维**: 关键设备接入故障预警系统
- **预期里程碑**: 综合能效提升15%，碳排放强度下降10%

### 第三阶段：优化提升期（远期，2-3年）
- **多能流协同**: 实现电、冷、热多能互补优化调度
- **零碳路径模拟**: 基于系统动力学进行多情景对比分析
- **供应链碳管理**: 向上下游延伸碳足迹管理
- **预期里程碑**: 达成零碳园区核心指标，形成可复制推广模式

> 💡 **提示**: 当前为Demo模式路线图。AI模式下将基于园区实际参数生成更精准的分阶段实施方案。
"""))

    # Section 5
    sections.append(ReportSection(title="五、总结与建议", level=1, content=f"""
### 核心结论
{park.name}作为广东省{park.park_type}零碳园区的代表，具有良好的产业基础和政策支持。通过系统性部署AI工具，可在能效提升、碳排放管理和运营优化方面取得显著成效。

### 优先行动建议
1. **立即启动数据基础设施建设**: 高质量数据是所有AI工具的前提，建议优先部署IoT监测和数据采集系统
2. **从成熟工具入手**: 优先部署成熟度≥4的工具（如电力负荷预测、暖通空调节能控制），快速见效建立信心
3. **制定分阶段实施计划**: 按照"基础建设→核心部署→优化提升"三阶段有序推进，避免资源分散

### 风险提示
- AI工具的实施效果依赖于数据质量和运维能力
- 部分前沿工具（如CCUS、零碳路径模拟）成熟度较低，建议保持关注但谨慎投入
- 建议与同类型园区（{peers}）建立交流机制，共享经验和最佳实践

> 💡 **提示**: 当前为Demo模式。配置 `LLM_API_KEY` 后可获得AI生成的专业分析报告。详见 `.env.example`。
"""))

    return sections
