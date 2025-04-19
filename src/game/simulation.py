from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.interfaces.action import Action
from src.interfaces.agent import Agent
from src.interfaces.environment import Environment
from src.interfaces.render_engine import RenderEngine
from src.interfaces.state import State


@dataclass
class Simulation(ABC):
    """
    The top-level class for an agent simulation. This can be used for either
    single or multi-agent simulations.
    """

    agents: list[Agent]
    env: Environment
    render_engine: RenderEngine

    def start(self, init_state: State):
        """
        Runs the simulation starting from a given state. This consists of a
        sense-act loop for the/(each) agent. An alternative approach would be to
        allow the agent to decide when it will sense and act.
        """
        self.env.state = init_state
        self.render_engine.display(self.env.state)

        while not self.is_complete():
            agents_actions: list[tuple[Agent, Action]] = []

            for agent in self.agents:
                percept = self.env.get_percept(agent)
                agent.see(percept)
                action = agent.select_action()
                agents_actions.append((agent, action))

            for agent, action in agents_actions:
                self.env.state = self.env.update_state(agent, action)

            self.render_engine.display(self.env.state)

    @abstractmethod
    def is_complete(self) -> bool:
        """
        Is the simulation over? Returns true if it is, otherwise false.
        """
        pass
