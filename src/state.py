from pydantic import BaseModel

from .agents.player import Ray
from .constants import (
    PLAYER_VIEW_FOV,
    PLAYER_NUM_RAYS,
    PLAYER_RAY_LENGTH,
    RAY_TRACER_STEPS,
    PLAYER_SHOOTING_DURATION_TICKS,
    PLAYER_SHOOTING_LENGTH_PER_TICK,
)
from .geometry import Vector2D
from .interfaces import State
from .map import GameMap, PlayerID, PlayerMapData
from .objects import GameObject, CollisionDetector


class AgentStats(BaseModel):
    is_alive: bool = True
    shooting_delay: int = 0  # ticks


class PendingShot(BaseModel):
    player_id: str
    origin: Vector2D
    direction: Vector2D
    remaining_ticks: int = PLAYER_SHOOTING_DURATION_TICKS


class GameState(State):
    tick: int = 0
    map: GameMap
    agent_stats: dict[PlayerID, AgentStats] = {}
    rays: dict[PlayerID, list[Ray]] = {}
    pending_shots: list[PendingShot] = []
    kills: dict[PlayerID, list[PlayerID]] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_stats = kwargs.get(
            "agent_stats",
            {player_id: AgentStats() for player_id in self.map.players.keys()},
        )
        self.rays = kwargs.get(
            "rays",
            {
                player_id: self._compute_rays_for_agent(player_data)
                for player_id, player_data in self.map.players.items()
            },
        )
        self.kills = kwargs.get(
            "kills",
            {player_id: [] for player_id in self.map.players.keys()},
        )

    def _compute_rays_for_agent(self, player_data: PlayerMapData) -> list[Ray]:
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
                return Ray(
                    distance=t / PLAYER_RAY_LENGTH,
                    obj=obj,
                    angle=direction.base_angle(),
                )

        return Ray(distance=1.0, obj=GameObject.NONE, angle=direction.base_angle())

    def _check_collision(
        self, point: Vector2D, player_data: PlayerMapData
    ) -> GameObject:
        for wall in self.map.nearest_walls(point):
            if CollisionDetector.check_collision_point_wall(point, wall):
                return GameObject.WALL

        for other_id, other_data in self.map.players.items():
            if (
                other_id == player_data.player_id
                or not self.agent_stats[other_id].is_alive
            ):
                continue
            if CollisionDetector.check_collision_point_player(
                point, other_data.position
            ):
                return (
                    GameObject.TEAMMATE
                    if other_data.team == player_data.team
                    else GameObject.ENEMY
                )

        return GameObject.NONE

    def agent_data(self, agent_id: str) -> dict:
        return {
            **self.map.players[agent_id].model_dump(),
            **self.agent_stats[agent_id].model_dump(),
        }

    def _compute_updated_bullets(self):
        updated_shots = []

        for shot in self.pending_shots:
            origin = shot.origin
            direction = shot.direction
            end = origin + direction * PLAYER_SHOOTING_LENGTH_PER_TICK

            hit = self._ray_hits_object(origin, end, shot.player_id)
            if not hit and shot.remaining_ticks > 1:
                updated_shots.append(
                    PendingShot(
                        player_id=shot.player_id,
                        origin=end,
                        direction=direction,
                        remaining_ticks=shot.remaining_ticks - 1,
                    )
                )

        return updated_shots

    def _ray_hits_object(
        self, origin: Vector2D, end: Vector2D, shooter_id: str
    ) -> bool:
        for step in range(1, RAY_TRACER_STEPS + 1):
            t = step / RAY_TRACER_STEPS
            point = origin + (end - origin) * t

            for other_id, other_data in self.map.players.items():
                if other_id == shooter_id:
                    continue
                other_stats = self.agent_stats[other_id]
                if not other_stats.is_alive:
                    continue

                if CollisionDetector.check_collision_point_player(
                    point, other_data.position
                ):
                    other_stats.is_alive = False
                    self.kills[shooter_id].append(other_id)
                    return True

            for wall in self.map.nearest_walls(point):
                if CollisionDetector.check_collision_point_wall(point, wall):
                    return True

        return False

    def step(self):
        self.pending_shots = self._compute_updated_bullets()
        for player_id, player_data in self.map.players.items():
            stats = self.agent_stats[player_id]
            if stats.shooting_delay > 0:
                stats.shooting_delay -= 1
            self.rays[player_id] = self._compute_rays_for_agent(player_data)
        self.tick += 1
