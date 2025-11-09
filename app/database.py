import clickhouse_connect

from app.config import settings

class ClickHouseClient:
    def __init__(self):
        self.client = None
    
    def get_client(self):
        if not self.client:
            self.client = clickhouse_connect.get_client(
                host=settings.clickhouse_host,
                port=settings.clickhouse_port,
                username=settings.clickhouse_user,
                password=settings.clickhouse_password,
                database=settings.clickhouse_database
            )
        return self.client
    
    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None

clickhouse_client = ClickHouseClient()
