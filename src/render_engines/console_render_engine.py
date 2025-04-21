from src.interfaces.render_engine import RenderEngine

from src.state import GameState


class ConsoleRenderEngine(RenderEngine):
    SYMBOLS = {"wall": "#", "empty": " ", "dead": "x"}

    def display(self, state: GameState):
        grid = [
            [self.SYMBOLS["empty"] for _ in range(state.map.width)]
            for _ in range(state.map.height)
        ]

        # Place walls
        for x, y in state.map.walls:
            grid[y][x] = self.SYMBOLS["wall"]

        # Place agents
        for agent, agent_data in state.map.players.items():
            agent_data = agent.map_data
            x, y = agent_data.position
            if not agent.is_alive:
                symbol = self.SYMBOLS["dead"]
            else:
                symbol = agent_data.team.lower()
            grid[int(y)][int(x)] = symbol

        print(f"Tick: {state.tick}")
        for row in grid:
            print("".join(row))
        print()
