"""
集成預測模型
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from backend.prediction.arima_model import ARIMAPredictor
from backend.prediction.sarima_model import SARIMAPredictor
import logging

logger = logging.getLogger(__name__)

class EnsemblePredictor:
    """集成預測模型，結合多個預測算法"""
    
    def __init__(self):
        self.predictors = {}
        self.weights = {}
    
    def train_all_models(self, data: pd.Series) -> Dict[str, bool]:
        """訓練所有預測模型"""
        results = {}
        
        # ARIMA 模型
        try:
            arima = ARIMAPredictor(order=(1, 1, 1))
            if arima.fit(data):
                self.predictors['ARIMA'] = arima
                results['ARIMA'] = True
            else:
                results['ARIMA'] = False
        except Exception as e:
            logger.error(f"ARIMA 訓練失敗: {e}")
            results['ARIMA'] = False
        
        # SARIMA 模型
        try:
            sarima = SARIMAPredictor(order=(1, 1, 1), seasonal_order=(1, 1, 1, 20))
            if sarima.fit(data):
                self.predictors['SARIMA'] = sarima
                results['SARIMA'] = True
            else:
                results['SARIMA'] = False
        except Exception as e:
            logger.error(f"SARIMA 訓練失敗: {e}")
            results['SARIMA'] = False
        
        return results
    
    def predict_ensemble(self, steps: int = 30, method: str = 'average') -> Dict:
        """
        集成預測
        
        Args:
            steps: 預測步數
            method: 集成方法 ('average', 'weighted', 'median')
        
        Returns:
            預測結果字典
        """
        if not self.predictors:
            logger.error("沒有可用的訓練模型")
            return {}
        
        predictions = {}
        for name, predictor in self.predictors.items():
            pred = predictor.predict(steps)
            if len(pred) > 0:
                predictions[name] = pred
        
        if not predictions:
            return {}
        
        # 集成多個預測
        if method == 'average':
            ensemble_pred = np.mean(list(predictions.values()), axis=0)
        elif method == 'median':
            ensemble_pred = np.median(list(predictions.values()), axis=0)
        elif method == 'weighted':
            weights = self._get_weights()
            ensemble_pred = np.average(
                list(predictions.values()),
                axis=0,
                weights=[weights.get(name, 1.0/len(predictions)) for name in predictions.keys()]
            )
        else:
            ensemble_pred = np.mean(list(predictions.values()), axis=0)
        
        return {
            'ensemble_forecast': ensemble_pred,
            'individual_forecasts': predictions,
            'method': method
        }
    
    def predict_with_confidence(self, steps: int = 30, confidence: float = 0.95) -> Dict:
        """帶有置信區間的預測"""
        result = {}
        
        for name, predictor in self.predictors.items():
            conf = predictor.get_confidence_interval(steps, confidence)
            if conf:
                result[name] = conf
        
        return result
    
    def _get_weights(self) -> Dict[str, float]:
        """獲取模型權重"""
        if self.weights:
            return self.weights
        
        # 默認權重
        return {
            'ARIMA': 0.4,
            'SARIMA': 0.6
        }
    
    def set_weights(self, weights: Dict[str, float]):
        """設置模型權重"""
        self.weights = weights
