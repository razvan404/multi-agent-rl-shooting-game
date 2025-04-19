from src.interfaces.action import Action
from src.interfaces.executable_action import ExecutableAction


class ActionExecutorFactory:
    _executors = {}

    @classmethod
    def register(cls, action_type: type[Action], executor: type[ExecutableAction]):
        cls._executors[action_type] = executor

    def get_executor(self, action: Action) -> ExecutableAction:
        executor_cls = self._executors[type(action)]
        return executor_cls.from_action(action)
