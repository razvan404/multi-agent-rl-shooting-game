from .actions import PlayerAction
from .agents.player import PlayerAgent, PlayerPercept
from .geometry import Vector2D
from .interfaces import Environment, Agent, Action, Percept
from .state import GameState
from .utils import ActionExecutorFactory


class GameEnvironment(Environment):
    state: GameState

    def get_percept(self, agent: Agent) -> Percept:
        if isinstance(agent, PlayerAgent):
            rays = self.state.rays[agent.player_id]
            direction = Vector2D(**self.state.agent_data(agent.player_id)["direction"])
            return PlayerPercept(rays=rays, direction=direction)
        raise ValueError("Unsupported agent type")

    def update_state(self, agent: Agent, action: Action) -> None:
        if isinstance(action, PlayerAction):
            executor = ActionExecutorFactory.get_executor(action)
            self.state = executor.execute(agent, self.state)

    def step(self) -> None:
        self.state.step()
