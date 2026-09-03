import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, Form, Input, Select, InputNumber, Button, Tag, Typography, Space, message, Spin } from 'antd'
import { SaveOutlined, DeleteOutlined, RobotOutlined } from '@ant-design/icons'

const { Title } = Typography
const { TextArea } = Input

// These would normally come from API
const CATEGORIES = [
  { id: 1, name: '预测类' }, { id: 2, name: '优化类' }, { id: 3, name: '控制类' },
  { id: 4, name: '诊断类' }, { id: 5, name: '核算类' }, { id: 6, name: '识别类' },
  { id: 7, name: '调度类' }, { id: 8, name: '知识类' }, { id: 9, name: '创新类' },
]
const PHASES = ['电力/能源管理', '建筑用能优化', '工业生产过程', '设备运维管理', '交通物流', '碳核算与交易', '水资源管理', '废弃物管理', '碳汇管理', '供应链碳管理', '综合规划决策']
const PARK_TYPES = ['先进制造型', '重化工近零碳型', '新能源装备制造型', '新材料型', '临港特色产业型', '生态高新技术型']
const SCENE_TAGS = ['建筑运行', '能源管理', '交通物流', '水资源管理', '废弃物管理', '碳汇管理', '供应链碳管理', '园区综合规划']

export default function ToolEdit() {
  const { id } = useParams<{ id: string }>()
  const isNew = id === 'new' || !id
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [aiLoading, setAiLoading] = useState(false)

  useEffect(() => {
    if (!isNew) {
      setLoading(true)
      fetch(`/api/tools/${id}`).then(r => r.json()).then(d => {
        form.setFieldsValue(d); setLoading(false)
      }).catch(() => setLoading(false))
    }
  }, [id])

  const onSave = async () => {
    const values = form.getFieldsValue()
    const method = isNew ? 'POST' : 'PUT'
    const url = isNew ? '/api/tools' : `/api/tools/${id}`
    const res = await fetch(url, {
      method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(values),
    })
    if (res.ok) {
      message.success(isNew ? '工具创建成功' : '工具更新成功')
      navigate('/tools')
    } else {
      message.error('保存失败')
    }
  }

  const onDelete = async () => {
    if (!confirm('确认删除此工具？')) return
    const res = await fetch(`/api/tools/${id}`, { method: 'DELETE' })
    if (res.ok) { message.success('已删除'); navigate('/tools') }
    else { message.error('删除失败') }
  }

  const onAIGenerate = async () => {
    const name = form.getFieldValue('name')
    if (!name) { message.warning('请先输入工具名称'); return }
    setAiLoading(true)
    const res = await fetch('/api/tools/ai-generate', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, brief_description: form.getFieldValue('description') || name }),
    })
    if (res.ok) {
      const data = await res.json()
      form.setFieldsValue(data)
      message.success('AI已自动填充工具信息')
    } else {
      message.error('AI生成失败，请检查API配置')
    }
    setAiLoading(false)
  }

  if (loading) return <Spin size="large" style={{ display: 'block', marginTop: 60 }} />

  return (
    <div>
      <Title level={3} style={{ color: '#e0e6ed', marginBottom: 20 }}>
        {isNew ? '新增AI工具' : '编辑AI工具'}
      </Title>

      <Card style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
        <Form form={form} layout="vertical" initialValues={{ maturity: 3, case_count: 0, version: '1.0' }}>
          {/* Basic info */}
          <Title level={5} style={{ color: '#40e495' }}>基本信息</Title>
          <Form.Item name="name" label="工具名称" rules={[{ required: true }]}>
            <Input placeholder="例如：智慧水务AI监测与优化" />
          </Form.Item>
          <Space size={16}>
            <Form.Item name="category_id" label="分类">
              <Select style={{ width: 160 }} options={CATEGORIES.map(c => ({ value: c.id, label: c.name }))} />
            </Form.Item>
            <Form.Item name="maturity" label="成熟度(1-5)">
              <InputNumber min={1} max={5} />
            </Form.Item>
            <Form.Item name="case_count" label="案例数">
              <InputNumber min={0} />
            </Form.Item>
            <Form.Item name="version" label="版本">
              <Input style={{ width: 80 }} />
            </Form.Item>
          </Space>

          {/* Rich text fields */}
          <Title level={5} style={{ color: '#40e495', marginTop: 20 }}>详细描述</Title>
          <Form.Item name="description" label="工具描述">
            <TextArea rows={3} placeholder="该AI工具的功能和特点..." />
          </Form.Item>
          <Form.Item name="scenario" label="适用场景">
            <TextArea rows={2} placeholder="什么情况下使用该工具..." />
          </Form.Item>
          <Form.Item name="ai_method" label="AI赋能方式">
            <TextArea rows={2} placeholder="如何利用AI技术实现..." />
          </Form.Item>

          <Title level={5} style={{ color: '#40e495', marginTop: 20 }}>技术与适用信息</Title>
          <Form.Item name="tech_path" label="技术路径（逗号分隔）">
            <Input placeholder="LSTM时序预测, XGBoost梯度提升, Transformer模型" />
          </Form.Item>
          <Form.Item name="value_props" label="价值主张（逗号分隔）">
            <Input placeholder="预测精度MAPE<5%, 降低需量电费10-20%" />
          </Form.Item>
          <Form.Item name="prerequisites" label="前置条件">
            <TextArea rows={2} placeholder="所需数据、系统、人员条件..." />
          </Form.Item>
          <Form.Item name="implementation_tips" label="实施建议">
            <TextArea rows={2} />
          </Form.Item>

          <Space size={16} wrap>
            <Form.Item name="operation_phase" label="运营环节">
              <Select style={{ width: 180 }} options={PHASES.map(p => ({ value: p, label: p }))} />
            </Form.Item>
            <Form.Item name="applicable_park_types" label="适用园区类型（逗号分隔）">
              <Input placeholder="先进制造型, 重化工近零碳型" style={{ width: 300 }} />
            </Form.Item>
            <Form.Item name="scene_tags" label="场景标签（逗号分隔）">
              <Input placeholder="建筑运行, 能源管理" style={{ width: 300 }} />
            </Form.Item>
          </Space>

          {/* Action buttons */}
          <div style={{ marginTop: 24, display: 'flex', gap: 12 }}>
            <Button type="primary" icon={<SaveOutlined />} onClick={onSave} size="large">
              {isNew ? '创建工具' : '保存修改'}
            </Button>
            {isNew && (
              <Button icon={<RobotOutlined />} onClick={onAIGenerate} loading={aiLoading} size="large"
                style={{ background: '#5b9cf5', borderColor: '#5b9cf5', color: '#fff' }}>
                AI辅助填充
              </Button>
            )}
            {!isNew && (
              <Button danger icon={<DeleteOutlined />} onClick={onDelete} size="large">删除工具</Button>
            )}
            <Button onClick={() => navigate('/tools')} size="large">取消</Button>
          </div>
        </Form>
      </Card>
    </div>
  )
}
