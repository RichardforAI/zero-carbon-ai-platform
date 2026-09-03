"""Pydantic schemas for API request/response."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# === Category ===
class CategoryOut(BaseModel):
    id: int
    name: str
    name_en: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

    model_config = {"from_attributes": True}


# === Tool ===
class ToolBrief(BaseModel):
    """Brief tool card for list view."""
    id: int
    name: str
    category_name: Optional[str] = Field(None, alias="category_name")
    maturity: int
    applicable_park_types: Optional[List[str]] = None
    scene_tags: Optional[List[str]] = None
    operation_phase: Optional[str] = None
    case_count: int

    model_config = {"from_attributes": True}


class ToolDetail(BaseModel):
    """Full tool detail."""
    id: int
    name: str
    category_name: Optional[str] = None
    category_id: Optional[int] = None
    maturity: int
    description: Optional[str] = None
    scenario: Optional[str] = None
    ai_method: Optional[str] = None
    tech_path: Optional[List[str]] = None
    value_props: Optional[List[str]] = None
    prerequisites: Optional[str] = None
    implementation_tips: Optional[str] = None
    operation_phase: Optional[str] = None
    applicable_park_types: Optional[List[str]] = None
    scene_tags: Optional[List[str]] = None
    case_count: int
    version: Optional[str] = None
    updated_at: Optional[datetime] = None
    cases: List["CaseOut"] = []
    suppliers: List["SupplierOut"] = []

    model_config = {"from_attributes": True}


class ToolFilter(BaseModel):
    """Filter params for tool list."""
    category_id: Optional[int] = None
    park_type: Optional[str] = None
    operation_phase: Optional[str] = None
    maturity_min: Optional[int] = None
    maturity_max: Optional[int] = None
    search: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=12, ge=1, le=50)


# === Park ===
class ParkBrief(BaseModel):
    id: int
    name: str
    city: Optional[str] = None
    park_type: Optional[str] = None
    park_type_primary: Optional[str] = None    # NEW: 一级分类
    park_type_secondary: Optional[str] = None  # NEW: 二级分类
    build_type: Optional[str] = None
    period: Optional[str] = None
    industry: Optional[str] = None
    level: Optional[str] = None

    model_config = {"from_attributes": True}


class ParkDetail(BaseModel):
    id: int
    name: str
    city: Optional[str] = None
    province: Optional[str] = None
    park_type: Optional[str] = None
    park_type_primary: Optional[str] = None     # NEW
    park_type_secondary: Optional[str] = None   # NEW
    build_type: Optional[str] = None
    period: Optional[str] = None
    industry: Optional[str] = None
    key_directions: Optional[List[str]] = None
    energy_profile: Optional[str] = None        # NEW: 能耗特征
    carbon_structure: Optional[str] = None      # NEW: 主要碳排结构
    core_challenges: Optional[str] = None       # NEW: 核心挑战
    description: Optional[str] = None
    level: Optional[str] = None

    model_config = {"from_attributes": True}


# === Case ===
class CaseOut(BaseModel):
    id: int
    platform_name: Optional[str] = None
    summary: Optional[str] = None
    effect: Optional[str] = None
    source_url: Optional[str] = None

    model_config = {"from_attributes": True}


# === Match ===
class MatchRequest(BaseModel):
    park_id: int


class MatchResult(BaseModel):
    park: ParkBrief
    core_recommendations: List[ToolBrief]  # 3-5 high-match tools
    general_recommendations: List[ToolBrief]  # 8-12 general tools


# === Dashboard ===
class DashboardKPI(BaseModel):
    total_tools: int
    total_scenarios: int
    total_cases: int
    park_types_covered: int
    operation_phases_covered: int
    new_this_month: int


class CategoryDistribution(BaseModel):
    name: str
    name_en: str
    count: int
    color: str


class ParkTypeCoverage(BaseModel):
    park_type: str
    high_maturity: int
    medium_maturity: int
    low_maturity: int


class MaturityRadar(BaseModel):
    phase: str
    avg_maturity: float


class DashboardData(BaseModel):
    kpi: DashboardKPI
    category_distribution: List[CategoryDistribution]
    park_type_coverage: List[ParkTypeCoverage]
    maturity_radar: List[MaturityRadar]
    building_scene_stats: dict = {}  # {tool_count, phases, cases}
    last_updated: Optional[str] = None
    recent_updates: List["UpdateLogOut"]


# === Update Log ===
class UpdateLogOut(BaseModel):
    id: int
    tool_id: Optional[int] = None
    version: Optional[str] = None
    change_type: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# Paginated response
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int


# === Agent (AI) ===
class AgentMatchRequest(BaseModel):
    park_id: int


class RecommendedTool(BaseModel):
    """A tool recommendation with AI reasoning."""
    tool_id: int
    tool_name: str
    category_name: str
    maturity: int
    relevance_score: float  # 0-100
    reasoning: str
    implementation_priority: str  # "immediate" | "short_term" | "long_term"


class AgentMatchResult(BaseModel):
    park: ParkBrief
    match_reasoning: str
    confidence: float  # 0-1
    core_recommendations: List[RecommendedTool]  # 3-5 tools
    general_recommendations: List[RecommendedTool]  # 5-8 tools


class AgentReportRequest(BaseModel):
    park_id: int


class ReportSection(BaseModel):
    title: str
    level: int  # heading level (1 or 2)
    content: str  # Markdown content


class AgentReportResult(BaseModel):
    park: ParkBrief
    report_title: str
    generated_at: datetime
    sections: List[ReportSection]


# === Policy ===
class PolicyBrief(BaseModel):
    id: int
    title: str
    issuing_body: Optional[str] = None
    publish_date: Optional[str] = None
    category: Optional[str] = None
    topic: Optional[str] = None
    summary: Optional[str] = None
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    full_text_url: Optional[str] = None
    tags: Optional[List[str]] = None

    model_config = {"from_attributes": True}


class PolicySource(BaseModel):
    name: str
    url: str
    description: str


# === ToolEdit ===
class ToolCreate(BaseModel):
    name: str
    category_id: int
    maturity: int = 3
    description: Optional[str] = None
    scenario: Optional[str] = None
    ai_method: Optional[str] = None
    tech_path: Optional[List[str]] = None
    value_props: Optional[List[str]] = None
    prerequisites: Optional[str] = None
    implementation_tips: Optional[str] = None
    operation_phase: Optional[str] = None
    applicable_park_types: Optional[List[str]] = None
    scene_tags: Optional[List[str]] = None
    case_count: int = 0
    version: str = "1.0"


class ToolUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    maturity: Optional[int] = None
    description: Optional[str] = None
    scenario: Optional[str] = None
    ai_method: Optional[str] = None
    tech_path: Optional[List[str]] = None
    value_props: Optional[List[str]] = None
    prerequisites: Optional[str] = None
    implementation_tips: Optional[str] = None
    operation_phase: Optional[str] = None
    applicable_park_types: Optional[List[str]] = None
    scene_tags: Optional[List[str]] = None
    case_count: Optional[int] = None
    version: Optional[str] = None


class AIGenerateRequest(BaseModel):
    name: str
    brief_description: str  # 一句话描述


# === News ===
class NewsBrief(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    publish_date: Optional[str] = None
    category: Optional[str] = None
    topic: Optional[str] = None
    tags: Optional[List[str]] = None

    model_config = {"from_attributes": True}


# === Update ===
class UpdateRequest(BaseModel):
    modules: List[str] = ["policies", "tools", "cases", "news"]
    count_per_module: int = Field(default=2, ge=1, le=5)


class UpdateDetail(BaseModel):
    module: str
    title: str
    action: str  # "created" | "skipped" | "error"


class UpdateResult(BaseModel):
    status: str  # "ok" | "partial" | "error"
    mode: str  # "llm" | "demo"
    summary: dict
    details: List[UpdateDetail]


# === Whitepaper ===
class WhitepaperData(BaseModel):
    title: str
    last_updated: str
    chapters: List[ReportSection]  # reuse ReportSection


# === Supplier ===
class SupplierOut(BaseModel):
    id: int
    tool_id: int
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    contact: Optional[str] = None
    related_case: Optional[str] = None

    model_config = {"from_attributes": True}
