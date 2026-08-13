"""
預測模型模組 - SARIMA
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import logging

logger = logging.getLogger(__name__)

class SARIMAPredictor:
    """SARIMA 預測模型 (季節性 ARIMA)"""
    
    def __init__(self, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)):
        """
        初始化 SARIMA 模型
        
        Args:
            order: (p, d, q) 元組
            seasonal_order: (P, D, Q, s) 元組，s 為季節週期
        """
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None
        self.fitted_model = None
    
    def fit(self, data: pd.Series) -> bool:
        """擬合 SARIMA 模型"""
        try:
            self.model = SARIMAX(
                data,
                order=self.order,
                seasonal_order=self.seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            self.fitted_model = self.model.fit(disp=False)
            return True
        except Exception as e:
            logger.error(f"SARIMA 模型擬合失敗: {e}")
            return False
    
    def predict(self, steps: int = 30) -> np.ndarray:
        """預測未來價格"""
        if self.fitted_model is None:
            logger.error("模型未擬合")
            return np.array([])
        
        try:
            forecast = self.fitted_model.get_forecast(steps=steps)
            return forecast.predicted_mean.values
        except Exception as e:
            logger.error(f"SARIMA 預測失敗: {e}")
            return np.array([])
    
    def get_confidence_interval(self, steps: int = 30, confidence: float = 0.95) -> dict:
        """獲取預測置信區間"""
        if self.fitted_model is None:
            return {}
        
        try:
            forecast_result = self.fitted_model.get_forecast(steps=steps)
            conf_int = forecast_result.conf_int(alpha=1-confidence)
            
            return {
                'forecast': forecast_result.predicted_mean.values,
                'lower': conf_int.iloc[:, 0].values,
                'upper': conf_int.iloc[:, 1].values
            }
        except Exception as e:
            logger.error(f"獲取置信區間失敗: {e}")
            return {}
