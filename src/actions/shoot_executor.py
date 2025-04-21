from src.agents.player import PlayerAgent
from src.geometry import Vector2D
from src.interfaces import ExecutableAction
from src.state import GameState, PendingShot

from .actions import ShootAction
from ..constants import PLAYER_SHOOTING_DELAY_TICKS
from ..utils import ActionExecutorFactory


class ShootExecutor(ExecutableAction):
    def __init__(self, angle: float):
        self.angle = angle

    @classmethod
    def from_action(cls, action: ShootAction):
        return cls(angle=action.angle)

    def execute(self, agent: PlayerAgent, state: GameState) -> GameState:
        stats = state.agent_stats[agent.player_id]
        if not stats.is_alive or stats.shooting_delay > 0:
            return state

        player_data = state.map.players[agent.player_id]
        origin = player_data.position
        if not player_data.direction:
            return state

        base_angle = player_data.direction.base_angle()
        shot_angle = base_angle + self.angle
        direction = Vector2D.from_angle(shot_angle)

        state.pending_shots.append(
            PendingShot(player_id=agent.player_id, origin=origin, direction=direction)
        )
        stats.shooting_delay = PLAYER_SHOOTING_DELAY_TICKS
        return state


ActionExecutorFactory.register(ShootAction, ShootExecutor)
