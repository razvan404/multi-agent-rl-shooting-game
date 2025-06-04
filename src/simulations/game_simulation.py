from .base_simulation import BaseSimulation
from src.environment import GameEnvironment


class GameSimulation(BaseSimulation):
    env: GameEnvironment

    def is_complete(self) -> bool:
        if self.env.state.tick >= 500:
            return True

        alive_teams = set()
        for agent_stats in self.env.state.agent_stats.values():
            if not agent_stats.is_alive or agent_stats.map_data.team in alive_teams:
                continue
            if len(alive_teams) >= 1:
                return False
            alive_teams.add(agent_stats.map_data.team)
        return True
