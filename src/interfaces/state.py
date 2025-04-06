from abc import ABC, abstractmethod


class State(ABC):
    """
    A complete representation of a situation in the agent environment.
    Since this is very domain specific, few methods are given.
    However, there should be methods for updating and retrieving various
    aspects of the state.
    """

    @abstractmethod
    def display(self):
        """
        Displays information about the state. This may be as simple as
        text-based output, or could update a graphical display.
        """
        pass
