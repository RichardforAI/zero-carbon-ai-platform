"""Tools API — sync."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_
import math, json, re

from ..database import get_db
from ..models import Tool, Case, Category, Supplier
from ..schemas import ToolBrief, ToolDetail, PaginatedResponse, CaseOut, SupplierOut, ToolCreate, ToolUpdate, AIGenerateRequest
from ..services.llm_service import chat_json, is_configured

router = APIRouter(prefix="/api/tools", tags=["tools"])


@router.get("")
def list_tools(
    category_id: int = Query(None),
    park_type: str = Query(None),
    park_type_primary: str = Query(None),     # NEW: 一级分类
    park_type_secondary: str = Query(None),   # NEW: 二级分类
    scene_tag: str = Query(None),
    operation_phase: str = Query(None),
    maturity_min: int = Query(None),
    maturity_max: int = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(Tool)

    if category_id:
        query = query.filter(Tool.category_id == category_id)
    if park_type:
        # SQLite JSON: filter in Python after query
        pass  # handled below
    if operation_phase:
        query = query.filter(Tool.operation_phase == operation_phase)
    if maturity_min is not None:
        query = query.filter(Tool.maturity >= maturity_min)
    if maturity_max is not None:
        query = query.filter(Tool.maturity <= maturity_max)
    if search:
        search_filter = or_(
            Tool.name.contains(search),
            Tool.description.contains(search),
            Tool.scenario.contains(search),
        )
        query = query.filter(search_filter)

    # Get results
    all_results = query.order_by(Tool.maturity.desc()).all()

    # Map new classification to old park_type values for filtering
    if park_type_primary or park_type_secondary:
        from ..models import Park
        park_query = db.query(Park)
        if park_type_primary:
            park_query = park_query.filter(Park.park_type_primary == park_type_primary)
        if park_type_secondary:
            park_query = park_query.filter(Park.park_type_secondary == park_type_secondary)
        mapped_old_types = list(set(p.park_type for p in park_query.all() if p.park_type))
        # Filter tools that apply to any of the mapped old park types
        if mapped_old_types:
            all_results = [
                t for t in all_results
                if t.applicable_park_types and any(pt in t.applicable_park_types for pt in mapped_old_types)
            ]

    # Filter by park_type in Python (SQLite JSON workaround)
    if park_type:
        all_results = [t for t in all_results if t.applicable_park_types and park_type in t.applicable_park_types]

    # Filter by scene_tag in Python
    if scene_tag:
        all_results = [t for t in all_results if t.scene_tags and scene_tag in t.scene_tags]

    total = len(all_results)
    offset = (page - 1) * page_size
    page_items = all_results[offset:offset + page_size]

    items = []
    for t in page_items:
        cat = db.query(Tool.category_ref).first() if False else None
        items.append(ToolBrief(
            id=t.id, name=t.name,
            category_name=t.category_ref.name if t.category_ref else None,
            maturity=t.maturity,
            applicable_park_types=t.applicable_park_types,
            scene_tags=t.scene_tags or [],
            operation_phase=t.operation_phase,
            case_count=t.case_count,
        ))

    return PaginatedResponse(
        items=items, total=total, page=page, page_size=page_size,
        total_pages=math.ceil(total / page_size) if total > 0 else 0,
    )


@router.get("/{tool_id}")
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    cases = db.query(Case).filter(Case.tool_id == tool_id).all()
    suppliers = db.query(Supplier).filter(Supplier.tool_id == tool_id).all()

    return ToolDetail(
        id=tool.id, name=tool.name,
        category_name=tool.category_ref.name if tool.category_ref else None,
        category_id=tool.category_id, maturity=tool.maturity,
        description=tool.description, scenario=tool.scenario,
        ai_method=tool.ai_method, tech_path=tool.tech_path,
        value_props=tool.value_props, prerequisites=tool.prerequisites,
        implementation_tips=tool.implementation_tips,
        operation_phase=tool.operation_phase,
        applicable_park_types=tool.applicable_park_types,
        scene_tags=tool.scene_tags or [],
        case_count=tool.case_count, version=tool.version,
        updated_at=tool.updated_at,
        cases=[CaseOut.model_validate(c) for c in cases],
        suppliers=[SupplierOut.model_validate(s) for s in suppliers],
    )


# === CRUD endpoints ===

@router.post("")
def create_tool(data: ToolCreate, db: Session = Depends(get_db)):
    """Create a new AI tool."""
    tool = Tool(
        name=data.name, category_id=data.category_id, maturity=data.maturity,
        description=data.description, scenario=data.scenario,
        ai_method=data.ai_method, tech_path=data.tech_path or [],
        value_props=data.value_props or [], prerequisites=data.prerequisites,
        implementation_tips=data.implementation_tips,
        operation_phase=data.operation_phase,
        applicable_park_types=data.applicable_park_types or [],
        scene_tags=data.scene_tags or [],
        case_count=data.case_count, version=data.version,
        updated_at=datetime.now(timezone.utc),
    )
    db.add(tool)
    db.commit()
    db.refresh(tool)
    return {"status": "ok", "id": tool.id, "name": tool.name}


@router.put("/{tool_id}")
def update_tool(tool_id: int, data: ToolUpdate, db: Session = Depends(get_db)):
    """Update an existing AI tool."""
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tool, key, value)
    tool.updated_at = datetime.now(timezone.utc)
    db.commit()
    return {"status": "ok", "id": tool.id, "name": tool.name}


@router.delete("/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    """Delete an AI tool."""
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    db.delete(tool)
    db.commit()
    return {"status": "ok", "deleted_id": tool_id}


@router.post("/ai-generate")
def ai_generate_tool(data: AIGenerateRequest, db: Session = Depends(get_db)):
    """Use LLM to auto-fill tool fields from name + brief description."""
    if not is_configured():
        raise HTTPException(status_code=501, detail="LLM API未配置，请设置LLM_API_KEY")

    categories = [c.name for c in db.query(Category).all()]
    cat_list = ", ".join(categories)

    prompt = f"""你是一个零碳园区AI工具专家。请基于用户输入的工具名称和简要描述，生成完整的工具信息。

