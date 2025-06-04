from src.agents.dummy_player.dummy_player import DummyPlayerAgent
from src.agents.random_player import RandomPlayerAgent
from src.environment import GameEnvironment
from src.map import GameMap
from src.render_engines import PygameRenderEngine
from src.simulations.game_simulation import GameSimulation
from src.state import GameState


if __name__ == "__main__":
    render_engine = PygameRenderEngine()
    game_map = GameMap.from_file("maps/level0.txt")
    player_agents = {
        identifier: (
            RandomPlayerAgent(player_id=data.player_id)
            if data.team == "R"
            else DummyPlayerAgent(player_id=data.player_id)
        )
        for identifier, data in game_map.players.items()
    }
    initial_state = GameState(agents=player_agents, map=game_map)
    simulation = GameSimulation(
        agents=list(player_agents.values()),
        env=GameEnvironment(state=initial_state),
        render_engine=render_engine,
    )
    simulation.start()
