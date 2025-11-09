from fastapi import APIRouter, Depends

from app.dependencies import get_clickhouse

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/clickhouse-status")
async def clickhouse_status(client=Depends(get_clickhouse)):
    try:
        result = client.query("SELECT version()")
        version = result.result_rows[0][0]
        return {"clickhouse_connected": True, "version": version}
    except Exception as e:
        return {"clickhouse_connected": False, "error": str(e)}
