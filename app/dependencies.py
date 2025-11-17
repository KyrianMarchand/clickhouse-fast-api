from app.database import get_clickhouse_client

def get_clickhouse():
    client = get_clickhouse_client()
    try:
        yield client
    finally:
        client.close()
