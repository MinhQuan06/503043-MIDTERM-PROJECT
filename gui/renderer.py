from pathlib import Path

import pygame


class SokobanRenderer:
    """Render Sokoban maps using reusable image assets."""

    def __init__(self, asset_dir=None, tile_size=32):
        project_root = Path(__file__).resolve().parents[1]

        self.asset_dir = (
            Path(asset_dir)
            if asset_dir is not None
            else project_root / "gui" / "assets"
        )

        self.tile_size = tile_size
        self.images = {}
        self._load_assets()

    def _load_image(self, relative_path):
        path = self.asset_dir / relative_path

        try:
            image = pygame.image.load(str(path)).convert_alpha()
        except (pygame.error, OSError) as exc:
            raise FileNotFoundError(
                f"Cannot load asset: {path}"
            ) from exc

        return pygame.transform.smoothscale(
            image,
            (self.tile_size, self.tile_size),
        )

    def _load_assets(self):
        asset_paths = {
            "wall": "tiles/wall.png",
            "floor": "tiles/ground_06.png",
            "goal": "tiles/goal.png",
            "player": "objects/player.png",
            "box": "objects/box.png",
            "box_on_goal": "objects/box_on_goal.png",
            "box_on_goal_1": "objects/box_on_goal_1.png",
            "box_on_goal_2": "objects/box_on_goal_2.png",
            "player2": "objects/player2.png",
        }

        for name, relative_path in asset_paths.items():
            self.images[name] = self._load_image(relative_path)

    @staticmethod
    def read_map(map_path):
        path = Path(map_path)

        with path.open("r", encoding="utf-8") as file:
            return file.read().splitlines()

    def render_map(self, surface, map_lines, area=None):
        if not map_lines:
            return

        map_width = max(len(row) for row in map_lines)
        map_height = len(map_lines)

        if area is None:
            area = surface.get_rect()

        # Fit the map inside the available drawing area.
        tile_size = min(
            self.tile_size,
            area.width // max(map_width, 1),
            area.height // max(map_height, 1),
        )

        if tile_size < 1:
            return

        map_pixel_width = map_width * tile_size
        map_pixel_height = map_height * tile_size

        start_x = area.x + (area.width - map_pixel_width) // 2
        start_y = area.y + (area.height - map_pixel_height) // 2

        for y, row in enumerate(map_lines):
            for x in range(map_width):
                cell = row[x] if x < len(row) else "%"

                rect = pygame.Rect(
                    start_x + x * tile_size,
                    start_y + y * tile_size,
                    tile_size,
                    tile_size,
                )

                if cell == "%":
                    self._draw_tile(surface, "wall", rect)
                else:
                    self._draw_tile(surface, "floor", rect)

                if cell in ("D", "C"):
                    self._draw_tile(surface, "goal", rect)

                if cell in ("B", "C"):
                    box_name = (
                        "box_on_goal" if cell == "C" else "box"
                    )
                    self._draw_tile(surface, box_name, rect)

                if cell == "A":
                    self._draw_tile(surface, "player", rect)

    def _draw_tile(self, surface, name, rect):
        image = self.images[name]

        if image.get_size() != rect.size:
            image = pygame.transform.smoothscale(
                image, rect.size
            )

        surface.blit(image, rect)

    def render_state(self, surface, problem, state, area=None):
        agent, boxes = state

        map_lines = []

        for row in range(problem.rows):
            line = []

            for col in range(problem.cols):
                pos = (row, col)

                if pos in problem.walls:
                    symbol = "%"
                elif pos in boxes and pos in problem.goals:
                    symbol = "C"
                elif pos in boxes:
                    symbol = "B"
                elif pos == agent:
                    symbol = "A"
                elif pos in problem.goals:
                    symbol = "D"
                else:
                    symbol = " "

                line.append(symbol)

            map_lines.append("".join(line))

        self.render_map(surface, map_lines, area)
    def _draw_owned_box(self, surface, rect, owner, on_goal):
        name = "box"
        if on_goal:
            name = (
                f"box_on_goal_{owner}"
                if owner in (1, 2)
                else "box_on_goal"
            )
        self._draw_tile(surface, name, rect)

    def render_competitive_state(self, surface, state, area=None):
        """
        Render Task 2 directly from CompetitiveState.

        Positions use (x, y), unlike Task 1's (row, col).
        """
        if area is None:
            area = surface.get_rect()

        tile_size = min(
            self.tile_size,
            area.width // max(state.width, 1),
            area.height // max(state.height, 1),
        )

        if tile_size < 1:
            return

        map_width = state.width * tile_size
        map_height = state.height * tile_size

        start_x = area.x + (area.width - map_width) // 2
        start_y = area.y + (area.height - map_height) // 2

        # Layer 1: floor, walls and goals
        for y in range(state.height):
            for x in range(state.width):
                pos = (x, y)

                rect = pygame.Rect(
                    start_x + x * tile_size,
                    start_y + y * tile_size,
                    tile_size,
                    tile_size,
                )

                if pos in state.walls:
                    self._draw_tile(surface, "wall", rect)
                    continue

                self._draw_tile(surface, "floor", rect)

                if pos in state.goals:
                    self._draw_tile(surface, "goal", rect)

        # Layer 2: shared box appearance; ownership colors only on goals.
        for (x, y), owner in state.boxes.items():
            rect = pygame.Rect(
                start_x + x * tile_size,
                start_y + y * tile_size,
                tile_size,
                tile_size,
            )

            self._draw_owned_box(
                surface,
                rect,
                owner,
                on_goal=(x, y) in state.goals,
            )

        # Layer 3: agents
        for agent_id, (x, y) in state.agents.items():
            rect = pygame.Rect(
                start_x + x * tile_size,
                start_y + y * tile_size,
                tile_size,
                tile_size,
            )

            image_name = "player" if agent_id == 1 else "player2"

            self._draw_tile(surface, image_name, rect)
