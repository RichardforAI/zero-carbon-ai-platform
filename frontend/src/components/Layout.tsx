import { useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { Layout as AntLayout, Menu, Typography } from 'antd'
import {
  DashboardOutlined, SearchOutlined, BankOutlined,
  SettingOutlined, BookOutlined, FileTextOutlined,
  GlobalOutlined,
} from '@ant-design/icons'

const { Sider, Content } = AntLayout

const menuItems = [
  { key: '/dashboard', icon: <DashboardOutlined />, label: '总览仪表盘' },
  { key: '/tools', icon: <SearchOutlined />, label: '工具箱浏览' },
  { key: '/match', icon: <BankOutlined />, label: '园区匹配' },
  { key: '/report', icon: <FileTextOutlined />, label: 'AI报告生成' },
  { key: '/policies', icon: <FileTextOutlined />, label: '政策法规' },
  { key: '/news', icon: <GlobalOutlined />, label: '新闻资讯' },
  { key: '/whitepaper', icon: <BookOutlined />, label: '零碳白皮书' },
]

export default function Layout({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate()
  const location = useLocation()
  const [lastUpdated, setLastUpdated] = useState('')

  const fetchLastUpdated = () => {
    fetch('/api/dashboard')
      .then(r => r.json())
      .then(d => { if (d.last_updated) setLastUpdated(d.last_updated.slice(0, 10)) })
      .catch(() => {})
  }

  useEffect(() => {
    fetchLastUpdated()
    // Listen for custom 'data-updated' event fired after one-click update
    window.addEventListener('data-updated', fetchLastUpdated)
    return () => window.removeEventListener('data-updated', fetchLastUpdated)
  }, [])

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider width={220} style={{
        background: '#151f2b', borderRight: '1px solid #1e2d3d',
        display: 'flex', flexDirection: 'column',
      }}>
        <div style={{ padding: '20px 24px', borderBottom: '1px solid #1e2d3d' }}>
          <Typography.Title level={5} style={{ color: '#40e495', margin: 0 }}>
            零碳园区AI策略平台
          </Typography.Title>
          <Typography.Text style={{ color: '#6b7d8e', fontSize: 11 }}>
            Zero-Carbon AI Tools Platform
          </Typography.Text>
        </div>

        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ background: 'transparent', borderRight: 0, marginTop: 16 }}
          theme="dark"
        />

        <div style={{ marginTop: 'auto', padding: 20, borderTop: '1px solid #1e2d3d' }}>
          <Typography.Text style={{ color: '#4a5c6e', fontSize: 11 }}>
            v1.0.0 · 数据更新于 {lastUpdated || '加载中...'}
          </Typography.Text>
        </div>
      </Sider>

      <Content style={{ padding: '24px 32px', overflow: 'auto', background: '#0f1923' }}>
        {children}
      </Content>
    </AntLayout>
  )
}
