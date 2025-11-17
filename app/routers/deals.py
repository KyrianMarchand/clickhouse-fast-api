from fastapi import APIRouter, Depends
from app.dependencies import get_clickhouse_client
from app.models.deal import Deal, DealFilter
from datetime import date, datetime
from typing import Any, Dict, Tuple, get_args, get_origin

router = APIRouter(prefix="/deals", tags=["deals"])

def get_field_type(model, field_name: str):
    if field_name in model.model_fields:
        field_type = model.model_fields[field_name].annotation
        origin = get_origin(field_type)
        if origin is type(None.__class__) or (get_args(field_type) and type(None) in get_args(field_type)):
            return get_args(field_type)[0] if get_args(field_type) else field_type
        return field_type
    return None

def build_clickhouse_query(filters, table_name: str = "deals") -> Tuple[str, Dict[str, Any]]:
    conditions = []
    params = {}
    
    filter_dict = filters.model_dump(exclude_unset=True, exclude={'limit'})
    
    for field, value in filter_dict.items():
        if value is None:
            continue
            
        field_lower = field.lower()
        field_type = get_field_type(Deal, field_lower.replace('_min', '').replace('_max', '').replace('_from', '').replace('_to', ''))
        
        if field_lower.endswith('_min'):
            base_field = field_lower.replace('_min', '')
            conditions.append(f"{base_field} >= %({field_lower})s")
            params[field_lower] = value
            
        elif field_lower.endswith('_max'):
            base_field = field_lower.replace('_max', '')
            conditions.append(f"{base_field} <= %({field_lower})s")
            params[field_lower] = value
            
        elif field_lower.endswith('_from'):
            base_field = field_lower.replace('_from', '')
            conditions.append(f"{base_field} >= %({field_lower})s")
            if isinstance(value, (date, datetime)):
                params[field_lower] = value.isoformat()
            else:
                params[field_lower] = value
                
        elif field_lower.endswith('_to'):
            base_field = field_lower.replace('_to', '')
            conditions.append(f"{base_field} <= %({field_lower})s")
            if isinstance(value, (date, datetime)):
                params[field_lower] = value.isoformat()
            else:
                params[field_lower] = value
        else:
            if field_type == str or isinstance(value, str):
                conditions.append(f"lower({field_lower}) LIKE lower(%({field_lower})s)")
                params[field_lower] = f"%{value}%"
            elif field_type in (date, datetime) or isinstance(value, (date, datetime)):
                conditions.append(f"{field_lower} = %({field_lower})s")
                params[field_lower] = value.isoformat()
            elif field_type in (int, float) or isinstance(value, (int, float)):
                conditions.append(f"{field_lower} = %({field_lower})s")
                params[field_lower] = value
            else:
                conditions.append(f"{field_lower} = %({field_lower})s")
                params[field_lower] = str(value)
    
    query = f"SELECT * FROM {table_name}"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    limit = filters.limit or 100
    query += f" LIMIT {limit}"
    
    return query, params

@router.post("/search")
def search_deals(filters: DealFilter, client=Depends(get_clickhouse_client)):
    query, params = build_clickhouse_query(filters)
    result = client.query(query, parameters=params)
    return {
        "query": query,
        "params": params,
        "data": result.result_rows,
        "columns": result.column_names
    }
