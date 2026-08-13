# 台股智能分析系統 (TW Stock Analyzer)

利用 KD、MACD、RSI、MA、布林通道、ARIMA、SARIMA 等技術指標和機器學習模型，分析台股全市場普通股上市上櫃股票，預測 3 個月、6 個月及 1 年的最高獲利前五檔股票。

## 功能特性

- ✅ 每日篩選成交量最大 100 檔股票
- ✅ 多種技術指標分析（KD、MACD、RSI、MA、布林通道）
- ✅ ARIMA/SARIMA 時間序列預測
- ✅ 3/6/12 個月綜合獲利預估
- ✅ 歷史回測驗證
- ✅ 網頁儀表板
- ✅ Windows EXE 桌面應用
- ✅ Android 行動應用

## 項目結構

```
tw-stock-analyzer/
├── backend/                    # Python 後端
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── data/                   # 數據爬蟲和存儲
│   ├── indicators/             # 技術指標計算
│   ├── prediction/             # 預測模型
│   ├── backtesting/            # 回測驗證
│   ├── routes/                 # API 路由
│   └── utils/                  # 工具函數
├── frontend/                   # React 網頁
├── desktop/                    # Electron 桌面應用
├── mobile/                     # React Native Android
└── docs/                       # 文檔
```

## 開發進度

### Phase 1: 網頁版 (進行中 🔄)
- [x] 項目初始化
- [ ] 後端數據爬蟲
- [ ] 技術指標計算
- [ ] 預測模型
- [ ] FastAPI 服務
- [ ] React 儀表板

### Phase 2: EXE 桌面應用
- [ ] Electron 框架
- [ ] 打包為 EXE

### Phase 3: Android 應用
- [ ] React Native UI
- [ ] 打包為 APK

## 技術棧

| 層級 | 技術 |
|------|------|
| 後端 | Python, FastAPI |
| 數據處理 | Pandas, NumPy, TA-Lib |
| 網頁前端 | React, TypeScript, Ant Design |
| 桌面應用 | Electron |
| 移動端 | React Native, Expo |

## 許可證

MIT License
