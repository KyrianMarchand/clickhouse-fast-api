import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

CLICKHOUSE_CONFIG = {
    "host": os.getenv("CLICKHOUSE_HOST", "localhost"),
    "port": int(os.getenv("CLICKHOUSE_PORT", "8123")),
    "username": os.getenv("CLICKHOUSE_USER", "default"),
    "password": os.getenv("CLICKHOUSE_PASSWORD", ""),
    "database": os.getenv("CLICKHOUSE_DATABASE", "default")
}

def get_clickhouse_client():
    return clickhouse_connect.get_client(**CLICKHOUSE_CONFIG)