工具名称: {data.name}
简要描述: {data.brief_description}

可选的分类: {cat_list}

请严格按照JSON格式返回：
{{
  "category_name": "预测类",
  "maturity": 4,
  "description": "150-200字的工具详细描述",
  "scenario": "100-150字的适用场景描述",
  "ai_method": "100-150字的AI赋能方式描述",
  "tech_path": ["技术路径1", "技术路径2", "技术路径3"],
  "value_props": ["量化价值1", "量化价值2", "量化价值3"],
  "prerequisites": "50-100字的前置条件与数据要求",
  "implementation_tips": "50-100字的实施建议",
  "operation_phase": "电力/能源管理",
  "applicable_park_types": ["先进制造型", "重化工近零碳型"],
  "scene_tags": ["建筑运行", "能源管理"]
}}

规则：
- maturity取值1-5，基于技术就绪度判断
- tech_path列出3-5个具体算法/技术
- value_props列出3-4条量化价值，含具体数字
- applicable_park_types从以下选择：["先进制造型","重化工近零碳型","新能源装备制造型","新材料型","临港特色产业型","生态高新技术型"]
- operation_phase选择合适的运营环节
- 所有描述使用中文"""

    try:
        result = chat_json([
            {"role": "system", "content": "你是一个专业的零碳园区AI工具信息生成专家。返回纯JSON，不要包含markdown代码块。"},
            {"role": "user", "content": prompt},
        ], temperature=0.4, max_tokens=2048)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM调用失败: {str(e)}")

    if not result:
        raise HTTPException(status_code=500, detail="LLM返回格式异常")

    # Map category name to ID
    cat_name = result.get("category_name", "预测类")
    category = db.query(Category).filter(Category.name == cat_name).first()
    category_id = category.id if category else 1

    return {
        "name": data.name,
        "category_id": category_id,
        "category_name": cat_name,
        "maturity": result.get("maturity", 3),
        "description": result.get("description", ""),
        "scenario": result.get("scenario", ""),
        "ai_method": result.get("ai_method", ""),
        "tech_path": result.get("tech_path", []),
        "value_props": result.get("value_props", []),
        "prerequisites": result.get("prerequisites", ""),
        "implementation_tips": result.get("implementation_tips", ""),
        "operation_phase": result.get("operation_phase", ""),
        "applicable_park_types": result.get("applicable_park_types", []),
        "scene_tags": result.get("scene_tags", []),
        "case_count": 0,
        "version": "1.0",
    }
