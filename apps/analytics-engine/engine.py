import logging
import uuid
import time
import pandas as pd
import numpy as np

class FinOpsAnalyticsEngine:
    def __init__(self):
        self.logger = logging.getLogger("finops-culture-engine")

    def detect_anomalies(self, daily_spend: list, sensitivity: float = 2.0):
        """
        Detects spend anomalies using a simple rolling standard deviation model.
        """
        if len(daily_spend) < 7:
            return []
            
        df = pd.DataFrame(daily_spend, columns=['spend'])
        df['rolling_mean'] = df['spend'].rolling(window=7).mean()
        df['rolling_std'] = df['spend'].rolling(window=7).std()
        
        df['anomaly'] = (df['spend'] > df['rolling_mean'] + (sensitivity * df['rolling_std']))
        
        anomalies = df[df['anomaly'] == True].to_dict('records')
        return anomalies

    def calculate_maturity_score(self, visibility_pct: float, accountability_pct: float, optimization_pct: float):
        """
        Calculates the FinOps maturity score (0-100) based on visibility, accountability, and optimization.
        """
        score = (visibility_pct * 0.3) + (accountability_pct * 0.4) + (optimization_pct * 0.3)
        return round(score * 100, 1)

    def forecast_spend(self, historical_spend: list, days: int = 30):
        """
        Simple linear trend forecasting for future cloud spend.
        """
        if len(historical_spend) < 30:
            return {"status": "INSUFFICIENT_DATA"}
            
        x = np.arange(len(historical_spend))
        y = np.array(historical_spend)
        
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        future_x = np.arange(len(historical_spend), len(historical_spend) + days)
        future_y = p(future_x)
        
        return {
            "forecast_total": round(np.sum(future_y), 2),
            "trend": "UP" if z[0] > 0 else "DOWN",
            "daily_forecast": future_y.tolist()
        }

    def benchmark_team_ownership(self, teams_data: list):
        """
        Benchmarks teams based on their budget adherence and optimization response time.
        """
        # Logic: Score teams by (1 - variance) and (optimization response)
        for team in teams_data:
            variance = abs(team['spend'] - team['budget']) / team['budget'] if team['budget'] > 0 else 0
            team['ownership_score'] = round((1 - min(variance, 1)) * 100, 1)
            
        return sorted(teams_data, key=lambda x: x['ownership_score'], reverse=True)

if __name__ == "__main__":
    engine = FinOpsAnalyticsEngine()
    
    # 1. Anomaly Detection
    history = [100, 105, 98, 110, 102, 108, 105, 500] # Spike at the end
    print("Anomalies:", engine.detect_anomalies(history))
    
    # 2. Maturity Score
    print("Maturity Score:", engine.calculate_maturity_score(0.9, 0.6, 0.8))
    
    # 3. Forecasting
    trend = [100 + i for i in range(30)]
    print("Forecast:", engine.forecast_spend(trend, 7))
    
    # 4. Team Benchmarking
    teams = [
        {"name": "Team A", "spend": 120, "budget": 100},
        {"name": "Team B", "spend": 95, "budget": 100}
    ]
    print("Team Benchmarks:", engine.benchmark_team_ownership(teams))
