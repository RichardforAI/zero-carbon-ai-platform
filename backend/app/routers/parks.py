"""Parks API — sync."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from ..database import get_db
from ..models import Park
from ..schemas import ParkBrief, ParkDetail

router = APIRouter(prefix="/api/parks", tags=["parks"])


@router.get("")
def list_parks(
    park_type_primary: str | None = Query(None, description="一级分类筛选"),
    park_type_secondary: str | None = Query(None, description="二级分类筛选"),
    db: Session = Depends(get_db),
):
    query = db.query(Park)
    if park_type_primary:
        query = query.filter(Park.park_type_primary == park_type_primary)
    if park_type_secondary:
        query = query.filter(Park.park_type_secondary == park_type_secondary)
    parks = query.order_by(Park.id).all()
    return [ParkBrief.model_validate(p) for p in parks]


@router.get("/types")
def list_park_types(db: Session = Depends(get_db)):
    """Return all unique park type classifications (一级+二级)."""
    primary_types = [
        row[0] for row in
        db.query(distinct(Park.park_type_primary)).filter(Park.park_type_primary.isnot(None)).all()
    ]
    secondary_types = [
        row[0] for row in
        db.query(distinct(Park.park_type_secondary)).filter(Park.park_type_secondary.isnot(None)).all()
    ]

    # Build hierarchy
    hierarchy = [
        {
            "primary": "工业园区",
            "secondary": ["重化工", "装备制造", "电子信息"],
            "count": db.query(Park).filter(Park.park_type_primary == "工业园区").count(),
        },
        {
            "primary": "公建园区",
            "secondary": ["政务中心", "商务楼宇", "医院", "学校"],
            "count": db.query(Park).filter(Park.park_type_primary == "公建园区").count(),
        },
        {
            "primary": "高新园区",
            "secondary": ["科技园", "孵化器", "数据中心集群"],
            "count": db.query(Park).filter(Park.park_type_primary == "高新园区").count(),
        },
        {
            "primary": "物流/农业园区",
            "secondary": ["仓储物流中心", "现代农业产业园"],
            "count": db.query(Park).filter(Park.park_type_primary == "物流/农业园区").count(),
        },
    ]
    return {
        "primary_types": primary_types,
        "secondary_types": secondary_types,
        "hierarchy": hierarchy,
    }


@router.get("/{park_id}")
def get_park(park_id: int, db: Session = Depends(get_db)):
    park = db.query(Park).filter(Park.id == park_id).first()
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")
    return ParkDetail.model_validate(park)
