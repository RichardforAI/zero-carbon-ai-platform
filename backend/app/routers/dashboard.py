"""Dashboard API — sync."""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import Tool, Category, UpdateLog, Park, Case
from ..schemas import (
    DashboardData, DashboardKPI, CategoryDistribution,
    ParkTypeCoverage, MaturityRadar, UpdateLogOut,
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

PRIMARY_PARK_TYPES = ["工业园区", "公建园区", "高新园区", "物流/农业园区"]


@router.get("")
def get_dashboard(db: Session = Depends(get_db)):
    all_tools = db.query(Tool).all()
    all_parks = db.query(Park).all()
    all_cases = db.query(Case).all()
    total_tools = len(all_tools)

    # Category distribution
    cats = db.query(Category).order_by(Category.id).all()
    category_distribution = []
    for cat in cats:
        count = sum(1 for t in all_tools if t.category_id == cat.id)
        category_distribution.append(CategoryDistribution(
            name=cat.name, name_en=cat.name_en, color=cat.color, count=count,
        ))

    # Unique operation phases (dynamic from actual data)
    unique_phases = set(t.operation_phase for t in all_tools if t.operation_phase)

    # Unique primary park types from parks table
    unique_park_types = set(p.park_type_primary for p in all_parks if p.park_type_primary)

    # New this month
    now = datetime.now(timezone.utc)
    month_ago = now - timedelta(days=30)
    new_this_month = 0
    for t in all_tools:
        if t.created_at:
            ct = t.created_at if t.created_at.tzinfo else t.created_at.replace(tzinfo=timezone.utc)
            if ct >= month_ago:
                new_this_month += 1

    # Total cases (dynamic)
    total_cases = len(all_cases)

    # Park type coverage — use new primary types
    park_coverage = []
    for pt in PRIMARY_PARK_TYPES:
        pt_parks = [p for p in all_parks if p.park_type_primary == pt]
        if not pt_parks:
            continue
        # Get old park_type values to match tools
        old_types = set(p.park_type for p in pt_parks if p.park_type)
        pt_tools = [t for t in all_tools if t.applicable_park_types and any(ot in t.applicable_park_types for ot in old_types)]
        high = sum(1 for t in pt_tools if t.maturity >= 4)
        med = sum(1 for t in pt_tools if 2 <= t.maturity < 4)
        low = sum(1 for t in pt_tools if t.maturity < 2)
        park_coverage.append(ParkTypeCoverage(
            park_type=pt, high_maturity=high, medium_maturity=med, low_maturity=low,
        ))

    # Maturity radar — use actual phases from data
    top_phases = sorted(unique_phases)
    maturity_radar = []
    for phase in top_phases:
        phase_tools = [t for t in all_tools if t.operation_phase == phase]
        avg = sum(t.maturity for t in phase_tools) / len(phase_tools) if phase_tools else 0
        maturity_radar.append(MaturityRadar(phase=phase, avg_maturity=round(avg, 1)))

    # Building scene stats
    building_tools = [t for t in all_tools if t.scene_tags and "建筑运行" in t.scene_tags]
    building_phases = set(t.operation_phase for t in building_tools if t.operation_phase)
    building_scene_stats = {
        "tool_count": len(building_tools),
        "phases": list(building_phases),
        "phase_count": len(building_phases),
        "case_count": sum(t.case_count for t in building_tools),
        "category_distribution": [
            {"name": cat.name, "count": sum(1 for t in building_tools if t.category_id == cat.id), "color": cat.color}
            for cat in cats if any(t.category_id == cat.id for t in building_tools)
        ]
    }

    # Recent updates
    updates = db.query(UpdateLog).order_by(UpdateLog.created_at.desc()).limit(5).all()

    # Last updated timestamp (latest update log)
    last_updated = None
    latest_log = db.query(UpdateLog).order_by(UpdateLog.created_at.desc()).first()
    if latest_log and latest_log.created_at:
        last_updated = latest_log.created_at.strftime("%Y-%m-%d %H:%M")

    return DashboardData(
        kpi=DashboardKPI(
            total_tools=total_tools,
            total_scenarios=len(unique_phases),
            total_cases=total_cases,
            park_types_covered=len(unique_park_types),
            operation_phases_covered=len(unique_phases),
            new_this_month=new_this_month,
        ),
        category_distribution=category_distribution,
        park_type_coverage=park_coverage,
        maturity_radar=maturity_radar,
        building_scene_stats=building_scene_stats,
        last_updated=last_updated,
        recent_updates=[UpdateLogOut.model_validate(u) for u in updates],
    )
