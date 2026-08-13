import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Layout } from 'antd'
import Dashboard from './pages/Dashboard'
import StockAnalysis from './pages/StockAnalysis'
import Predictions from './pages/Predictions'
import './App.css'

const { Header, Content, Footer } = Layout

function App() {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ background: '#001529', color: '#fff' }}>
          <h1>台股智能分析系統</h1>
        </Header>
        <Content style={{ padding: '50px' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analysis/:stockCode" element={<StockAnalysis />} />
            <Route path="/predictions" element={<Predictions />} />
          </Routes>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          TW Stock Analyzer ©2024
        </Footer>
      </Layout>
    </Router>
  )
}

export default App