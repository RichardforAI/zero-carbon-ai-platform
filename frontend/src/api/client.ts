const BASE = '/api'

export interface DashboardData {
  kpi: { total_tools: number; total_scenarios: number; total_cases: number; park_types_covered: number; operation_phases_covered: number; new_this_month: number }
  category_distribution: { name: string; name_en: string; count: number; color: string }[]
  park_type_coverage: { park_type: string; high_maturity: number; medium_maturity: number; low_maturity: number }[]
  maturity_radar: { phase: string; avg_maturity: number }[]
  building_scene_stats: { tool_count: number; phases: string[]; phase_count: number; case_count: number; category_distribution: { name: string; count: number; color: string }[] }
  last_updated: string
  recent_updates: { id: number; description: string; change_type: string; created_at: string }[]
}

export interface ToolItem {
  id: number; name: string; category_name: string; maturity: number
  applicable_park_types: string[]; operation_phase: string; case_count: number
}

export interface Supplier {
  id: number; tool_id: number; name: string; type: string
  description: string; website: string; contact: string; related_case: string
}

export interface ToolDetail {
  id: number; name: string; category_name: string; category_id: number; maturity: number
  description: string; scenario: string; ai_method: string
  tech_path: string[]; value_props: string[]; prerequisites: string
  implementation_tips: string; operation_phase: string
  applicable_park_types: string[]; case_count: number; version: string
  updated_at: string
  cases: { id: number; platform_name: string; summary: string; effect: string }[]
  suppliers: Supplier[]
}

export interface ParkItem {
  id: number; name: string; city: string; park_type: string
  build_type: string; period: string; industry: string; level: string
}

export interface MatchResult {
  park: ParkItem
  core_recommendations: ToolItem[]
  general_recommendations: ToolItem[]
}

export interface PaginatedTools {
  items: ToolItem[]; total: number; page: number; page_size: number; total_pages: number
}

// === Agent (AI) types ===
export interface RecommendedTool {
  tool_id: number; tool_name: string; category_name: string; maturity: number
  relevance_score: number; reasoning: string; implementation_priority: string
}

export interface AgentMatchResult {
  park: ParkItem
  match_reasoning: string
  confidence: number
  core_recommendations: RecommendedTool[]
  general_recommendations: RecommendedTool[]
}

export interface ReportSection {
  title: string; level: number; content: string
}

export interface AgentReportResult {
  park: ParkItem
  report_title: string
  generated_at: string
  sections: ReportSection[]
}

async function get<T>(url: string): Promise<T> {
  const res = await fetch(`${BASE}${url}`)
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

async function post<T>(url: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `API error: ${res.status}`)
  }
  return res.json()
}

export const api = {
  getDashboard: () => get<DashboardData>('/dashboard'),
  getTools: (params: Record<string, string>) => {
    const qs = new URLSearchParams(params).toString()
    return get<PaginatedTools>(`/tools?${qs}`)
  },
  getTool: (id: number) => get<ToolDetail>(`/tools/${id}`),
  getParks: () => get<ParkItem[]>('/parks'),
  matchPark: (parkId: number) => get<MatchResult>(`/match?park_id=${parkId}`),
  // Agent AI endpoints
  agentMatch: (parkId: number) => post<AgentMatchResult>('/agent/match', { park_id: parkId }),
  agentReport: (parkId: number) => post<AgentReportResult>('/agent/report', { park_id: parkId }),
  // Update endpoint
  triggerUpdate: (modules?: string[], count?: number) =>
    post<{status:string;mode:string;summary:Record<string,number>;details:{module:string;title:string;action:string}[]}>(
      '/update/all', { modules: modules || ['policies','tools','cases','news'], count_per_module: count || 2 }
    ),
}
