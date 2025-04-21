from .base_simulation import BaseSimulation
from src.environment import GameEnvironment


class GameSimulation(BaseSimulation):
    env: GameEnvironment

    def is_complete(self) -> bool:
        num_alive_agents = 0
        for agent_stats in self.env.state.agent_stats.values():
            num_alive_agents += 1 if agent_stats.is_alive else 0
        return num_alive_agents <= 1
