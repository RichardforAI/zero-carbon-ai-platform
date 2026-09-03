"""News API — sync."""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import News
from ..schemas import NewsBrief

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("")
def list_news(
    category: str | None = Query(None, description="AI+双碳/AI+能源/AI+零碳园区/AI+碳市场/国际动态"),
    topic: str | None = Query(None, description="技术突破/政策解读/行业应用/企业动态/研究报告"),
    search: str | None = Query(None, description="关键词搜索标题和摘要"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """List news with filtering, search, and pagination."""
    query = db.query(News)

    if category:
        query = query.filter(News.category == category)
    if topic:
        query = query.filter(News.topic == topic)
    if search:
        query = query.filter(
            (News.title.contains(search)) | (News.summary.contains(search))
        )

    total = query.count()
    total_pages = max(1, (total + page_size - 1) // page_size)
    items = query.order_by(News.publish_date.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": [NewsBrief.model_validate(n) for n in items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@router.get("/{news_id}")
def get_news(news_id: int, db: Session = Depends(get_db)):
    """Get a single news item by ID."""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="新闻未找到")
    return NewsBrief.model_validate(news)
