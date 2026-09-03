import { useState, useRef, useCallback } from 'react'
import { Card, Button, Typography, Spin, Space, message } from 'antd'
import { BookOutlined, ThunderboltOutlined, FilePdfOutlined } from '@ant-design/icons'
import html2pdf from 'html2pdf.js'

const { Title } = Typography

export default function Whitepaper() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [exporting, setExporting] = useState(false)
  const [htmlContent, setHtmlContent] = useState('')
  const contentRef = useRef<HTMLDivElement>(null)

  const generate = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/whitepaper')
      if (!res.ok) throw new Error('API error: ' + res.status)
      const json = await res.json()
      setData(json)
      let html = `<div class="wp-header"><h2>${json.title}</h2><p>数据更新：${json.last_updated}</p></div>`
      for (const ch of json.chapters || []) {
        html += `<h3 class="wp-chapter">${ch.title}</h3>`
        let content = ch.content || ''
        content = content.replace(/### (.+)/g, '<h5>$1</h5>')
        content = content.replace(/## (.+)/g, '<h4>$1</h4>')
        content = content.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        content = content.replace(/\n- (.+)/g, '\n<li>$1</li>')
        content = content.replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>')
        content = content.replace(/\n\n/g, '</p><p>')
        content = '<p>' + content + '</p>'
        html += content
      }
      html += '<hr class="wp-footer-hr"><p class="wp-footer">本白皮书由 AI赋能零碳园区策略平台 自动生成 · ' + json.last_updated + '</p>'
      setHtmlContent(html)
    } catch (e: any) {
      message.error('生成失败: ' + (e.message || '未知错误'))
    }
    setLoading(false)
  }

  const exportPdf = useCallback(async () => {
    if (!contentRef.current) return
    setExporting(true)
    try {
      const el = contentRef.current
      const opt = {
        margin:       15,
        filename:     `零碳园区白皮书_${data?.last_updated || '2026'}.pdf`,
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, backgroundColor: '#ffffff', logging: false },
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' },
      }
      await (html2pdf as any)().set(opt).from(el).save()
      message.success('白皮书PDF已导出！')
    } catch (e: any) {
      message.error('PDF导出失败: ' + (e.message || '未知错误'))
    }
    setExporting(false)
  }, [data])

  return (
    <div>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:20}}>
        <Title level={3} style={{color:'#e0e6ed',margin:0}}><BookOutlined/> 零碳园区白皮书</Title>
        <Space>
          {data && (
            <Button type="primary" icon={<FilePdfOutlined/>} onClick={exportPdf} loading={exporting}
              style={{background:'#f5706a',borderColor:'#f5706a',fontWeight:'bold'}}>
              一键导出PDF
            </Button>
          )}
          <Button type="primary" size="large" icon={<ThunderboltOutlined/>} onClick={generate} loading={loading}
            style={{background:'#40e495',borderColor:'#40e495',color:'#0f1923',fontWeight:'bold'}}>
            {data ? '重新生成' : '一键生成白皮书'}
          </Button>
        </Space>
      </div>

      {loading ? (
        <div style={{textAlign:'center',padding:80}}>
          <Spin size="large"/>
          <div style={{color:'#6b7d8e',marginTop:16}}>正在从平台数据库聚合内容...</div>
        </div>
      ) : data ? (
        <Card style={{background:'#151f2b',borderColor:'#1e2d3d'}}>
          <div ref={contentRef}
            dangerouslySetInnerHTML={{__html:htmlContent}}
            style={{maxWidth:900,margin:'0 auto',color:'#c0ccd8',lineHeight:1.9}}/>
        </Card>
      ) : (
        <Card style={{background:'#151f2b',borderColor:'#1e2d3d',textAlign:'center',padding:60}}>
          <BookOutlined style={{fontSize:48,color:'#4a5d6e',marginBottom:16}}/>
          <div style={{color:'#c0ccd8',fontSize:16,marginBottom:8}}>点击上方按钮，一键生成《AI赋能零碳园区建设白皮书》</div>
          <div style={{color:'#6b7d8e',fontSize:13}}>白皮书基于平台实时数据聚合生成，包含六大章节：概述、政策环境、园区分类、AI工具体系、案例实践、实施建议</div>
        </Card>
      )}

      {/* Print/PDF-optimized styles */}
      <style>{`
        @media print {
          body * { visibility: hidden; }
          #pdf-content, #pdf-content * { visibility: visible; }
          #pdf-content { position: absolute; left: 0; top: 0; width: 100%; }
        }
        .wp-header { text-align:center; padding-bottom:20px; border-bottom:3px solid #1a3a2a; margin-bottom:28px; }
        .wp-header h2 { color:#0f5c2e; margin-bottom:6px; font-size:22px; }
        .wp-header p { color:#666; font-size:12px; }
        .wp-chapter { color:#0f5c2e; border-bottom:2px solid #d9d9d9; padding-bottom:6px; margin:22px 0 14px; font-size:17px; }
        h4 { color:#1a1a1a; margin:18px 0 10px; font-size:15px; }
        h5 { color:#333; margin:12px 0 6px; font-size:13px; }
        p { color:#333; line-height:1.9; font-size:13px; margin-bottom:6px; text-align:justify; }
        ul { color:#333; padding-left:18px; margin:6px 0; line-height:1.8; }
        li { margin-bottom:2px; }
        strong { color:#0f5c2e; }
        .wp-footer-hr { border-color:#d9d9d9; margin-top:28px; }
        .wp-footer { color:#999; font-size:11px; text-align:center; }
      `}</style>
    </div>
  )
}
