import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基礎配置"""
    
    # 應用設置
    APP_NAME = "TW Stock Analyzer API"
    DEBUG = os.getenv("DEBUG", "False") == "True"
    
    # 服務器設置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # 數據庫
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./tw_stocks.db"
    )
    
    # Redis (可選用於緩存)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # API 密鑰
    API_KEY = os.getenv("API_KEY", "your-secret-key")
    
    # 台股數據設置
    STOCK_MARKETS = ["TWSE", "TPEX"]  # 上市、上櫃
    TOP_VOLUME_STOCKS = 100  # 篩選成交量最大檔數
    
    # 回測設置
    BACKTEST_PERIODS = [3, 6, 12]  # 月數
    
    # 預測模型
    PREDICTION_MODELS = ["ARIMA", "SARIMA"]
    
    # 技術指標
    INDICATORS = [
        "KD",
        "MACD",
        "RSI",
        "MA",
        "BOLLINGER"
    ]
    
    # 日誌設置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = "logs"
    
    # 數據更新
    UPDATE_FREQUENCY = "daily"  # daily or real-time
    UPDATE_TIME = "16:00"  # 市場收盤時間
    
    # 技術指標參數
    MA_PERIODS = [5, 10, 20, 50, 200]
    RSI_PERIOD = 14
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    BOLLINGER_PERIOD = 20
    BOLLINGER_STD = 2

config = Config()
