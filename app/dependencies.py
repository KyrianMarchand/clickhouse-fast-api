from app.database import clickhouse_client

def get_clickhouse():
    return clickhouse_client.get_client()
