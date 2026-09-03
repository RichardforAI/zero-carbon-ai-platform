import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, Tag, Input, Select, Row, Col, Pagination, Spin, Typography, Space, Button } from 'antd'
import { SearchOutlined, PlusOutlined } from '@ant-design/icons'
import { api, ToolItem } from '../api/client'

const CATEGORIES = [
  { id: '', name: '全部' }, { id: '1', name: '预测类' }, { id: '2', name: '优化类' },
  { id: '3', name: '控制类' }, { id: '4', name: '诊断类' }, { id: '5', name: '核算类' },
  { id: '6', name: '识别类' }, { id: '7', name: '调度类' }, { id: '8', name: '知识类' }, { id: '9', name: '创新类' },
]

const PARK_TYPES = ['', '先进制造型', '重化工近零碳型', '新能源装备制造型', '新材料型', '临港特色产业型', '生态高新技术型']
const PARK_PRIMARY_TYPES = ['', '工业园区', '公建园区', '高新园区', '物流/农业园区']
const PARK_SECONDARY_MAP: Record<string, string[]> = {
  '工业园区': ['', '重化工', '装备制造', '电子信息'],
  '公建园区': ['', '政务中心', '商务楼宇', '医院', '学校'],
  '高新园区': ['', '科技园', '孵化器', '数据中心集群'],
  '物流/农业园区': ['', '仓储物流中心', '现代农业产业园'],
}
const SCENE_TAGS = ['', '建筑运行', '能源管理', '交通物流', '水资源管理', '废弃物管理', '碳汇管理', '供应链碳管理', '园区综合规划']
const PHASES = ['', '电力/能源管理', '建筑用能优化', '工业生产过程', '设备运维管理', '交通物流', '碳核算与交易', '水资源管理', '废弃物管理', '碳汇管理', '供应链碳管理', '综合规划决策']

const starColors: Record<number, string> = { 1: '#f5706a', 2: '#fb923c', 3: '#f5c842', 4: '#5b9cf5', 5: '#40e495' }

