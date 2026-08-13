import { useState, useEffect } from 'react'
import { Table, Card, Row, Col, Statistic, Spin } from 'antd'
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons'
import axios from 'axios'

interface Stock {
  code: string
  name: string
  price: number
  change: number
  changePercent: number
}

function Dashboard() {
  const [stocks, setStocks] = useState<Stock[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchTopVolumeStocks()
  }, [])

  const fetchTopVolumeStocks = async () => {
    setLoading(true)
    try {
      const response = await axios.get('/api/stocks/top-volume?limit=50')
      setStocks(response.data.stocks || [])
    } catch (error) {
      console.error('獲取股票數據失敗:', error)
    } finally {
      setLoading(false)
    }
  }

  const columns = [
    {
      title: '股票代碼',
      dataIndex: 'code',
      key: 'code',
    },
    {
      title: '股票名稱',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '現價',
      dataIndex: 'price',
      key: 'price',
    },
    {
      title: '漲跌',
      dataIndex: 'change',
      key: 'change',
      render: (text: number) => (
        <span style={{ color: text > 0 ? '#cf1322' : '#3f8600' }}>
          {text > 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
          {Math.abs(text).toFixed(2)}
        </span>
      ),
    },
  ]

  return (
    <div>
      <h2>市場概況</h2>
      <Row gutter={16} style={{ marginBottom: '30px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic title="成交量排行" value={stocks.length} />
          </Card>
        </Col>
      </Row>

      <Card title="成交量最大前50檔股票" loading={loading}>
        <Table
          columns={columns}
          dataSource={stocks.map((stock, index) => ({
            ...stock,
            key: index,
          }))}
          pagination={{ pageSize: 10 }}
        />
      </Card>
    </div>
  )
}

export default Dashboard