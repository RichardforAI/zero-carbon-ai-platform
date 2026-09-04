import { useEffect, useState } from 'react'
import { Card, Select, Button, Typography, Spin, Space, Empty, Alert, Anchor, Divider, Tag, Row, Col } from 'antd'
import { FileTextOutlined, RobotOutlined, ClockCircleOutlined, BulbOutlined } from '@ant-design/icons'
import { api, ParkItem, AgentReportResult } from '../api/client'

const { Title, Text } = Typography

/** Simple markdown-to-JSX renderer for report content */
function SimpleMarkdown({ content }: { content: string }) {
  if (!content) return null

  const lines = content.split('\n')
  const elements: React.ReactNode[] = []
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    // Heading ### or ##
    if (/^###\s/.test(line)) {
      elements.push(
        <Title key={i} level={5} style={{ color: '#c0ccd8', marginTop: 16, marginBottom: 8 }}>
          {line.replace(/^###\s+/, '')}
        </Title>
      )
      i++; continue
    }
    if (/^##\s/.test(line)) {
      elements.push(
        <Title key={i} level={4} style={{ color: '#40e495', marginTop: 20, marginBottom: 10 }}>
          {line.replace(/^##\s+/, '')}
        </Title>
      )
      i++; continue
    }

    // Unordered list
    if (/^[-*]\s/.test(line)) {
      const startIdx = i
      const listItems: string[] = []
      while (i < lines.length && /^[-*]\s/.test(lines[i])) {
        listItems.push(lines[i].replace(/^[-*]\s+/, ''))
        i++
      }
      elements.push(
        <ul key={startIdx} style={{ color: '#c0ccd8', paddingLeft: 20, margin: '8px 0' }}>
          {listItems.map((item, idx) => {
            // Bold markers
            const formatted = item.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            return <li key={idx} style={{ marginBottom: 4, lineHeight: 1.8 }}
              dangerouslySetInnerHTML={{ __html: formatted }} />
          })}
        </ul>
      )
      continue
    }

    // Ordered list
    if (/^\d+\.\s/.test(line)) {
      const startIdx = i
      const listItems: string[] = []
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        listItems.push(lines[i].replace(/^\d+\.\s+/, ''))
        i++
      }
      elements.push(
        <ol key={startIdx} style={{ color: '#c0ccd8', paddingLeft: 20, margin: '8px 0' }}>
          {listItems.map((item, idx) => {
            const formatted = item.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            return <li key={idx} style={{ marginBottom: 4, lineHeight: 1.8 }}
              dangerouslySetInnerHTML={{ __html: formatted }} />
          })}
        </ol>
      )
      continue
    }

    // Horizontal rule
    if (/^---/.test(line)) {
      elements.push(<Divider key={i} style={{ borderColor: '#1e2d3d', margin: '16px 0' }} />)
      i++; continue
    }

    // Blockquote
    if (/^>\s/.test(line)) {
      const startIdx = i
      const quoteLines: string[] = []
      while (i < lines.length && /^>\s/.test(lines[i])) {
        quoteLines.push(lines[i].replace(/^>\s+/, ''))
        i++
      }
      elements.push(
        <div key={startIdx} style={{
          borderLeft: '3px solid #5b9cf5', padding: '8px 16px', margin: '12px 0',
          background: 'rgba(91,156,245,0.08)', borderRadius: '0 4px 4px 0'
        }}>
          {quoteLines.map((ql, idx) => {
            const formatted = ql.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            return <p key={idx} style={{ color: '#8ea4b8', margin: 0, fontSize: 13, lineHeight: 1.8 }}
              dangerouslySetInnerHTML={{ __html: formatted }} />
          })}
        </div>
      )
      continue
    }

    // Empty line
    if (line.trim() === '') {
      elements.push(<div key={i} style={{ height: 8 }} />)
      i++; continue
    }

    // Normal paragraph (also handles **bold** / *italic* lines that start with * or -)
    const startIdx = i
    const paraLines: string[] = []
    while (i < lines.length && lines[i].trim() !== '' &&
      !/^#{1,6}\s/.test(lines[i]) && !/^[-*]\s/.test(lines[i]) && !/^\d+\.\s/.test(lines[i]) &&
      !/^>\s?/.test(lines[i]) && !/^---/.test(lines[i])) {
      paraLines.push(lines[i])
      i++
    }
    if (paraLines.length === 0) {
      // Safety net: never loop forever on an unrecognized line type
      paraLines.push(line)
      i++
    }
    const paraText = paraLines.join('\n')
    const formatted = paraText
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/`([^`]+)`/g, '<code style="background:#1e2d3d;color:#40e495;padding:1px 6px;border-radius:3px;font-size:12px">$1</code>')

    elements.push(
      <p key={startIdx} style={{ color: '#c0ccd8', marginBottom: 8, lineHeight: 1.9, fontSize: 14 }}
        dangerouslySetInnerHTML={{ __html: formatted }} />
    )
  }

  return <>{elements}</>
}

export default function Report() {
  const [parks, setParks] = useState<ParkItem[]>([])
  const [selectedPark, setSelectedPark] = useState<number | null>(null)
  const [parksLoading, setParksLoading] = useState(true)
  const [report, setReport] = useState<AgentReportResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api.getParks().then(d => { setParks(d); setParksLoading(false) })
  }, [])

  const generateReport = () => {
    if (!selectedPark) return
    setLoading(true)
    setReport(null)
    setError(null)
    api.agentReport(selectedPark)
      .then(d => { setReport(d); setLoading(false) })
      .catch(e => { setError(e.message); setLoading(false) })
  }

  const selectedParkName = parks.find(p => p.id === selectedPark)?.name || ''

  // Build anchor items from report sections
  const anchorItems = report?.sections.map((s, i) => ({
    key: `section-${i}`,
    href: `#section-${i}`,
    title: s.title,
  })) || []

  return (
    <div>
      <Title level={3} style={{ color: '#e0e6ed', marginBottom: 20 }}>
        <FileTextOutlined /> AI报告生成
      </Title>

      <Row gutter={24}>
        {/* Left: Park selector */}
        <Col span={5}>
          <Card title="生成配置" style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
            <Text style={{ color: '#6b7d8e', fontSize: 12, display: 'block', marginBottom: 8 }}>
              选择园区
            </Text>
            <Select
              showSearch
              placeholder="选择园区..."
              style={{ width: '100%', marginBottom: 16 }}
              loading={parksLoading}
              options={parks.map(p => ({ value: p.id, label: p.name }))}
              onChange={v => setSelectedPark(v)}
              filterOption={(input, option) => (option?.label as string)?.includes(input)}
            />

            <Button
              type="primary"
              block
              onClick={generateReport}
              loading={loading}
              icon={<RobotOutlined />}
              size="large"
              style={{ background: '#40e495', borderColor: '#40e495', color: '#0f1923', fontWeight: 'bold' }}
            >
              生成AI分析报告
            </Button>

            <div style={{ marginTop: 16, color: '#6b7d8e', fontSize: 11, lineHeight: 1.8 }}>
              <Text style={{ color: '#40e495', fontSize: 12, display: 'block', marginBottom: 8 }}>
                💡 报告包含内容：
              </Text>
              <div>📋 园区概况分析</div>
              <div>🛠️ 核心AI工具推荐</div>
              <div>🔍 技术缺口分析</div>
              <div>🗺️ 分阶段实施路线图</div>
              <div>📝 总结与行动建议</div>
            </div>
          </Card>

          {/* Section navigation */}
          {report && anchorItems.length > 0 && (
            <Card title="报告目录" size="small" style={{ background: '#151f2b', borderColor: '#1e2d3d', marginTop: 16 }}>
              <Anchor
                items={anchorItems}
                style={{ background: 'transparent' }}
              />
            </Card>
          )}
        </Col>

        {/* Right: Report display */}
        <Col span={19}>
          {loading ? (
            <Card style={{ background: '#151f2b', borderColor: '#1e2d3d', textAlign: 'center', padding: 60 }}>
              <Spin size="large" />
              <div style={{ marginTop: 24 }}>
                <Title level={4} style={{ color: '#40e495' }}>
                  <RobotOutlined /> AI正在生成分析报告...
                </Title>
                <Text style={{ color: '#6b7d8e', fontSize: 14, display: 'block', marginTop: 8 }}>
                  正在分析 {selectedParkName} 的园区特征
                </Text>
                <Text style={{ color: '#4a5d6e', fontSize: 12, display: 'block', marginTop: 4 }}>
                  AI将对园区概况、工具推荐、技术缺口、实施路线图进行综合分析
                </Text>
                <Text style={{ color: '#4a5d6e', fontSize: 11, display: 'block' }}>
                  （首次生成约需10-20秒，请耐心等待）
                </Text>
              </div>
            </Card>
          ) : error ? (
            <Alert
              type="error"
              message="报告生成失败"
              description={error}
              showIcon
              style={{ marginTop: 40 }}
              action={<Button size="small" onClick={generateReport}>重试</Button>}
            />
          ) : report ? (
            <Card style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
              {/* Report header */}
              <div style={{ marginBottom: 24, paddingBottom: 16, borderBottom: '2px solid #1e2d3d' }}>
                <Title level={3} style={{ color: '#40e495', marginBottom: 8 }}>
                  {report.report_title}
                </Title>
                <Space size={16}>
                  <Text style={{ color: '#6b7d8e', fontSize: 12 }}>
                    <ClockCircleOutlined /> 生成时间: {new Date(report.generated_at).toLocaleString('zh-CN')}
                  </Text>
                  <Tag color="green">{report.park.park_type}</Tag>
                  <Tag color="blue">{report.park.city}</Tag>
                </Space>
              </div>

              {/* Report sections */}
              {report.sections.map((section, idx) => (
                <div key={idx} id={`section-${idx}`} style={{ marginBottom: 24 }}>
                  <Title level={4} style={{
                    color: '#40e495', marginBottom: 12,
                    paddingBottom: 8, borderBottom: '1px solid #1e2d3d'
                  }}>
                    {section.title}
                  </Title>
                  <div style={{ paddingLeft: 4 }}>
                    <SimpleMarkdown content={section.content} />
                  </div>
                </div>
              ))}

              {/* Footer */}
              <Divider style={{ borderColor: '#1e2d3d' }} />
              <Text style={{ color: '#4a5c6e', fontSize: 11 }}>
                本报告由AI自动生成，仅供参考。实际决策请结合专业判断。
                {report.park.name} · 广东省零碳园区 · {new Date(report.generated_at).toLocaleDateString('zh-CN')}
              </Text>
            </Card>
          ) : (
            <Empty description="选择园区并点击生成按钮，AI将为您生成专业的零碳转型分析报告">
              <div style={{ color: '#6b7d8e', fontSize: 12, marginTop: 8 }}>
                <BulbOutlined /> 支持广东省全部15个省级零碳园区的个性化分析
              </div>
            </Empty>
          )}
        </Col>
      </Row>
    </div>
  )
}
