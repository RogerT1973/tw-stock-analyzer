"""
預測相關 API 路由
"""

from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timedelta
from backend.data.fetcher import StockDataFetcher
from backend.prediction.ensemble import EnsemblePredictor

router = APIRouter(prefix="/api/predictions", tags=["predictions"])
fetcher = StockDataFetcher()

@router.get("/{stock_code}/forecast")
async def get_stock_forecast(
    stock_code: str,
    days: int = Query(90, ge=30, le=365),
    period: int = Query(30, ge=10, le=90)
):
    """
    獲取股票價格預測
    
    Parameters:
    - stock_code: 股票代碼
    - days: 用於訓練的歷史天數
    - period: 預測天數
    """
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    df = fetcher.get_historical_data(stock_code, start_date, end_date)
    
    if df.empty:
        raise HTTPException(status_code=404, detail="股票數據不找")
    
    # 訓練預測模型
    predictor = EnsemblePredictor()
    train_results = predictor.train_all_models(df['Close'])
    
    # 獲取預測
    forecast = predictor.predict_ensemble(steps=period, method='weighted')
    confidence = predictor.predict_with_confidence(steps=period, confidence=0.95)
    
    return {
        "stock_code": stock_code,
        "training_period": days,
        "forecast_period": period,
        "last_price": float(df['Close'].iloc[-1]),
        "forecast": forecast.get('ensemble_forecast', []).tolist(),
        "confidence_intervals": {
            name: {
                "forecast": conf['forecast'].tolist(),
                "lower": conf['lower'].tolist(),
                "upper": conf['upper'].tolist()
            }
            for name, conf in confidence.items()
        },
        "training_success": train_results,
        "timestamp": datetime.now().isoformat()
    }
