"""
回測驗證模組
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class BacktestEngine:
    """回測引擎"""
    
    def __init__(self, initial_capital: float = 1000000):
        """
        初始化回測引擎
        
        Args:
            initial_capital: 初始資本 (新台幣)
        """
        self.initial_capital = initial_capital
        self.portfolio = initial_capital
        self.trades = []
        self.performance = {}
    
    def backtest_simple_strategy(
        self,
        prices: pd.Series,
        signals: pd.Series
    ) -> Dict:
        """
        簡單的回測策略 (買賣信號)
        
        Args:
            prices: 股票價格序列
            signals: 買賣信號 (1=買, -1=賣, 0=持有)
        
        Returns:
            回測結果
        """
        portfolio_values = [self.initial_capital]
        positions = 0
        entry_price = 0
        
        for i, (price, signal) in enumerate(zip(prices, signals)):
            if signal == 1 and positions == 0:  # 買入
                positions = self.initial_capital / price
                entry_price = price
                self.trades.append({
                    'type': 'BUY',
                    'price': price,
                    'date': prices.index[i],
                    'amount': self.initial_capital
                })
            
            elif signal == -1 and positions > 0:  # 賣出
                profit = (price - entry_price) * positions
                self.trades.append({
                    'type': 'SELL',
                    'price': price,
                    'date': prices.index[i],
                    'profit': profit
                })
                self.portfolio = self.initial_capital + profit
                positions = 0
            
            # 更新投資組合價值
            current_value = self.initial_capital if positions == 0 else positions * price
            portfolio_values.append(current_value)
        
        return self._calculate_metrics(portfolio_values, prices)
    
    def _calculate_metrics(self, portfolio_values: List, prices: pd.Series) -> Dict:
        """計算回測績效指標"""
        portfolio_values = np.array(portfolio_values)
        returns = np.diff(portfolio_values) / portfolio_values[:-1]
        
        total_return = (portfolio_values[-1] - self.initial_capital) / self.initial_capital
        annual_return = (1 + total_return) ** (252 / len(portfolio_values)) - 1
        volatility = np.std(returns) * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0
        
        max_drawdown = self._calculate_max_drawdown(portfolio_values)
        win_rate = len([t for t in self.trades if t.get('profit', 0) > 0]) / max(len([t for t in self.trades if t['type'] == 'SELL']), 1)
        
        return {
            'total_return': total_return,
            'annual_return': annual_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'trades': self.trades,
            'final_portfolio_value': portfolio_values[-1]
        }
    
    @staticmethod
    def _calculate_max_drawdown(portfolio_values: np.ndarray) -> float:
        """計算最大回落"""
        running_max = np.maximum.accumulate(portfolio_values)
        drawdown = (portfolio_values - running_max) / running_max
        return np.min(drawdown)
