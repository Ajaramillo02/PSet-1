from datetime import datetime
from backend.app.schemas import Zone, ZoneCreate


class ZoneStorage:
    def __init__(self):
        self.zones = []
        self.next_id = 1

    def create_zone(self, zone: ZoneCreate) -> Zone:
        new_zone = Zone(
            id=self.next_id,
            borough=zone.borough,
            zone_name=zone.zone_name,
            service_zone=zone.service_zone,
            active=True,
            created_at=datetime.utcnow()
        )
        self.zones.append(new_zone)
        self.next_id += 1
        return new_zone

    def get_zones(self) -> list[Zone]:
        return self.zones

    def get_zone_by_id(self, zone_id: int) -> Zone | None:
        for zone in self.zones:
            if zone.id == zone_id:
                return zone
        return None

    def update_zone(self, zone_id: int, zone_data: ZoneCreate) -> Zone | None:
        for index, zone in enumerate(self.zones):
            if zone.id == zone_id:
                updated_zone = Zone(
                    id=zone.id,
                    borough=zone_data.borough,
                    zone_name=zone_data.zone_name,
                    service_zone=zone_data.service_zone,
                    active=zone.active,
                    created_at=zone.created_at
                )
                self.zones[index] = updated_zone
                return updated_zone
        return None

    def delete_zone(self, zone_id: int) -> bool:
        for index, zone in enumerate(self.zones):
            if zone.id == zone_id:
                del self.zones[index]
                return True
        return False
