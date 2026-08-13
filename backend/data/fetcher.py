"""
台股數據爬蟲模組
使用 yfinance 和 requests 獲取台股數據
"""

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class StockDataFetcher:
    """台股數據爬蟲"""
    
    def __init__(self):
        self.twse_url = "https://www.twse.com.tw/rwd/zh/cData/"
        self.market_data = {}
    
    def get_top_volume_stocks(self, date: str = None, limit: int = 100) -> List[str]:
        """
        獲取指定日期成交量最大的前N檔股票
        
        Args:
            date: 日期 (YYYYMMDD格式)，如果為None則使用最近交易日
            limit: 篩選數量，默認100檔
        
        Returns:
            股票代碼列表
        """
        try:
            if date is None:
                date = datetime.now().strftime("%Y%m%d")
            
            # 台灣證券交易所 API
            url = f"{self.twse_url}t21sc03_{date}.csv"
            
            response = requests.get(url, timeout=10)
            response.encoding = 'big5'
            
            # 解析 CSV
            df = pd.read_csv(
                pd.io.common.StringIO(response.text),
                header=None,
                skiprows=2
            )
            
            # 提取股票代碼和成交量
            if len(df) > 0:
                df.columns = ['code', 'name', 'trade_volume', 'trade_value', 'open', 'high', 'low', 'close', 'change']
                
                # 按成交量排序
                df['trade_volume'] = pd.to_numeric(df['trade_volume'], errors='coerce')
                top_stocks = df.dropna(subset=['trade_volume']).nlargest(limit, 'trade_volume')
                
                return top_stocks['code'].tolist()
        
        except Exception as e:
            logger.error(f"獲取成交量排行失敗: {e}")
            return []
    
    def get_historical_data(
        self, 
        stock_code: str, 
        start_date: str, 
        end_date: str,
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        獲取股票歷史數據
        
        Args:
            stock_code: 股票代碼 (例如: 2330.TW)
            start_date: 開始日期 (YYYY-MM-DD)
            end_date: 結束日期 (YYYY-MM-DD)
            interval: 時間間隔 (1d, 1wk, 1mo)
        
        Returns:
            含 OHLCV 的 DataFrame
        """
        try:
            # 確保股票代碼格式正確
            if not stock_code.endswith('.TW'):
                stock_code = f"{stock_code}.TW"
            
            # 使用 yfinance 獲取數據
            df = yf.download(
                stock_code,
                start=start_date,
                end=end_date,
                interval=interval,
                progress=False
            )
            
            if df.empty:
                logger.warning(f"未能獲取 {stock_code} 的數據")
                return pd.DataFrame()
            
            # 重新命名列名
            df.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            df.index.name = 'Date'
            
            return df
        
        except Exception as e:
            logger.error(f"獲取 {stock_code} 數據失敗: {e}")
            return pd.DataFrame()
    
    def get_latest_price(self, stock_code: str) -> Dict:
        """
        獲取股票最新價格
        
        Args:
            stock_code: 股票代碼
        
        Returns:
            包含價格信息的字典
        """
        try:
            if not stock_code.endswith('.TW'):
                stock_code = f"{stock_code}.TW"
            
            ticker = yf.Ticker(stock_code)
            data = ticker.history(period='1d')
            
            if data.empty:
                return {}
            
            latest = data.iloc[-1]
            return {
                'code': stock_code.replace('.TW', ''),
                'close': latest['Close'],
                'high': latest['High'],
                'low': latest['Low'],
                'volume': latest['Volume'],
                'timestamp': data.index[-1]
            }
        
        except Exception as e:
            logger.error(f"獲取 {stock_code} 最新價格失敗: {e}")
            return {}
    
    def get_batch_historical_data(
        self,
        stock_codes: List[str],
        start_date: str,
        end_date: str
    ) -> Dict[str, pd.DataFrame]:
        """
        批量獲取多檔股票歷史數據
        
        Args:
            stock_codes: 股票代碼列表
            start_date: 開始日期
            end_date: 結束日期
        
        Returns:
            {股票代碼: DataFrame}
        """
        result = {}
        
        for code in stock_codes:
            df = self.get_historical_data(code, start_date, end_date)
            if not df.empty:
                result[code.replace('.TW', '')] = df
        
        return result
    
    def prepare_data_for_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        準備用於分析的數據
        
        Args:
            df: 原始 OHLCV 數據
        
        Returns:
            清潔後的 DataFrame
        """
        df = df.copy()
        
        # 刪除缺失值
        df = df.dropna()
        
        # 確保數值類型
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
        df['High'] = pd.to_numeric(df['High'], errors='coerce')
        df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
        
        return df.dropna()
