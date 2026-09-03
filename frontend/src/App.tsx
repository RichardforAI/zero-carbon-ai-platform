import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ToolList from './pages/ToolList'
import ToolDetail from './pages/ToolDetail'
import ParkMatch from './pages/ParkMatch'
import Report from './pages/Report'
import Policies from './pages/Policies'
import ToolEdit from './pages/ToolEdit'
import Whitepaper from './pages/Whitepaper'
import News from './pages/News'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/tools" element={<ToolList />} />
        <Route path="/tools/:id" element={<ToolDetail />} />
        <Route path="/tools/:id/edit" element={<ToolEdit />} />
        <Route path="/tools/new" element={<ToolEdit />} />
        <Route path="/match" element={<ParkMatch />} />
        <Route path="/report" element={<Report />} />
        <Route path="/policies" element={<Policies />} />
        <Route path="/whitepaper" element={<Whitepaper />} />
        <Route path="/news" element={<News />} />
      </Routes>
    </Layout>
  )
}
