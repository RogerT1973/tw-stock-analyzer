"""
股票相關 API 路由
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import datetime, timedelta
from backend.data.fetcher import StockDataFetcher
from backend.indicators.calculator import IndicatorCalculator

router = APIRouter(prefix="/api/stocks", tags=["stocks"])
fetcher = StockDataFetcher()

@router.get("/top-volume")
async def get_top_volume_stocks(limit: int = Query(100, ge=1, le=500)):
    """
    獲取成交量最大的前 N 檔股票
    
    Parameters:
    - limit: 篩選數量 (1-500)
    """
    stocks = fetcher.get_top_volume_stocks(limit=limit)
    return {
        "count": len(stocks),
        "stocks": stocks,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/{stock_code}/history")
async def get_stock_history(
    stock_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = Query("1d", regex="^(1d|1wk|1mo)$")
):
    """
    獲取股票歷史數據
    
    Parameters:
    - stock_code: 股票代碼 (例如: 2330)
    - start_date: 開始日期 (YYYY-MM-DD)
    - end_date: 結束日期 (YYYY-MM-DD)
    - interval: 時間間隔 (1d/1wk/1mo)
    """
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    df = fetcher.get_historical_data(stock_code, start_date, end_date, interval)
    
    if df.empty:
        raise HTTPException(status_code=404, detail="股票數據不找")
    
    return {
        "stock_code": stock_code,
        "data_points": len(df),
        "start_date": start_date,
        "end_date": end_date,
        "data": df.to_dict(orient="index")
    }

@router.get("/{stock_code}/indicators")
async def get_stock_indicators(stock_code: str, days: int = Query(365, ge=30, le=1000)):
    """
    獲取股票技術指標
    
    Parameters:
    - stock_code: 股票代碼
    - days: 計算天數
    """
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    df = fetcher.get_historical_data(stock_code, start_date, end_date)
    
    if df.empty:
        raise HTTPException(status_code=404, detail="股票數據不找")
    
    df_with_indicators = IndicatorCalculator.calculate_all_indicators(df)
    
    return {
        "stock_code": stock_code,
        "indicators": df_with_indicators.tail(30).to_dict(orient="index")
    }
