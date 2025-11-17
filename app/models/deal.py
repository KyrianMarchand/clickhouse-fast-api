from pydantic import BaseModel, create_model
from typing import Optional, get_args, get_origin
from datetime import date, datetime
from enum import Enum

class DealStatus(str, Enum):
    pending = "pending"
    active = "active"
    closed = "closed"
    cancelled = "cancelled"

class Deal(BaseModel):
    id: int
    name: str
    amount: float
    discount: Optional[float] = None
    quantity: int
    status: DealStatus
    created_date: date
    updated_at: datetime
    description: Optional[str] = None

def create_filter_fields():
    fields = {}
    for field_name, field_info in Deal.model_fields.items():
        field_type = field_info.annotation
        
        if get_origin(field_type) is Optional:
            base_type = get_args(field_type)[0]
        else:
            base_type = field_type
        
        fields[field_name] = (Optional[base_type], None)
        
        if base_type in (int, float):
            fields[f"{field_name}_min"] = (Optional[base_type], None)
            fields[f"{field_name}_max"] = (Optional[base_type], None)
        elif base_type in (date, datetime):
            fields[f"{field_name}_from"] = (Optional[base_type], None)
            fields[f"{field_name}_to"] = (Optional[base_type], None)
    
    fields["limit"] = (Optional[int], 100)
    return fields

DealFilter = create_model("DealFilter", **create_filter_fields())
