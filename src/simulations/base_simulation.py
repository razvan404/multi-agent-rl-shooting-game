from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict

from src.interfaces.action import Action
from src.interfaces.agent import Agent
from src.interfaces.environment import Environment
from src.interfaces.render_engine import RenderEngine

from .exceptions import StopSimulationException


class BaseSimulation(BaseModel, ABC):
    """
    The top-level class for an agent simulation. This can be used for either
    single or multi-agent simulations.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    agents: list[Agent]
    env: Environment
    render_engine: RenderEngine

    def simulation_step(self):
        agents_actions: list[tuple[Agent, Action]] = []

        for agent in self.agents:
            percept = self.env.get_percept(agent)
            agent.see(percept)
            action = agent.select_action()
            agents_actions.append((agent, action))

        for agent, action in agents_actions:
            self.env.update_state(agent, action)

        self.env.step()
        self.render_engine.display(self.env.state)

    def start(self):
        """
        Runs the simulation starting from a given state. This consists of a
        sense-act loop for the/(each) agent. An alternative approach would be to
        allow the agent to decide when it will sense and act.
        """
        self.render_engine.display(self.env.state)

        try:
            while not self.is_complete():
                self.simulation_step()
            self.render_engine.stop()
        except StopSimulationException:
            pass

    @abstractmethod
    def is_complete(self) -> bool:
        """
        Is the simulation over? Returns true if it is, otherwise false.
        """
        pass
