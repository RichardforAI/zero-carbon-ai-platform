import { useState, useEffect } from 'react'
import { Card, Select, Input, Pagination, Tag, Typography, Space, Spin } from 'antd'
import { SearchOutlined, GlobalOutlined, ThunderboltOutlined } from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography

interface NewsItem {
  id: number
  title: string
  summary: string
  source_name: string
  source_url: string
  publish_date: string
  category: string
  topic: string
  tags: string[]
}

const CATEGORIES = ['全部', 'AI+双碳', 'AI+能源', 'AI+零碳园区', 'AI+碳市场', '国际动态']
const TOPICS = ['全部', '技术突破', '政策解读', '行业应用', '企业动态', '研究报告']

const categoryColors: Record<string, string> = {
  'AI+双碳': '#40e495', 'AI+能源': '#5b9cf5', 'AI+零碳园区': '#a78bfa',
  'AI+碳市场': '#f5c842', '国际动态': '#f5706a',
}

export default function News() {
  const [items, setItems] = useState<NewsItem[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState('')
  const [topic, setTopic] = useState('')
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)

  const fetchNews = () => {
    setLoading(true)
    const params = new URLSearchParams()
    if (category) params.set('category', category)
    if (topic) params.set('topic', topic)
    if (search) params.set('search', search)
    params.set('page', String(page))
    params.set('page_size', '12')
    fetch(`/api/news?${params.toString()}`)
      .then(r => r.json())
      .then(d => { setItems(d.items); setTotal(d.total); setLoading(false) })
      .catch(() => setLoading(false))
  }

  useEffect(() => { fetchNews() }, [page, category, topic])

  const handleSearch = () => { setPage(1); fetchNews() }

  return (
    <div>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:20}}>
        <Title level={3} style={{color:'#e0e6ed',margin:0}}>
          <GlobalOutlined /> 新闻资讯
        </Title>
        <Text style={{color:'#6b7d8e',fontSize:12}}>AI+双碳全球动态 · 实时更新</Text>
      </div>

      {/* Filters */}
      <Card size="small" style={{background:'#151f2b',borderColor:'#1e2d3d',marginBottom:16}}>
        <Space wrap size={[12,8]}>
          <span style={{color:'#6b7d8e',fontSize:12}}>分类:</span>
          {CATEGORIES.map(c => (
            <Tag key={c} color={category === c || (c === '全部' && !category) ? 'green' : undefined}
              style={{cursor:'pointer',opacity:category === c || (c === '全部' && !category) ? 1 : 0.5}}
              onClick={() => { setCategory(c === '全部' ? '' : c); setPage(1) }}>
              {c}
            </Tag>
          ))}
          <span style={{color:'#6b7d8e',fontSize:12,marginLeft:16}}>主题:</span>
          {TOPICS.map(t => (
            <Tag key={t} color={topic === t || (t === '全部' && !topic) ? 'blue' : undefined}
              style={{cursor:'pointer',opacity:topic === t || (t === '全部' && !topic) ? 1 : 0.5}}
              onClick={() => { setTopic(t === '全部' ? '' : t); setPage(1) }}>
              {t}
            </Tag>
          ))}
          <Input.Search placeholder="搜索新闻..." allowClear onSearch={handleSearch}
            value={search} onChange={e => setSearch(e.target.value)}
            style={{width:220}} prefix={<SearchOutlined />} />
        </Space>
      </Card>

      {/* News List */}
      {loading ? (
        <div style={{textAlign:'center',padding:60}}><Spin size="large" /></div>
      ) : (
        <div style={{display:'grid',gap:12}}>
          {items.map(n => (
            <Card key={n.id} size="small" style={{background:'#151f2b',borderColor:'#1e2d3d',cursor:'default'}}
              hoverable>
              <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',gap:16}}>
                <div style={{flex:1}}>
                  <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:6,flexWrap:'wrap'}}>
                    <Tag color={categoryColors[n.category] || 'default'}>{n.category}</Tag>
                    <Tag>{n.topic}</Tag>
                    <Text strong style={{color:'#e0e6ed',fontSize:15}}>{n.title}</Text>
                  </div>
                  <Paragraph style={{color:'#b0bec5',fontSize:13,margin:'6px 0'}} ellipsis={{rows:2}}>
                    {n.summary}
                  </Paragraph>
                  <div style={{display:'flex',alignItems:'center',gap:16,flexWrap:'wrap'}}>
                    <Text style={{color:'#6b7d8e',fontSize:11}}>📅 {n.publish_date}</Text>
                    {n.source_url ? (
                      <a href={n.source_url} target="_blank" rel="noopener noreferrer"
                        style={{color:'#5b9cf5',fontSize:11,textDecoration:'underline'}}>
                        📰 {n.source_name}
                      </a>
                    ) : (
                      <Text style={{color:'#6b7d8e',fontSize:11}}>📰 {n.source_name}</Text>
                    )}
                    {n.tags?.map(t => <Tag key={t} style={{fontSize:10,background:'#1e2d3d',color:'#6b7d8e',border:'none'}}>{t}</Tag>)}
                    {n.source_url && (
                      <a href={n.source_url} target="_blank" rel="noopener noreferrer"
                        style={{fontSize:11,color:'#5b9cf5',marginLeft:'auto'}}>
                        🔗 阅读原文
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {total > 12 && (
        <div style={{textAlign:'center',marginTop:20}}>
          <Pagination current={page} total={total} pageSize={12} onChange={setPage}
            style={{textAlign:'center'}} />
        </div>
      )}
    </div>
  )
}
