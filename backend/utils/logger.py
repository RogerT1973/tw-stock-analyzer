"""
日誌配置
"""

import logging
import os
from pathlib import Path
from backend.config import config

def setup_logging():
    """設置日誌"""
    log_dir = Path(config.LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'app.log'),
            logging.StreamHandler()
        ]
    )

def get_logger(name: str):
    """獲取 logger"""
    return logging.getLogger(name)
