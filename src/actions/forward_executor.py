from src.agents.player import PlayerAgent
from src.constants import PLAYER_FORWARD_DISTANCE
from src.interfaces import ExecutableAction
from src.objects import CollisionDetector
from src.state import GameState
from src.utils import ActionExecutorFactory

from .actions import ForwardAction


class ForwardExecutor(ExecutableAction):
    def execute(self, agent: PlayerAgent, state: GameState) -> GameState:
        stats = state.agent_stats[agent.player_id]
        if not stats.is_alive:
            return state

        player_data = state.map.players[agent.player_id]
        dir_vec = player_data.direction
        if dir_vec is None:
            return state

        new_pos = player_data.position + dir_vec * PLAYER_FORWARD_DISTANCE
        if all(
            not CollisionDetector.check_collision_player_wall(new_pos, wall)
            for wall in state.map.nearest_walls(new_pos)
        ):
            player_data.position = new_pos

        return state


ActionExecutorFactory.register(ForwardAction, ForwardExecutor)
