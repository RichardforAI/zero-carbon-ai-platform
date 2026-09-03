import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, Tag, Descriptions, List, Typography, Spin, Button, Space } from 'antd'
import { ArrowLeftOutlined, StarFilled } from '@ant-design/icons'
import { api, ToolDetail as ToolDetailType } from '../api/client'

export default function ToolDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [tool, setTool] = useState<ToolDetailType | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (id) {
      api.getTool(Number(id)).then(d => { setTool(d); setLoading(false) })
    }
  }, [id])

  if (loading || !tool) return <Spin size="large" style={{ display: 'block', marginTop: 80 }} />

  return (
    <div>
      <Button type="link" icon={<ArrowLeftOutlined />} onClick={() => navigate('/tools')} style={{ padding: 0, marginBottom: 16 }}>
        返回工具箱列表
      </Button>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 20 }}>
        <div>
          <Typography.Title level={2} style={{ color: '#fff', margin: 0 }}>{tool.name}</Typography.Title>
          <Space style={{ marginTop: 8 }}>
            <Tag color="blue">{tool.category_name}</Tag>
            <span style={{ color: '#f5c842' }}>{'★'.repeat(tool.maturity)}{'☆'.repeat(5 - tool.maturity)}</span>
            {tool.applicable_park_types?.map(pt => <Tag key={pt} color="green">{pt}</Tag>)}
            <span style={{ color: '#6b7d8e', fontSize: 12 }}>运营环节：{tool.operation_phase}</span>
            <span style={{ color: '#5b9cf5', fontSize: 12 }}>{tool.case_count} 个应用案例</span>
          </Space>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, marginBottom: 14 }}>
        <Card title="基本信息" style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
          <Descriptions column={1} size="small">
            <Descriptions.Item label="工具类型">{tool.category_name}</Descriptions.Item>
            <Descriptions.Item label="技术成熟度">{tool.maturity}/5 星</Descriptions.Item>
            <Descriptions.Item label="版本">{tool.version}</Descriptions.Item>
            <Descriptions.Item label="更新时间">{tool.updated_at?.slice(0, 10)}</Descriptions.Item>
          </Descriptions>
        </Card>
        <Card title="技术路径" style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
          <Space wrap>
            {tool.tech_path?.map(t => <Tag key={t} color="blue" style={{ fontSize: 11 }}>{t}</Tag>)}
          </Space>
        </Card>
      </div>

      <Card title="适用场景" style={{ background: '#151f2b', borderColor: '#1e2d3d', marginBottom: 14 }}>
        <Typography.Paragraph style={{ color: '#b0bec5', margin: 0 }}>{tool.scenario}</Typography.Paragraph>
      </Card>

      <Card title="AI赋能方式" style={{ background: '#151f2b', borderColor: '#1e2d3d', marginBottom: 14 }}>
        <Typography.Paragraph style={{ color: '#b0bec5', margin: 0 }}>{tool.ai_method}</Typography.Paragraph>
      </Card>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, marginBottom: 14 }}>
        <Card title="应用价值" style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
          <List size="small" dataSource={tool.value_props || []} renderItem={v => (
            <List.Item style={{ color: '#40e495', borderColor: '#1e2d3d', padding: '4px 0' }}>
              <Typography.Text style={{ color: '#40e495' }}>+ {v}</Typography.Text>
            </List.Item>
          )} />
        </Card>
        <Card title="前置条件与数据要求" style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
          <Typography.Paragraph style={{ color: '#b0bec5', margin: 0 }}>{tool.prerequisites}</Typography.Paragraph>
        </Card>
      </div>

      <Card title="参考案例" style={{ background: '#151f2b', borderColor: '#1e2d3d', marginBottom: 14 }}>
        <List size="small" dataSource={tool.cases || []} renderItem={c => (
          <List.Item style={{ borderColor: '#1e2d3d' }}>
            <div>
              <Typography.Text strong style={{ color: '#e0e6ed' }}>{c.platform_name}</Typography.Text>
              <br />
              <Typography.Text style={{ color: '#8899aa', fontSize: 12 }}>{c.summary} — {c.effect}</Typography.Text>
            </div>
          </List.Item>
        )} />
      </Card>

      <Card title="🔗 供应商与专家资源" style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
        {tool.suppliers && tool.suppliers.length > 0 ? (
          <List size="small" dataSource={tool.suppliers} renderItem={s => (
            <List.Item style={{ borderColor: '#1e2d3d', padding: '12px 0' }}>
              <div style={{ width: '100%' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                  <Space>
                    <Typography.Text strong style={{ color: '#e0e6ed', fontSize: 14 }}>{s.name}</Typography.Text>
                    <Tag color={s.type === '技术提供商' ? 'blue' : s.type === '研究机构' ? 'green' : 'orange'} style={{ fontSize: 10 }}>
                      {s.type}
                    </Tag>
                  </Space>
                </div>
                <Typography.Paragraph style={{ color: '#b0bec5', fontSize: 12, margin: '4px 0' }} ellipsis={{ rows: 2 }}>
                  {s.description}
                </Typography.Paragraph>
                {s.related_case && (
                  <Typography.Text style={{ color: '#6b7d8e', fontSize: 11 }}>
                    📌 相关案例：{s.related_case}
                  </Typography.Text>
                )}
                <div style={{ marginTop: 6, display: 'flex', gap: 16 }}>
                  {s.website && (
                    <a href={s.website} target="_blank" rel="noopener noreferrer"
                      style={{ color: '#5b9cf5', fontSize: 12 }}>
                      🌐 {s.website.replace('https://', '').replace('www.', '')}
                    </a>
                  )}
                  {s.contact && (
                    <Typography.Text style={{ color: '#6b7d8e', fontSize: 12 }}>📞 {s.contact}</Typography.Text>
                  )}
                </div>
              </div>
            </List.Item>
          )} />
        ) : (
          <Typography.Text style={{ color: '#6b7d8e' }}>暂无供应商信息，欢迎推荐相关专家和供应商资源</Typography.Text>
        )}
      </Card>
    </div>
  )
}
