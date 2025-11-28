import pandas as pd
from app.interface.repository import AnalysisRepositoryPort
from app.domain.model import WeatherAggregate, CorrelationMatrix

class AnalysisService:
    def __init__(self, repo: AnalysisRepositoryPort):
        self.repo = repo

    def run_analysis(self):
        print(">>> [UseCase] Starting Analysis ETL...")
        
        # 1. Get Data
        df = self.repo.get_raw_data()
        if df.empty:
            print(">>> [UseCase] No data found.")
            return

        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)

        # 2. Transform: Aggregates (Weekly & Monthly)
        granularities = {'W': 'Tuần', 'ME': 'Tháng'}
        
        for freq, name in granularities.items():
            # Chỉ aggregate các cột tồn tại
            agg_rules = {
                'temp_max': 'mean', 'temp_min': 'mean',
                'rain_sum': 'sum', 'humidity_max': 'mean',
                'wind_speed_max': 'max', 'radiation_sum': 'sum'
            }
            valid_rules = {k: v for k, v in agg_rules.items() if k in df.columns}
            
            if not valid_rules: continue

            agg_df = df.resample(freq).agg(valid_rules).dropna()
            
            # Convert DF -> Domain Objects
            domain_list = []
            for date_idx, row in agg_df.iterrows():
                item = WeatherAggregate(
                    date=date_idx.date(),
                    granularity=freq,
                    temp_max_avg=float(row.get('temp_max', 0)),
                    temp_min_avg=float(row.get('temp_min', 0)),
                    rain_sum=float(row.get('rain_sum', 0)),
                    humidity_avg=float(row.get('humidity_max', 0)),
                    wind_speed_max=float(row.get('wind_speed_max', 0)),
                    radiation_sum=float(row.get('radiation_sum', 0))
                )
                domain_list.append(item)
            
            # Save via Port
            self.repo.save_aggregates(domain_list)

        # 3. Transform: Correlation
        corr_cols = ['temp_max', 'humidity_max', 'rain_sum', 'wind_speed_max', 'radiation_sum']
        valid_cols = [c for c in corr_cols if c in df.columns]
        
        if valid_cols:
            matrix_df = df[valid_cols].corr()

            # C1
            domain_matrix = CorrelationMatrix(matrix=matrix_df.to_dict())
            self.repo.save_correlation(domain_matrix)
            # C2
            ## Chuyển ma trận tương quan thành dạng "long format"
            # corr_long = matrix_df.stack().reset_index()
            # corr_long.columns = ['column_1', 'column_2', 'correlation_value']

            # # Lọc các cặp cột đối xứng (tránh trùng lặp như temp_max với temp_max)
            # corr_long = corr_long[corr_long['column_1'] < corr_long['column_2']]
                        
        print(">>> [UseCase] Analysis Completed.")