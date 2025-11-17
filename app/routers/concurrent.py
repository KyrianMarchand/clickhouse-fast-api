"""
Exemple de router avec tests de requêtes simultanées.
"""
from fastapi import APIRouter, Depends
from app.dependencies import get_clickhouse
import asyncio
from datetime import datetime

router = APIRouter(prefix="/concurrent", tags=["concurrent-tests"])

@router.get("/simple-query")
async def simple_concurrent_query(client=Depends(get_clickhouse)):
    """
    Exécute une requête simple. 
    Chaque appel utilise son propre client ClickHouse.
    """
    try:
        result = client.query("SELECT now() as current_time, version() as version")
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "data": result.result_rows[0]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/heavy-query")
async def heavy_concurrent_query(client=Depends(get_clickhouse)):
    """
    Simule une requête lourde pour tester le multithreading.
    """
    try:
        # Requête qui prend du temps (génère des nombres aléatoires)
        result = client.query("""
            SELECT 
                count() as count,
                avg(number) as average,
                max(number) as maximum
            FROM numbers(10000000)
        """)
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "data": {
                "count": result.result_rows[0][0],
                "average": result.result_rows[0][1],
                "maximum": result.result_rows[0][2]
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/test-isolation")
async def test_isolation(delay: int = 1, client=Depends(get_clickhouse)):
    """
    Test l'isolation entre les clients.
    Ajoute un délai pour voir si les autres requêtes sont bloquées.
    
    Usage: Appelez ce endpoint plusieurs fois en parallèle avec différents délais.
    """
    try:
        # Simule un traitement long
        await asyncio.sleep(delay)
        
        result = client.query(f"""
            SELECT 
                '{datetime.now().isoformat()}' as start_time,
                {delay} as delay_seconds,
                now() as query_time
        """)
        
        return {
            "success": True,
            "delay_used": delay,
            "timestamp": datetime.now().isoformat(),
            "data": result.result_rows[0]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
