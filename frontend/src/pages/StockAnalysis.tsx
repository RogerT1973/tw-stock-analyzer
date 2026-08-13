import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Card, Spin, Row, Col } from 'antd'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import axios from 'axios'

interface ChartData {
  date: string
  close: number
  ma20: number
  rsi: number
}

function StockAnalysis() {
  const { stockCode } = useParams<{ stockCode: string }>()
  const [data, setData] = useState<ChartData[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchStockData()
  }, [stockCode])

  const fetchStockData = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`/api/stocks/${stockCode}/indicators`)
      setData(response.data.indicators || [])
    } catch (error) {
      console.error('獲取指標數據失敗:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2>股票分析 - {stockCode}</h2>
      <Spin spinning={loading}>
        <Row gutter={16}>
          <Col xs={24}>
            <Card title="價格走勢與技術指標">
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="close" stroke="#1890ff" name="收盤價" />
                  <Line type="monotone" dataKey="ma20" stroke="#ff7a45" name="MA20" />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </Col>
        </Row>
      </Spin>
    </div>
  )
}

export default StockAnalysis