export default function ToolList() {
  const [tools, setTools] = useState<ToolItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState<Record<string, string>>({ page: '1', page_size: '12' })
  const navigate = useNavigate()

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = { ...filters, page: String(page) }
    Object.keys(params).forEach(k => { if (!params[k]) delete params[k] })
    api.getTools(params).then(d => { setTools(d.items); setTotal(d.total); setLoading(false) })
  }

  useEffect(() => { load() }, [page, filters])

  const stars = (m: number) => '★'.repeat(m) + '☆'.repeat(5 - m)

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Typography.Title level={3} style={{ color: '#e0e6ed', margin: 0 }}>AI工具箱分类浏览</Typography.Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/tools/new')}
          style={{ background: '#40e495', borderColor: '#40e495', color: '#0f1923', fontWeight: 'bold' }}>
          新增工具
        </Button>
      </div>

      {/* Type tags */}
      <div style={{ marginBottom: 16, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
        {CATEGORIES.map(c => (
          <Tag.CheckableTag
            key={c.id}
            checked={filters.category_id === c.id || (!filters.category_id && c.id === '')}
            onChange={() => setFilters(f => ({ ...f, category_id: c.id }))}
            style={{ padding: '4px 14px', fontSize: 12, borderRadius: 16, border: '1px solid #1e2d3d' }}
          >
            {c.name}
          </Tag.CheckableTag>
        ))}
      </div>

      {/* Filters */}
      <Space wrap style={{ marginBottom: 20, width: '100%' }}>
        <Select
          placeholder="一级分类" allowClear style={{ width: 150 }}
          options={PARK_PRIMARY_TYPES.map(p => ({ value: p, label: p || '全部分类' }))}
          value={filters.park_type_primary || ''}
          onChange={v => setFilters(f => ({ ...f, park_type_primary: v || '', park_type_secondary: '' }))}
        />
        <Select
          placeholder="二级分类" allowClear style={{ width: 150 }}
          options={(PARK_SECONDARY_MAP[filters.park_type_primary || ''] || ['']).map(s => ({ value: s, label: s || '全部' }))}
          value={filters.park_type_secondary || ''}
          onChange={v => setFilters(f => ({ ...f, park_type_secondary: v || '' }))}
          disabled={!filters.park_type_primary}
        />
        <Select
          placeholder="运营环节" allowClear style={{ width: 150 }}
          options={PHASES.map(p => ({ value: p, label: p || '全部运营环节' }))}
          onChange={v => setFilters(f => ({ ...f, operation_phase: v || '' }))}
        />
        <Select
          placeholder="应用场景" allowClear style={{ width: 140 }}
          options={SCENE_TAGS.map(s => ({ value: s, label: s || '全部场景' }))}
          onChange={v => setFilters(f => ({ ...f, scene_tag: v || '' }))}
        />
        <Select
          placeholder="运营环节" allowClear style={{ width: 160 }}
          options={PHASES.map(p => ({ value: p, label: p || '全部运营环节' }))}
          onChange={v => setFilters(f => ({ ...f, operation_phase: v || '' }))}
        />
        <Select
          placeholder="应用场景" allowClear style={{ width: 140 }}
          options={SCENE_TAGS.map(s => ({ value: s, label: s || '全部场景' }))}
          onChange={v => setFilters(f => ({ ...f, scene_tag: v || '' }))}
        />
        <Select
          placeholder="成熟度" allowClear style={{ width: 120 }}
          options={[5, 4, 3, 2, 1].map(m => ({ value: String(m), label: '★'.repeat(m) }))}
          onChange={v => setFilters(f => ({ ...f, maturity_min: v || '' }))}
        />
        <Input
          placeholder="搜索AI工具名称、场景..." prefix={<SearchOutlined />} style={{ width: 260 }}
          allowClear
          onPressEnter={e => setFilters(f => ({ ...f, search: (e.target as HTMLInputElement).value }))}
          onBlur={e => setFilters(f => ({ ...f, search: (e.target as HTMLInputElement).value }))}
        />
      </Space>

      {loading ? <Spin size="large" style={{ display: 'block', marginTop: 60 }} /> : (
        <>
          <Typography.Text style={{ color: '#6b7d8e', marginBottom: 16, display: 'block' }}>
            共 {total} 个工具
          </Typography.Text>
          <Row gutter={[14, 14]}>
            {tools.map(t => (
              <Col span={8} key={t.id}>
                <Card
                  hoverable
                  onClick={() => navigate(`/tools/${t.id}`)}
                  style={{ background: '#151f2b', borderColor: '#1e2d3d', cursor: 'pointer', height: '100%' }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                    <span style={{ color: starColors[t.maturity], fontSize: 13 }}>{stars(t.maturity)}</span>
                  </div>
                  <Typography.Title level={5} style={{ color: '#fff', margin: '0 0 8px' }}>{t.name}</Typography.Title>
                  <Space size={4} style={{ marginBottom: 8 }}>
                    <Tag color="blue" style={{ fontSize: 10 }}>{t.category_name}</Tag>
                    {t.applicable_park_types?.slice(0, 2).map(pt => (
                      <Tag key={pt} color="green" style={{ fontSize: 10 }}>{pt}</Tag>
                    ))}
                  </Space>
                  <div style={{ color: '#6b7d8e', fontSize: 11 }}>
                    <span>{t.operation_phase}</span>
                    <span style={{ float: 'right', color: '#5b9cf5' }}>{t.case_count} 案例</span>
                  </div>
                </Card>
              </Col>
            ))}
          </Row>
          <div style={{ textAlign: 'center', marginTop: 24 }}>
            <Pagination
              current={page} total={total} pageSize={12}
              onChange={p => setPage(p)}
              showSizeChanger={false}
            />
          </div>
        </>
      )}
    </div>
  )
}
