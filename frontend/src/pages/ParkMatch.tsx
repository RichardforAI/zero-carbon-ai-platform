import { useEffect, useState } from 'react'
import { Card, Select, Button, Tag, Row, Col, Typography, Spin, Space, Empty, Tabs, Progress, Alert } from 'antd'
import { ThunderboltOutlined, StarFilled, RobotOutlined, BulbOutlined } from '@ant-design/icons'
import { api, ParkItem, MatchResult, AgentMatchResult } from '../api/client'

const { Text, Title } = Typography

export default function ParkMatch() {
  const [parks, setParks] = useState<ParkItem[]>([])
  const [selectedPark, setSelectedPark] = useState<number | null>(null)
  const [parksLoading, setParksLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'rule' | 'ai'>('rule')

  // Rule-based state
  const [ruleResult, setRuleResult] = useState<MatchResult | null>(null)
  const [ruleLoading, setRuleLoading] = useState(false)

  // AI state
  const [aiResult, setAiResult] = useState<AgentMatchResult | null>(null)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError] = useState<string | null>(null)

  useEffect(() => {
    api.getParks().then(d => { setParks(d); setParksLoading(false) })
  }, [])

  const doRuleMatch = () => {
    if (!selectedPark) return
    setRuleLoading(true)
    setRuleResult(null)
    api.matchPark(selectedPark).then(d => { setRuleResult(d); setRuleLoading(false) })
  }

  const doAiMatch = () => {
    if (!selectedPark) return
    setAiLoading(true)
    setAiResult(null)
    setAiError(null)
    api.agentMatch(selectedPark)
      .then(d => { setAiResult(d); setAiLoading(false) })
      .catch(e => { setAiError(e.message); setAiLoading(false) })
  }

  const stars = (m: number) => '★'.repeat(m) + '☆'.repeat(5 - m)

  const priorityColor = (p: string) => {
    if (p === 'immediate') return '#f5706a'
    if (p === 'short_term') return '#f5c842'
    return '#5b9cf5'
  }

  const priorityLabel = (p: string) => {
    if (p === 'immediate') return '立即部署'
    if (p === 'short_term') return '短期规划'
    return '长期储备'
  }

  return (
    <div>
      <Title level={3} style={{ color: '#e0e6ed', marginBottom: 20 }}>
        <BulbOutlined /> 园区-AI工具智能匹配
      </Title>

      <Row gutter={24}>
        <Col span={6}>
          <Card title="选择目标园区" style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
            <Select
              showSearch
              placeholder="选择园区..."
              style={{ width: '100%', marginBottom: 12 }}
              loading={parksLoading}
              options={parks.map(p => ({ value: p.id, label: `${p.name} (${p.park_type})` }))}
              onChange={v => setSelectedPark(v)}
              filterOption={(input, option) => (option?.label as string)?.includes(input)}
            />
            <Tabs
              activeKey={activeTab}
              onChange={k => setActiveTab(k as 'rule' | 'ai')}
              size="small"
              items={[
                {
                  key: 'rule',
                  label: <span>规则匹配</span>,
                },
                {
                  key: 'ai',
                  label: <span><RobotOutlined /> AI智能匹配</span>,
                },
              ]}
              style={{ marginBottom: 8 }}
            />
            {activeTab === 'rule' ? (
              <Button type="primary" block onClick={doRuleMatch} loading={ruleLoading} icon={<ThunderboltOutlined />}>
                规则匹配AI工具
              </Button>
            ) : (
              <Button type="primary" block onClick={doAiMatch} loading={aiLoading} icon={<RobotOutlined />}
                style={{ background: '#5b9cf5', borderColor: '#5b9cf5' }}>
                AI智能匹配分析
              </Button>
            )}
          </Card>
        </Col>

        <Col span={18}>
          {/* Rule-based results */}
          {activeTab === 'rule' && (
            ruleLoading ? <Spin size="large" style={{ display: 'block', marginTop: 60 }} /> : ruleResult ? (
              <>
                <Title level={5} style={{ color: '#f5c842', marginBottom: 12 }}>
                  <StarFilled /> 核心推荐（{ruleResult.core_recommendations.length}个）
                </Title>
                <Row gutter={[12, 12]} style={{ marginBottom: 24 }}>
                  {ruleResult.core_recommendations.map(t => (
                    <Col span={12} key={t.id}>
                      <Card style={{ background: '#1a1a15', borderColor: '#f5c842', height: '100%' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                          <Text strong style={{ color: '#fff' }}>{t.name}</Text>
                          <span style={{ color: '#f5c842', fontSize: 11 }}>{stars(t.maturity)}</span>
                        </div>
                        <Space size={4}>
                          <Tag color="blue" style={{ fontSize: 9 }}>{t.category_name}</Tag>
                          <span style={{ color: '#6b7d8e', fontSize: 10 }}>{t.case_count} 案例</span>
                        </Space>
                      </Card>
                    </Col>
                  ))}
                </Row>
                <Title level={5} style={{ color: '#c0ccd8', marginBottom: 12 }}>
                  通用推荐（{ruleResult.general_recommendations.length}个）
                </Title>
                <Row gutter={[12, 12]}>
                  {ruleResult.general_recommendations.map(t => (
                    <Col span={12} key={t.id}>
                      <Card style={{ background: '#151f2b', borderColor: '#1e2d3d', height: '100%' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                          <Text strong style={{ color: '#fff' }}>{t.name}</Text>
                          <span style={{ color: '#5b9cf5', fontSize: 11 }}>{stars(t.maturity)}</span>
                        </div>
                        <Space size={4}>
                          <Tag color="blue" style={{ fontSize: 9 }}>{t.category_name}</Tag>
                          <span style={{ color: '#6b7d8e', fontSize: 10 }}>{t.case_count} 案例</span>
                        </Space>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </>
            ) : (
              <Empty description="请选择一个园区开始匹配" />
            )
          )}

          {/* AI results */}
          {activeTab === 'ai' && (
            aiLoading ? (
              <div style={{ textAlign: 'center', marginTop: 60 }}>
                <Spin size="large" />
                <div style={{ color: '#6b7d8e', marginTop: 16 }}>
                  <RobotOutlined style={{ fontSize: 24, marginRight: 8 }} />
                  AI正在分析园区特征并匹配最优工具...
                </div>
                <div style={{ color: '#4a5d6e', marginTop: 8, fontSize: 12 }}>
                  正在评估{parks.find(p => p.id === selectedPark)?.name || '...'}与20个AI工具的匹配度
                </div>
              </div>
            ) : aiError ? (
              <Alert
                type="error"
                message="AI匹配失败"
                description={aiError}
                showIcon
                style={{ marginTop: 40 }}
                action={<Button size="small" onClick={doAiMatch}>重试</Button>}
              />
            ) : aiResult ? (
              <>
                {/* Match reasoning + confidence */}
                <Card style={{ background: '#151f2b', borderColor: '#5b9cf5', marginBottom: 20 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                    <Text strong style={{ color: '#5b9cf5', fontSize: 14 }}>
                      <RobotOutlined /> AI匹配分析
                    </Text>
                    <Tag color="blue" style={{ fontSize: 12 }}>
                      置信度: {(aiResult.confidence * 100).toFixed(0)}%
                    </Tag>
                  </div>
                  <Text style={{ color: '#c0ccd8', fontSize: 13, lineHeight: 1.8 }}>
                    {aiResult.match_reasoning}
                  </Text>
                </Card>

                {/* Core recommendations */}
                <Title level={5} style={{ color: '#f5c842', marginBottom: 12 }}>
                  <StarFilled /> 核心推荐（{aiResult.core_recommendations.length}个）
                </Title>
                <Row gutter={[12, 12]} style={{ marginBottom: 24 }}>
                  {aiResult.core_recommendations.map(t => (
                    <Col span={12} key={t.tool_id}>
                      <Card style={{ background: '#1a1a15', borderColor: '#f5c842', height: '100%' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                          <Text strong style={{ color: '#fff' }}>{t.tool_name}</Text>
                          <Space size={4}>
                            <Tag color={priorityColor(t.implementation_priority)} style={{ fontSize: 9 }}>
                              {priorityLabel(t.implementation_priority)}
                            </Tag>
                            <span style={{ color: '#f5c842', fontSize: 11 }}>{stars(t.maturity)}</span>
                          </Space>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                          <Space size={4}>
                            <Tag color="blue" style={{ fontSize: 9 }}>{t.category_name}</Tag>
                          </Space>
                          <Text style={{ color: '#40e495', fontSize: 12, fontWeight: 'bold' }}>
                            匹配度: {t.relevance_score}%
                          </Text>
                        </div>
                        <Text style={{ color: '#6b7d8e', fontSize: 11, lineHeight: 1.6 }}>
                          💡 {t.reasoning}
                        </Text>
                      </Card>
                    </Col>
                  ))}
                </Row>

                {/* General recommendations */}
                <Title level={5} style={{ color: '#c0ccd8', marginBottom: 12 }}>
                  通用推荐（{aiResult.general_recommendations.length}个）
                </Title>
                <Row gutter={[12, 12]}>
                  {aiResult.general_recommendations.map(t => (
                    <Col span={12} key={t.tool_id}>
                      <Card style={{ background: '#151f2b', borderColor: '#1e2d3d', height: '100%' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                          <Text strong style={{ color: '#fff' }}>{t.tool_name}</Text>
                          <Space size={4}>
                            <Tag color={priorityColor(t.implementation_priority)} style={{ fontSize: 9 }}>
                              {priorityLabel(t.implementation_priority)}
                            </Tag>
                            <span style={{ color: '#5b9cf5', fontSize: 11 }}>{stars(t.maturity)}</span>
                          </Space>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                          <Space size={4}>
                            <Tag color="blue" style={{ fontSize: 9 }}>{t.category_name}</Tag>
                          </Space>
                          <Text style={{ color: '#5b9cf5', fontSize: 12, fontWeight: 'bold' }}>
                            匹配度: {t.relevance_score}%
                          </Text>
                        </div>
                        <Text style={{ color: '#6b7d8e', fontSize: 11, lineHeight: 1.6 }}>
                          💡 {t.reasoning}
                        </Text>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </>
            ) : (
              <Empty description="请选择园区，点击AI智能匹配分析">
                <div style={{ color: '#6b7d8e', fontSize: 12, marginTop: 8 }}>
                  AI将基于园区特征进行深度推理匹配，提供个性化的工具推荐和理由说明
                </div>
              </Empty>
            )
          )}
        </Col>
      </Row>
    </div>
  )
}
