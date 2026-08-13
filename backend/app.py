"""
主應用程式
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.config import config
from backend.utils.logger import setup_logging, get_logger
from backend.routes import stocks, predictions

# 設置日誌
setup_logging()
logger = get_logger(__name__)

# 創建 FastAPI 應用
app = FastAPI(
    title=config.APP_NAME,
    description="台股智能分析系統 API",
    version="0.1.0"
)

# CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康檢查
@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "ok", "service": config.APP_NAME}

# 根端點
@app.get("/")
async def root():
    """根端點"""
    return {
        "message": "歡迎使用台股智能分析系統",
        "version": "0.1.0",
        "docs": "/docs"
    }

# 包含路由
app.include_router(stocks.router)
app.include_router(predictions.router)

# 錯誤處理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"未處理的異常: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "伺服器內部錯誤"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
