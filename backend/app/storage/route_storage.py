from datetime import datetime
from backend.app.schemas import Route, RouteCreate


class RouteStorage:
    def __init__(self):
        self.routes = []
        self.next_id = 1

    def create_route(self, route: RouteCreate) -> Route:
        new_route = Route(
            id=self.next_id,
            pickup_zone_id=route.pickup_zone_id,
            dropoff_zone_id=route.dropoff_zone_id,
            name=route.name,
            active=True,
            created_at=datetime.utcnow()
        )
        self.routes.append(new_route)
        self.next_id += 1
        return new_route

    def get_routes(self) -> list[Route]:
        return self.routes

    def get_route_by_id(self, route_id: int) -> Route | None:
        for route in self.routes:
            if route.id == route_id:
                return route
        return None

    def find_route(self, pickup_zone_id: int, dropoff_zone_id: int) -> Route | None:
        for route in self.routes:
            if (
                route.pickup_zone_id == pickup_zone_id
                and route.dropoff_zone_id == dropoff_zone_id
            ):
                return route
        return None

    def update_route(self, route_id: int, route_data: RouteCreate) -> Route | None:
        for index, route in enumerate(self.routes):
            if route.id == route_id:
                updated_route = Route(
                    id=route.id,
                    pickup_zone_id=route_data.pickup_zone_id,
                    dropoff_zone_id=route_data.dropoff_zone_id,
                    name=route_data.name,
                    active=route.active,
                    created_at=route.created_at
                )
                self.routes[index] = updated_route
                return updated_route
        return None

    def delete_route(self, route_id: int) -> bool:
        for index, route in enumerate(self.routes):
            if route.id == route_id:
                del self.routes[index]
                return True
        return False
