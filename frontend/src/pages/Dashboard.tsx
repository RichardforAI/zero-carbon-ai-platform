import { useEffect, useState } from 'react'
import { Row, Col, Card, Statistic, Tag, Spin, Typography, Button, Modal, message, Space } from 'antd'
import { ArrowUpOutlined, SyncOutlined, CheckCircleOutlined } from '@ant-design/icons'
import ReactEChartsCore from 'echarts-for-react/lib/core'
import * as echarts from 'echarts/core'
import { PieChart, BarChart, RadarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, PolarComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { api, DashboardData } from '../api/client'

echarts.use([PieChart, BarChart, RadarChart, GridComponent, TooltipComponent, LegendComponent, PolarComponent, CanvasRenderer])

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [updating, setUpdating] = useState(false)
  const [updateResult, setUpdateResult] = useState<any>(null)

  const fetchDashboard = () => {
    api.getDashboard().then(d => { setData(d); setLoading(false) })
  }

  useEffect(() => { fetchDashboard() }, [])

  const handleUpdate = async () => {
    setUpdating(true)
    try {
      const result = await api.triggerUpdate(['policies', 'tools', 'cases', 'news'], 2)
      setUpdateResult(result)
      if (result.status === 'ok') {
        message.success(`更新完成：新增${result.summary.new_policies}条政策、${result.summary.new_tools}个工具、${result.summary.new_cases}个案例、${result.summary.new_news}条新闻`)
      }
      fetchDashboard()
      // Notify Layout to refresh the "数据更新于" timestamp
      window.dispatchEvent(new Event('data-updated'))
    } catch (e: any) {
      message.error('更新失败: ' + (e.message || '未知错误'))
    }
    setUpdating(false)
  }

  if (loading || !data) return <Spin size="large" style={{ display: 'block', marginTop: 80 }} />

  const { kpi, category_distribution, park_type_coverage, maturity_radar, recent_updates } = data

  const pieOption = {
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie', radius: ['45%', '72%'], center: ['50%', '55%'],
      label: { color: '#8899aa', fontSize: 10, formatter: '{b}\n{d}%' },
      data: category_distribution.map(c => ({ value: c.count, name: c.name, itemStyle: { color: c.color } })),
    }],
  }

  const barOption = {
    tooltip: { trigger: 'axis' },
    legend: { textStyle: { color: '#8899aa', fontSize: 10 }, top: 0 },
    grid: { left: 40, right: 20, top: 35, bottom: 25 },
    xAxis: { type: 'category', data: park_type_coverage.map(p => p.park_type.replace('型', '')), axisLabel: { color: '#8899aa', fontSize: 9 } },
    yAxis: { type: 'value', axisLabel: { color: '#8899aa', fontSize: 9 }, splitLine: { lineStyle: { color: '#1e2d3d' } } },
    series: [
      { name: '高成熟度', type: 'bar', stack: 'a', data: park_type_coverage.map(p => p.high_maturity), itemStyle: { color: '#40e495' } },
      { name: '中成熟度', type: 'bar', stack: 'a', data: park_type_coverage.map(p => p.medium_maturity), itemStyle: { color: '#f5c842' } },
      { name: '低成熟度', type: 'bar', stack: 'a', data: park_type_coverage.map(p => p.low_maturity), itemStyle: { color: '#f5706a' } },
    ],
  }

  const radarOption = {
    radar: {
      center: ['50%', '55%'], radius: '60%',
      indicator: maturity_radar.map(r => ({ name: r.phase, max: 5 })),
      axisName: { color: '#8899aa', fontSize: 9 },
    },
    series: [{
      type: 'radar',
      data: [{ value: maturity_radar.map(r => r.avg_maturity), name: '成熟度', areaStyle: { color: 'rgba(64,228,149,0.15)' }, lineStyle: { color: '#40e495' }, itemStyle: { color: '#40e495' } }],
    }],
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <Typography.Title level={3} style={{ color: '#e0e6ed', margin: 0 }}>总览仪表盘</Typography.Title>
        <Space>
          <Button type="primary" icon={<SyncOutlined spin={updating} />} onClick={handleUpdate} loading={updating}
            style={{background:'#a78bfa',borderColor:'#a78bfa',fontWeight:'bold'}}>
            一键更新
          </Button>
          <Tag color="green">园区管理者视图</Tag>
        </Space>
      </div>

      {/* Update Result Modal */}
      <Modal title={<span><CheckCircleOutlined style={{color:'#40e495'}}/> 一键更新结果</span>}
        open={!!updateResult} onCancel={() => setUpdateResult(null)} footer={null} width={500}>
        {updateResult && (
          <div>
            <p style={{color:'#6b7d8e',marginBottom:16}}>
              更新模式：<Tag color={updateResult.mode === 'llm' ? 'purple' : 'orange'}>{updateResult.mode === 'llm' ? '🤖 AI生成' : '📦 Demo模式'}</Tag>
            </p>
            <Row gutter={[12,12]} style={{marginBottom:16}}>
              {[{k:'new_policies',label:'政策',icon:'📋'},{k:'new_tools',label:'工具',icon:'🔧'},{k:'new_cases',label:'案例',icon:'📊'},{k:'new_news',label:'新闻',icon:'📰'}].map(item => (
                <Col span={6} key={item.k}>
                  <Card size="small" style={{background:'#1e2d3d',borderColor:'#2a3d4d',textAlign:'center'}}>
                    <div style={{fontSize:24,fontWeight:'bold',color:'#40e495'}}>{(updateResult.summary || {})[item.k] || 0}</div>
                    <div style={{fontSize:11,color:'#6b7d8e'}}>{item.icon} {item.label}</div>
                  </Card>
                </Col>
              ))}
            </Row>
            {(updateResult.details || []).length > 0 && (
              <div style={{maxHeight:200,overflow:'auto'}}>
                {updateResult.details.map((d:any,i:number) => (
                  <div key={i} style={{padding:'4px 0',borderBottom:'1px solid #1e2d3d',fontSize:12}}>
                    <Tag color={d.action==='created'?'green':'red'}>{d.action==='created'?'新增':'失败'}</Tag>
                    <span style={{color:'#c0ccd8'}}>[{d.module}] {d.title}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </Modal>

      <Row gutter={[16, 16]} style={{ marginBottom: 20 }}>
        {[
          { title: 'AI工具总数', value: kpi.total_tools, suffix: `+${kpi.new_this_month} 本月` },
          { title: '覆盖场景数', value: kpi.total_scenarios, suffix: '个运营场景' },
          { title: '应用案例', value: kpi.total_cases, suffix: '个商业平台' },
          { title: '园区类型覆盖', value: `${kpi.park_types_covered}/6`, suffix: '全类型覆盖' },
          { title: '运营环节覆盖', value: `${kpi.operation_phases_covered}/11`, suffix: '全环节覆盖' },
        ].map((k, i) => (
          <Col span={i < 3 ? 8 : 12} key={k.title}>
            <Card style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
              <Statistic
                title={<span style={{ color: '#6b7d8e', fontSize: 12 }}>{k.title}</span>}
                value={k.value}
                valueStyle={{ color: '#fff', fontSize: 32, fontWeight: 700 }}
                suffix={<span style={{ fontSize: 11, color: '#40e495' }}>{k.suffix}</span>}
              />
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={[16, 16]} style={{ marginBottom: 20 }}>
        <Col span={8}>
          <Card title={<span style={{ color: '#c0ccd8' }}>AI工具类型分布</span>} style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
            <ReactEChartsCore echarts={echarts} option={pieOption} style={{ height: 280 }} />
          </Card>
        </Col>
        <Col span={8}>
          <Card title={<span style={{ color: '#c0ccd8' }}>各类型园区AI工具覆盖</span>} style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
            <ReactEChartsCore echarts={echarts} option={barOption} style={{ height: 280 }} />
          </Card>
        </Col>
        <Col span={8}>
          <Card title={<span style={{ color: '#c0ccd8' }}>技术成熟度雷达图</span>} style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
            <ReactEChartsCore echarts={echarts} option={radarOption} style={{ height: 280 }} />
          </Card>
        </Col>
      </Row>

      {/* Building scene section */}
      <Row gutter={[16, 16]} style={{ marginBottom: 20 }}>
        <Col span={24}>
          <Card
            title={<span style={{ color: '#40e495' }}>建筑运行场景 AI应用分析</span>}
            style={{ background: '#151f2b', borderColor: '#40e495' }}
          >
            <Row gutter={16}>
              <Col span={6}>
                <Statistic title={<span style={{ color: '#6b7d8e' }}>建筑场景AI工具</span>} value={data.building_scene_stats?.tool_count || 0} suffix="个" valueStyle={{ color: '#40e495', fontSize: 28 }} />
              </Col>
              <Col span={6}>
                <Statistic title={<span style={{ color: '#6b7d8e' }}>覆盖运营环节</span>} value={data.building_scene_stats?.phase_count || 0} suffix="个" valueStyle={{ color: '#40e495', fontSize: 28 }} />
              </Col>
              <Col span={6}>
                <Statistic title={<span style={{ color: '#6b7d8e' }}>应用案例</span>} value={data.building_scene_stats?.case_count || 0} suffix="个" valueStyle={{ color: '#40e495', fontSize: 28 }} />
              </Col>
              <Col span={6}>
                <div style={{ color: '#8899aa', fontSize: 11, lineHeight: 1.8 }}>
                  <strong style={{ color: '#c0ccd8' }}>覆盖环节：</strong><br />
                  {(data.building_scene_stats?.phases || []).join('、')}
                </div>
              </Col>
            </Row>
            <div style={{ marginTop: 12 }}>
              <Typography.Text style={{ color: '#6b7d8e', fontSize: 11 }}>
                建筑运行是园区AI应用的重要场景。建筑运行过程中积累的能耗、设备运行等数据，可为AI分析和策略推荐提供基础支撑。
                平台已将建筑运行作为重点研究场景之一，用户可在工具箱浏览中通过"应用场景→建筑运行"筛选相关AI工具。
              </Typography.Text>
            </div>
          </Card>
        </Col>
      </Row>

      <Card title={<span style={{ color: '#c0ccd8' }}>最新更新动态</span>} style={{ background: '#151f2b', borderColor: '#1e2d3d' }}>
        {recent_updates.map(u => (
          <div key={u.id} style={{ padding: '8px 0', borderBottom: '1px solid #1e2d3d' }}>
            <Tag color={u.change_type === 'new' ? 'green' : u.change_type === 'update' ? 'blue' : 'orange'} style={{ fontSize: 10 }}>
              {u.change_type === 'new' ? '新增' : u.change_type === 'update' ? '更新' : '案例'}
            </Tag>
            <span style={{ color: '#6b7d8e', fontSize: 11, marginRight: 12 }}>
              {u.created_at?.slice(0, 10)}
            </span>
            <span style={{ color: '#b0bec5', fontSize: 12 }}>{u.description}</span>
          </div>
        ))}
      </Card>
    </div>
  )
}
