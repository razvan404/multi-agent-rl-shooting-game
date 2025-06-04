import random
from abc import ABC

from src.actions import WaitAction
from src.objects import GameObject, Ray
from src.geometry import Vector2D
from src.state import AgentStats

from .percept import ModeratorPercept
from ..communication_agent import CommunicationAgent


class ModeratorAgent(CommunicationAgent, ABC):
    current_percept: ModeratorPercept | None = None
    teams_notified: set = set()

    def see(self, percept: ModeratorPercept):
        self.current_percept = percept
        self.teams_notified.clear()

    def _direction_to(self, player_stats: AgentStats, position: AgentStats):
        global_direction = (position - player_stats.map_data.position).versor()
        relative_direction = (
            global_direction - player_stats.map_data.direction
        ).versor()
        return relative_direction

    def _notify_teammates(
        self, player_id: str, player_stats: AgentStats, rays_hitting_enemy: list[Ray]
    ):
        estimated_position = Vector2D(x=0, y=0)
        for ray in rays_hitting_enemy:
            estimated_position += ray.direction * ray.distance
        estimated_position /= len(rays_hitting_enemy)

        team = player_stats.map_data.team
        for other_id, other_stats in self.current_percept.agent_stats.items():
            if other_stats.map_data.team != team or other_id == player_id:
                continue

            direction = self._direction_to(other_stats, estimated_position)
            print(
                f"[MOD]: Sending message to {other_id} from {player_id}. Enemy at relative direction {direction}."
            )
            self.blackboard.write(other_id, direction)
        self.teams_notified.add(team)

    def _notify_player_randomly(self, player_id: str, player_stats: AgentStats):
        random_enemy_id, random_enemy_stats = random.choice(
            [
                (other_id, other_stats)
                for other_id, other_stats in self.current_percept.agent_stats.items()
                if other_stats.map_data.team != player_stats.map_data.team
                and other_stats.is_alive
            ]
        )
        direction = self._direction_to(
            player_stats, random_enemy_stats.map_data.position
        )
        print(
            f"[MOD]: Sending message to {player_id} randomly. Enemy at relative direction {direction}."
        )

        self.blackboard.write(player_id, direction)

    def select_action(self) -> WaitAction:
        if not self.current_percept or random.random() > 0.2:
            return WaitAction()

        for player_id, player_stats in self.current_percept.agent_stats.items():
            if not player_stats.is_alive:
                continue

            rays_hitting_enemy = [
                ray for ray in player_stats.rays if ray.obj == GameObject.ENEMY
            ]

            if len(rays_hitting_enemy) > 0:
                self._notify_teammates(player_id, player_stats, rays_hitting_enemy)

        if random.random() > 0.25:
            return WaitAction()

        for player_id, player_stats in self.current_percept.agent_stats.items():
            if (
                not player_stats.is_alive
                or player_stats.map_data.team in self.teams_notified
            ):
                continue

            self._notify_player_randomly(player_id, player_stats)

        return WaitAction()
