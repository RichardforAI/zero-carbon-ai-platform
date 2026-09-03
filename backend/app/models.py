"""SQLAlchemy ORM models — synchronous."""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from .database import Base

tool_park_association = Table(
    "tool_park_association",
    Base.metadata,
    Column("tool_id", Integer, ForeignKey("tools.id"), primary_key=True),
    Column("park_id", Integer, ForeignKey("parks.id"), primary_key=True),
)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    name_en = Column(String(100))
    description = Column(Text)
    icon = Column(String(10))
    color = Column(String(10))
    tools = relationship("Tool", back_populates="category_ref")


class Tool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    maturity = Column(Integer, default=3)
    description = Column(Text)
    scenario = Column(Text)
    ai_method = Column(Text)
    tech_path = Column(JSON, default=list)
    value_props = Column(JSON, default=list)
    prerequisites = Column(Text)
    implementation_tips = Column(Text)
    operation_phase = Column(String(100))
    applicable_park_types = Column(JSON, default=list)
    scene_tags = Column(JSON, default=list)  # e.g. ["建筑运行", "能源管理", "交通物流"]
    case_count = Column(Integer, default=0)
    version = Column(String(20), default="1.0")
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    category_ref = relationship("Category", back_populates="tools")
    cases = relationship("Case", back_populates="tool_ref", cascade="all, delete-orphan")
    parks = relationship("Park", secondary=tool_park_association, back_populates="tools")
    suppliers = relationship("Supplier", back_populates="tool_ref", cascade="all, delete-orphan")


class Park(Base):
    __tablename__ = "parks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    city = Column(String(100))
    province = Column(String(50), default="广东省")
    park_type = Column(String(100))              # 保留兼容旧数据
    park_type_primary = Column(String(100))       # NEW: 一级分类
    park_type_secondary = Column(String(100))     # NEW: 二级分类
    build_type = Column(String(50))
    period = Column(String(50))
    industry = Column(String(200))
    key_directions = Column(JSON, default=list)
    energy_profile = Column(Text)                 # NEW: 能耗特征
    carbon_structure = Column(Text)               # NEW: 主要碳排结构
    core_challenges = Column(Text)                # NEW: 核心挑战
    description = Column(Text)
    level = Column(String(20), default="省级")
    tools = relationship("Tool", secondary=tool_park_association, back_populates="parks")
    cases = relationship("Case", back_populates="park_ref")


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False)
    name = Column(String(200), nullable=False)       # 供应商/专家名称
    type = Column(String(50))                         # 技术提供商/咨询机构/研究机构/行业专家
    description = Column(Text)                        # 简介
    website = Column(String(500))                     # 官网链接
    contact = Column(String(200))                     # 联系方式
    related_case = Column(Text)                       # 相关案例
    tool_ref = relationship("Tool", back_populates="suppliers")


class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False)
    park_id = Column(Integer, ForeignKey("parks.id"), nullable=True)
    platform_name = Column(String(200))
    summary = Column(Text)
    effect = Column(Text)
    source_url = Column(String(500))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    tool_ref = relationship("Tool", back_populates="cases")
    park_ref = relationship("Park", back_populates="cases")


class UpdateLog(Base):
    __tablename__ = "update_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tool_id = Column(Integer, ForeignKey("tools.id"))
    version = Column(String(20))
    change_type = Column(String(20))
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False, index=True)
    summary = Column(Text)
    source_name = Column(String(200))       # 来源
    source_url = Column(String(500))        # 来源链接
    publish_date = Column(String(50))       # 发布日期
    category = Column(String(50))           # AI+双碳/AI+能源/AI+零碳园区/AI+碳市场/国际动态
    topic = Column(String(50))              # 技术突破/政策解读/行业应用/企业动态/研究报告
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False, index=True)
    issuing_body = Column(String(200))          # 发布机构
    publish_date = Column(String(50))           # 发布日期
    category = Column(String(50))               # 国际/国家/地方/行业标准
    topic = Column(String(50))                  # 碳市场/碳关税/零碳园区/碳核算/绿色航运/能源转型
    summary = Column(Text)                      # 政策摘要
    source_name = Column(String(200))           # 来源网站名称
    source_url = Column(String(500))            # 来源网站URL
    full_text_url = Column(String(500))         # 全文链接
    tags = Column(JSON, default=list)           # 标签
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
