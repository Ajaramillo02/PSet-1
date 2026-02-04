from pydantic import BaseModel, field_validator
from datetime import datetime


# Lo que el CLIENTE envía
class ZoneCreate(BaseModel):
    borough: str
    zone_name: str
    service_zone: str


# Lo que el BACKEND devuelve
class Zone(ZoneCreate):
    id: int
    active: bool = True
    created_at: datetime


class RouteCreate(BaseModel):
    pickup_zone_id: int
    dropoff_zone_id: int
    name: str

    @field_validator("pickup_zone_id", "dropoff_zone_id")
    @classmethod
    def positive_ids(cls, v):
        if v <= 0:
            raise ValueError("IDs must be positive")
        return v

    @field_validator("name")
    @classmethod
    def name_length(cls, v):
        if len(v) < 3:
            raise ValueError("Name too short")
        return v


class Route(RouteCreate):
    id: int
    active: bool = True
    created_at: datetime
