from typing import List
from fastapi import FastAPI, HTTPException

from backend.app.schemas import Zone, ZoneCreate
from backend.app.storage.zone_storage import ZoneStorage
from backend.app.schemas import RouteCreate, Route
from backend.app.storage.route_storage import RouteStorage


app = FastAPI(title="Demand Prediction Service")

zone_storage = ZoneStorage()
route_storage = RouteStorage()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/zones", response_model=Zone)
def create_zone(zone: ZoneCreate):
    return zone_storage.create_zone(zone)

@app.post("/zones", response_model=Zone)
def create_zone(zone: ZoneCreate):
    if not zone.borough or not zone.zone_name or not zone.service_zone:
        raise HTTPException(status_code=400, detail="All fields are required")
    return zone_storage.create_zone(zone)



@app.get("/zones", response_model=List[Zone])
def list_zones():
    return zone_storage.get_zones()


@app.get("/zones/{zone_id}", response_model=Zone)
def get_zone(zone_id: int):
    zone = zone_storage.get_zone_by_id(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone

@app.put("/zones/{zone_id}", response_model=Zone)
def update_zone(zone_id: int, zone: ZoneCreate):
    updated = zone_storage.update_zone(zone_id, zone)
    if not updated:
        raise HTTPException(status_code=404, detail="Zone not found")
    return updated

@app.delete("/zones/{zone_id}")
def delete_zone(zone_id: int):
    deleted = zone_storage.delete_zone(zone_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Zone not found")
    return {"message": "Zone deleted successfully"}

@app.delete("/zones/{zone_id}", status_code=204)
def delete_zone(zone_id: int):
    if not delete_zone(zone_id):
        raise HTTPException(status_code=404, detail="Zone not found")

@app.post("/routes", response_model=Route)
def create_route(route: RouteCreate):
    if route.pickup_zone_id == route.dropoff_zone_id:
        raise HTTPException(400, "pickup_zone_id and dropoff_zone_id must be different")

    if not zone_storage.get_zone_by_id(route.pickup_zone_id):
        raise HTTPException(400, "pickup_zone_id does not exist")

    if not zone_storage.get_zone_by_id(route.dropoff_zone_id):
        raise HTTPException(400, "dropoff_zone_id does not exist")

    return route_storage.create_route(route)

from fastapi import UploadFile, File, Form


@app.post("/uploads/trips-parquet")
def upload_trips_parquet(
    file: UploadFile = File(...),
    mode: str = Form(...),
    limit_rows: int = Form(50000),
    top_n_routes: int = Form(50),
):
    if not file.filename.endswith(".parquet"):
        raise HTTPException(status_code=400, detail="Only .parquet files are allowed")

    return {
        "file_name": file.filename,
        "rows_read": 0,
        "zones_created": 0,
        "zones_updated": 0,
        "routes_detected": 0,
        "routes_created": 0,
        "routes_updated": 0,
        "errors": []
    }
