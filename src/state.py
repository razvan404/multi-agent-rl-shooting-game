from .agents.player_agent import PlayerAgent, Ray
from .constants import (
    PLAYER_VIEW_FOV,
    PLAYER_NUM_RAYS,
    PLAYER_RAY_LENGTH,
    RAY_TRACER_STEPS,
)
from .geometry import Vector2D
from .interfaces import State
from .map import GameMap, PlayerID, PlayerMapData
from .objects import GameObject, game_object_size


class GameState(State):
    tick: int = 0
    agents: dict[PlayerID, PlayerAgent]
    map: GameMap
    rays: dict[PlayerID, list[Ray]] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rays = {
            player_id: self._compute_rays_for_agent(player_id, player_data)
            for player_id, player_data in self.map.players.items()
        }

    def _compute_rays_for_agent(
        self, player_id: PlayerID, player_data: PlayerMapData
    ) -> list[Ray]:
        origin = player_data.position
        direction = player_data.direction
        if direction is None:
            raise ValueError("Invalid direction for one of the agents.")

        base_angle = direction.base_angle()
        start_angle = base_angle - (PLAYER_VIEW_FOV / 2)
        angle_step = PLAYER_VIEW_FOV / (PLAYER_NUM_RAYS - 1)

        rays = []
        for i in range(PLAYER_NUM_RAYS):
            angle = start_angle + i * angle_step
            ray_dir = Vector2D.from_angle(angle)
            ray = self._cast_single_ray(origin, ray_dir, player_data)
            rays.append(ray)

        return rays

    def _cast_single_ray(
        self, origin: Vector2D, direction: Vector2D, player_data: PlayerMapData
    ) -> Ray:
        for step in range(1, RAY_TRACER_STEPS + 1):
            t = (step / RAY_TRACER_STEPS) * PLAYER_RAY_LENGTH
            point = origin + direction * t

            obj = self._check_collision(point, player_data)
            if obj != GameObject.NONE:
                return Ray(distance=t / PLAYER_RAY_LENGTH, obj=obj)

        return Ray(distance=1.0, obj=GameObject.NONE)

    def _check_collision(
        self, point: Vector2D, player_data: PlayerMapData
    ) -> GameObject:
        for wall in self.map.walls:
            if self._check_collision_point_cell(point, wall, GameObject.WALL):
                return GameObject.WALL

        for other_id, other_data in self.map.players.items():
            if other_id == player_data.player_id:
                continue
            other_obj_type = (
                GameObject.TEAMMATE
                if other_data.team == player_data.team
                else GameObject.ENEMY
            )
            if self._check_collision_point_cell(
                point, other_data.position, other_obj_type
            ):
                return other_obj_type

        return GameObject.NONE

    @classmethod
    def _check_collision_point_cell(
        cls, point: Vector2D, cell: Vector2D, obj: GameObject
    ) -> bool:
        size = game_object_size(obj)
        return (
            cell.x - size / 2 <= point.x <= cell.x + size / 2
            and cell.y - size / 2 <= point.y <= cell.y + size / 2
        )

    def agent_map_data(self, agent_id: str) -> PlayerMapData:
        return self.map.players[agent_id]
