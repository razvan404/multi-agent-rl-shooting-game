from abc import ABC, abstractmethod

from .agent import Agent
from .state import State


class Action(ABC):
    """
    An abstract class for actions in an agent environment. Each type of
    Action should be a separate subclass.
    """

    @abstractmethod
    def execute(self, agent: Agent, state: State) -> State:
        """
        Update the state of the environment to reflect the effects of the
        agent performing the action. This implements the env: S x A -> S
        function. Note that in a multiagent environment, it is also
        important to know which agent is executing the action.
        """
        pass
