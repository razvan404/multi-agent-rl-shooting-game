import pygame
import math

from src.interfaces.render_engine import RenderEngine
from src.state import GameState
from src.constants import PLAYER_VIEW_FOV, PLAYER_NUM_RAYS, PLAYER_RAY_LENGTH
from src.geometry import Vector2D


class PygameRenderEngine(RenderEngine):
    CELL_SIZE = 40
    COLORS = {
        "background": (200, 255, 200),
        "wall": (0, 0, 0),
        "empty": (255, 255, 255),
        "dead": (100, 100, 100),
        "team_r": (255, 0, 0),
        "team_y": (255, 200, 0),
        "ray_wall": (0, 0, 255),
        "ray_agent": (255, 0, 255),
        "ray_none": (0, 255, 0),
    }

    def __init__(self):
        pygame.init()
        self.screen = None
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    def display(self, state: GameState):
        self._setup_screen(state)
        self._draw_grid(state)
        self._draw_walls(state)
        self._draw_agents(state)
        self._draw_rays(state)
        self._draw_tick(state)
        pygame.display.flip()
        self.clock.tick(5)

    def _setup_screen(self, state: GameState):
        width = state.map.width * self.CELL_SIZE
        height = state.map.height * self.CELL_SIZE + 30
        if self.screen is None:
            self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(self.COLORS["background"])

    def _draw_grid(self, state: GameState):
        for x in range(state.map.width):
            for y in range(state.map.height):
                rect = pygame.Rect(
                    x * self.CELL_SIZE,
                    y * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE,
                )
                pygame.draw.rect(self.screen, self.COLORS["empty"], rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def _draw_walls(self, state: GameState):
        for wall in state.map.walls:
            rect = pygame.Rect(
                int(wall.x * self.CELL_SIZE),
                int(wall.y * self.CELL_SIZE),
                self.CELL_SIZE,
                self.CELL_SIZE,
            )
            pygame.draw.rect(self.screen, self.COLORS["wall"], rect)

    def _draw_agents(self, state: GameState):
        for agent in state.agents.values():
            agent_map_data = state.agent_map_data(agent.player_id)
            x, y = agent_map_data.position.x, agent_map_data.position.y
            pixel_x = int(x * self.CELL_SIZE + self.CELL_SIZE / 2)
            pixel_y = int(y * self.CELL_SIZE + self.CELL_SIZE / 2)

            if not agent.is_alive:
                color = self.COLORS["dead"]
            else:
                color = self.COLORS.get(
                    f"team_{agent_map_data.team.lower()}", (255, 0, 0)
                )

            pygame.draw.circle(
                self.screen, color, (pixel_x, pixel_y), self.CELL_SIZE // 2 - 2
            )

    def _draw_rays(self, state: GameState):
        for player_id, agent in state.agents.items():
            if not agent.is_alive or player_id not in state.rays:
                continue

            agent_map_data = state.agent_map_data(agent.player_id)
            origin = agent_map_data.position
            direction = agent_map_data.direction
            if direction is None:
                continue

            base_angle = direction.base_angle()
            start_angle = base_angle - (PLAYER_VIEW_FOV / 2)
            angle_step = PLAYER_VIEW_FOV / (PLAYER_NUM_RAYS - 1)

            for i, ray in enumerate(state.rays[player_id]):
                angle = start_angle + i * angle_step
                dx = math.cos(math.radians(angle))
                dy = math.sin(math.radians(angle))
                ray_direction = Vector2D(x=dx, y=dy)

                hit_pos = origin + ray_direction * (ray.distance * PLAYER_RAY_LENGTH)

                start_px = int(origin.x * self.CELL_SIZE + self.CELL_SIZE / 2)
                start_py = int(origin.y * self.CELL_SIZE + self.CELL_SIZE / 2)
                end_px = int(hit_pos.x * self.CELL_SIZE + self.CELL_SIZE / 2)
                end_py = int(hit_pos.y * self.CELL_SIZE + self.CELL_SIZE / 2)

                if ray.obj.name == "WALL":
                    color = self.COLORS["ray_wall"]
                elif ray.obj.name in ("ENEMY", "TEAMMATE"):
                    color = self.COLORS["ray_agent"]
                else:
                    color = self.COLORS["ray_none"]

                pygame.draw.line(
                    self.screen, color, (start_px, start_py), (end_px, end_py), 2
                )

    def _draw_tick(self, state: GameState):
        tick_text = self.font.render(f"Tick: {state.tick}", True, (0, 0, 0))
        self.screen.blit(tick_text, (5, state.map.height * self.CELL_SIZE + 5))

    @classmethod
    def quit(cls):
        pygame.quit()
