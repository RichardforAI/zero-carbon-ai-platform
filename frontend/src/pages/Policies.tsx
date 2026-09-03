import { useEffect, useState } from 'react'
import { Card, Tag, Row, Col, Typography, Spin, Empty, Input, Select, Space, Pagination } from 'antd'
import { SearchOutlined, LinkOutlined, FileTextOutlined } from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography

interface PolicyItem {
  id: number; title: string; issuing_body: string; publish_date: string
  category: string; topic: string; summary: string
  source_name: string; source_url: string; full_text_url: string; tags: string[]
}

const CATEGORY_OPTIONS = [
  { value: '', label: '全部分类' },
  { value: '国际', label: '🌍 国际' },
  { value: '国家', label: '🏛️ 国家' },
  { value: '地方', label: '📍 地方' },
  { value: '行业标准', label: '📐 行业标准' },
]

const TOPIC_OPTIONS = [
  { value: '', label: '全部主题' },
  { value: '碳市场', label: '碳市场' },
  { value: '碳关税', label: '碳关税' },
  { value: '零碳园区', label: '零碳园区' },
  { value: '碳核算', label: '碳核算' },
  { value: '绿色航运', label: '绿色航运' },
  { value: '能源转型', label: '能源转型' },
]

const CATEGORY_COLORS: Record<string, string> = {
  '国际': 'blue', '国家': 'red', '地方': 'green', '行业标准': 'orange',
}
const TOPIC_COLORS: Record<string, string> = {
  '碳市场': 'purple', '碳关税': 'magenta', '零碳园区': 'green',
  '碳核算': 'cyan', '绿色航运': 'geekblue', '能源转型': 'gold',
}

export default function Policies() {
  const [policies, setPolicies] = useState<PolicyItem[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [category, setCategory] = useState('')
  const [topic, setTopic] = useState('')
  const [search, setSearch] = useState('')
  const pageSize = 12

  const fetchPolicies = () => {
    setLoading(true)
    const params = new URLSearchParams()
    params.set('page', String(page))
    params.set('page_size', String(pageSize))
    if (category) params.set('category', category)
    if (topic) params.set('topic', topic)
    if (search) params.set('search', search)

    fetch(`/api/policies?${params.toString()}`)
      .then(r => r.json())
      .then(d => { setPolicies(d.items || d); setTotal(d.total || d.length); setLoading(false) })
      .catch(() => setLoading(false))
  }

  useEffect(() => { fetchPolicies() }, [page, category, topic])

  const doSearch = () => { setPage(1); fetchPolicies() }

  return (
    <div>
      <Title level={3} style={{ color: '#e0e6ed', marginBottom: 20 }}>
        <FileTextOutlined /> 政策法规
      </Title>

      {/* Filters */}
      <Card size="small" style={{ background: '#151f2b', borderColor: '#1e2d3d', marginBottom: 20 }}>
        <Row gutter={[12, 12]} align="middle">
          <Col span={4}>
            <Select
              value={category} onChange={v => { setCategory(v); setPage(1) }}
              options={CATEGORY_OPTIONS} style={{ width: '100%' }}
            />
          </Col>
          <Col span={4}>
            <Select
              value={topic} onChange={v => { setTopic(v); setPage(1) }}
              options={TOPIC_OPTIONS} style={{ width: '100%' }}
            />
          </Col>
          <Col span={10}>
            <Input
              placeholder="搜索政策标题、摘要..."
              prefix={<SearchOutlined />} value={search}
              onChange={e => setSearch(e.target.value)}
              onPressEnter={doSearch}
              allowClear
            />
          </Col>
          <Col span={6}>
            <Text style={{ color: '#6b7d8e', fontSize: 12 }}>共 {total} 条政策</Text>
          </Col>
        </Row>
      </Card>

      {/* Policy list */}
      {loading ? (
        <Spin size="large" style={{ display: 'block', marginTop: 60 }} />
      ) : policies.length === 0 ? (
        <Empty description="暂无匹配的政策" />
      ) : (
        <>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {policies.map(p => (
              <Card
                key={p.id}
                style={{ background: '#151f2b', borderColor: '#1e2d3d', cursor: p.source_url ? 'pointer' : 'default' }}
                hoverable={!!p.source_url}
                onClick={() => { if (p.source_url) window.open(p.source_url, '_blank') }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
                  <Title level={5} style={{ color: '#fff', margin: 0, flex: 1 }}>
                    {p.source_url ? <LinkOutlined style={{ marginRight: 8, color: '#5b9cf5', fontSize: 12 }} /> : null}
                    {p.title}
                  </Title>
                  <Space size={4} style={{ flexShrink: 0, marginLeft: 12 }}>
                    <Tag color={CATEGORY_COLORS[p.category] || 'default'} style={{ fontSize: 10 }}>
                      {p.category}
                    </Tag>
                    <Tag color={TOPIC_COLORS[p.topic] || 'default'} style={{ fontSize: 10 }}>
                      {p.topic}
                    </Tag>
                  </Space>
                </div>

                <Paragraph
                  style={{ color: '#c0ccd8', fontSize: 13, marginBottom: 8, lineHeight: 1.7 }}
                  ellipsis={{ rows: 2 }}
                >
                  {p.summary}
                </Paragraph>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Space size={8}>
                    <Text style={{ color: '#6b7d8e', fontSize: 11 }}>{p.issuing_body}</Text>
                    <Text style={{ color: '#4a5d6e', fontSize: 11 }}>·</Text>
                    <Text style={{ color: '#6b7d8e', fontSize: 11 }}>{p.publish_date}</Text>
                    <Text style={{ color: '#4a5d6e', fontSize: 11 }}>·</Text>
                    {p.source_url ? (
                      <a href={p.source_url} target="_blank" rel="noopener noreferrer"
                        style={{color:'#40e495',fontSize:11,textDecoration:'underline'}}
                        onClick={e => e.stopPropagation()}>
                        来源: {p.source_name} 🔗
                      </a>
                    ) : (
                      <Text style={{ color: '#40e495', fontSize: 11 }}>来源: {p.source_name}</Text>
                    )}
                  </Space>
                  <Space size={4}>
                    {p.source_url && (
                      <a href={p.source_url} target="_blank" rel="noopener noreferrer"
                        style={{fontSize:11,color:'#5b9cf5'}}
                        onClick={e => e.stopPropagation()}>
                        🔗 阅读原文
                      </a>
                    )}
                    {p.tags && p.tags.length > 0 && (
                      <Space size={4}>
                        {p.tags.slice(0, 3).map(tag => (
                          <Tag key={tag} style={{ fontSize: 9, background: 'rgba(91,156,245,0.1)', border: 'none', color: '#5b9cf5' }}>
                            {tag}
                          </Tag>
                        ))}
                      </Space>
                    )}
                  </Space>
                </div>
              </Card>
            ))}
          </div>

          <div style={{ textAlign: 'center', marginTop: 24 }}>
            <Pagination
              current={page} total={total} pageSize={pageSize}
              onChange={p => setPage(p)} showSizeChanger={false}
            />
          </div>
        </>
      )}
    </div>
  )
}
