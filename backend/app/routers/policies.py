"""Policy API — sync."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import Policy
from ..schemas import PolicyBrief, PolicySource

router = APIRouter(prefix="/api/policies", tags=["policies"])

# Policy sources
POLICY_SOURCES = [
    {"name": "欧盟EU ETS官网", "url": "https://climate.ec.europa.eu/eu-action/carbon-markets/about-eu-ets_en", "description": "欧盟碳排放交易体系官方信息"},
    {"name": "欧盟CBAM官网", "url": "https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry-and-reporting_en", "description": "欧盟碳边境调节机制官方信息"},
    {"name": "IMO绿色航运", "url": "https://www.imo.org/en/OurWork/Environment/Pages/2023-IMO-Strategy-on-Reduction-of-GHG-Emissions-from-Ships.aspx", "description": "国际海事组织船舶温室气体减排"},
    {"name": "全国碳市场信息网", "url": "https://www.cets.org.cn/", "description": "生态环境部应对气候变化司主管，全国碳市场信息发布"},
    {"name": "生态环境部(MEE)", "url": "https://www.mee.gov.cn", "description": "中国生态环境部官方网站"},
    {"name": "中国政府网", "url": "https://www.gov.cn", "description": "国务院政策文件发布平台"},
    {"name": "广东省发改委", "url": "https://drc.gd.gov.cn", "description": "广东省发展和改革委员会"},
]


@router.get("/sources")
def list_sources():
    """Return all policy source websites."""
    return [
        PolicySource(name=s["name"], url=s["url"], description=s["description"])
        for s in POLICY_SOURCES
    ]


@router.get("")
def list_policies(
    category: str | None = Query(None, description="国际/国家/地方/行业标准"),
    topic: str | None = Query(None, description="碳市场/碳关税/零碳园区/碳核算/绿色航运/能源转型"),
    search: str | None = Query(None, description="关键词搜索标题和摘要"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """List policies with filtering, search, and pagination."""
    query = db.query(Policy)

    if category:
        query = query.filter(Policy.category == category)
    if topic:
        query = query.filter(Policy.topic == topic)
    if search:
        like = f"%{search}%"
        query = query.filter(
            (Policy.title.contains(search)) | (Policy.summary.contains(search))
        )

    total = query.count()
    total_pages = max(1, (total + page_size - 1) // page_size)
    items = query.order_by(Policy.publish_date.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": [PolicyBrief.model_validate(p) for p in items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@router.get("/{policy_id}")
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    """Get a single policy by ID."""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="政策未找到")
    return PolicyBrief.model_validate(policy)
