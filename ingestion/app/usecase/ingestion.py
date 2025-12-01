from app.interface.weather_api import WeatherApiClientPort
from app.interface.repository import WeatherRepositoryPort

class WeatherIngestionService:
    def __init__(self, api_client: WeatherApiClientPort, repo: WeatherRepositoryPort):
        self.api_client = api_client
        self.repo = repo

    def execute(self, start_date: str, end_date: str):
        print(f"--- Bắt đầu Ingestion Hexagonal ({start_date} -> {end_date}) ---")
        
        # 1. Gọi Port API để lấy dữ liệu (Domain Objects)
        data = self.api_client.fetch_daily_data(start_date, end_date)
        
        if not data:
            print("Không có dữ liệu trả về.")
            return

        print(f"-> Đã lấy được {len(data)} bản ghi từ API.")


        # 2. Gọi Port Repository để lưu
        self.repo.save_bulk(data)
        
        print("-> Ingestion hoàn tất.")