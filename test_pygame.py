import multiprocessing

from src.agents.dummy_player.dummy_player import DummyPlayerAgent
from src.agents.moderator.agent import ModeratorAgent
from src.agents.random_player import RandomPlayerAgent
from src.blackboard import Blackboard
from src.environment import GameEnvironment
from src.map import GameMap
from src.render_engines import PygameRenderEngine
from src.simulations.game_simulation import GameSimulation
from src.state import GameState


def run_simulation():
    render_engine = PygameRenderEngine(sleep_between_simulations=0.001)
    blackboard = Blackboard()
    game_map = GameMap.from_file("maps/level2.txt")
    agents = [
        *[
            (
                RandomPlayerAgent(player_id=player_id, blackboard=blackboard)
                if data.team == "R" or data.team == "B"
                else DummyPlayerAgent(player_id=data.player_id, blackboard=blackboard)
            )
            for player_id, data in game_map.players.items()
        ],
        ModeratorAgent(blackboard=blackboard),
    ]
    initial_state = GameState(map=game_map)
    simulation = GameSimulation(
        agents=agents,
        env=GameEnvironment(state=initial_state),
        render_engine=render_engine,
    )
    simulation.start()


if __name__ == "__main__":
    processes = []
    for _ in range(1):
        p = multiprocessing.Process(target=run_simulation)
        p.start()
        processes.append(p)
