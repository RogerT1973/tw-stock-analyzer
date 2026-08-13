# 台股智能分析系統 - 後端

## 功能模組

### 數據爬蟲 (`data/`)
- `fetcher.py`: 從 yfinance 獲取台股數據
  - 獲取成交量最大的股票
  - 獲取歷史 OHLCV 數據
  - 批量數據處理

### 技術指標 (`indicators/`)
- `calculator.py`: 計算多種技術指標
  - 移動平均線 (MA)
  - 隨機指標 (KD)
  - 相對強弱指標 (RSI)
  - MACD
  - 布林通道 (Bollinger Bands)
  - 波動率

### 預測模型 (`prediction/`)
- `arima_model.py`: ARIMA 時間序列預測
- `sarima_model.py`: 季節性 ARIMA 預測
- `ensemble.py`: 集成多個預測模型

### 回測 (`backtesting/`)
- `backtest.py`: 策略回測引擎
  - 計算收益率、夏普比率、最大回落
  - 支持簡單買賣信號

### API 路由 (`routes/`)
- `stocks.py`: 股票數據 API
  - `/api/stocks/top-volume`: 成交量排行
  - `/api/stocks/{code}/history`: 歷史數據
  - `/api/stocks/{code}/indicators`: 技術指標

- `predictions.py`: 預測 API
  - `/api/predictions/{code}/forecast`: 價格預測

## 安裝

```bash
pip install -r requirements.txt
```

## 運行

```bash
python app.py
```

或使用 uvicorn：

```bash
uvicorn backend.app:app --reload
```

## API 文檔

應用運行後訪問 http://localhost:8000/docs
