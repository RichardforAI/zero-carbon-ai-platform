"""Match API — sync."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Park, Tool
from ..schemas import MatchResult, ParkBrief, ToolBrief

router = APIRouter(prefix="/api/match", tags=["match"])

PARK_TYPE_PRIORITY_TOOLS = {
    "先进制造型": [1, 7, 4, 9, 11, 8, 15, 20],
    "重化工近零碳型": [6, 19, 4, 1, 9, 11, 13, 20],
    "新能源装备制造型": [3, 1, 4, 9, 15, 11, 7, 20],
    "新材料型": [4, 7, 9, 11, 12, 13, 8, 20],
    "临港特色产业型": [16, 15, 1, 4, 7, 8, 11, 20],
    "生态高新技术型": [14, 7, 2, 1, 4, 11, 8, 20],
}


@router.get("")
def match_tools(park_id: int = Query(...), db: Session = Depends(get_db)):
    park = db.query(Park).filter(Park.id == park_id).first()
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")

    park_brief = ParkBrief.model_validate(park)

    priority_ids = PARK_TYPE_PRIORITY_TOOLS.get(park.park_type, [1, 7, 4])

    all_tools = {t.id: t for t in db.query(Tool).all()}

    def to_brief(t):
        return ToolBrief(
            id=t.id, name=t.name,
            category_name=t.category_ref.name if t.category_ref else None,
            maturity=t.maturity,
            applicable_park_types=t.applicable_park_types,
            operation_phase=t.operation_phase,
            case_count=t.case_count,
        )

    core = []
    for tid in priority_ids:
        if tid in all_tools:
            t = all_tools[tid]
            if t.applicable_park_types and park.park_type in t.applicable_park_types:
                core.append(to_brief(t))
                if len(core) >= 5:
                    break

    core_ids = {t.id for t in core}
    universal_phases = ["电力/能源管理", "建筑用能优化"]
    general = []
    for t in all_tools.values():
        if t.id not in core_ids and t.operation_phase in universal_phases and t.maturity >= 4:
            general.append(to_brief(t))
            if len(general) >= 8:
                break

    return MatchResult(park=park_brief, core_recommendations=core, general_recommendations=general)
