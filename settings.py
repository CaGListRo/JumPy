from typing import Final

MAIN_WINDOW_RESOLUTION: Final[tuple[int]] = (1400, 900)
GAME_WINDOW_RESOLUTION: Final[tuple[int]] = (700, 850)
FRAME_THICKNESS: Final[int] = 5
WINDOW_FRAME_POSITION: Final[tuple[int]] = (int(MAIN_WINDOW_RESOLUTION[0] // 2 - GAME_WINDOW_RESOLUTION[0] // 2 - FRAME_THICKNESS),
                                            int(MAIN_WINDOW_RESOLUTION[1] // 2 - GAME_WINDOW_RESOLUTION[1] // 2 - FRAME_THICKNESS))
WINDOW_FRAME_SIZE: Final[tuple[int]] = (GAME_WINDOW_RESOLUTION[0] + 2 * FRAME_THICKNESS, GAME_WINDOW_RESOLUTION[1] + 2 * FRAME_THICKNESS)

BLACK: Final[tuple[int]] = (1, 1, 1)

BUTTON_COLORS: Final[dict[dict[tuple[int]]]] = {
    'green': {'color': (56, 155, 60), 'hover_color': (76, 175, 80), 'shadow_color': (16, 115, 20), 'frame_color': (6, 95, 20)},
    'yellow': {'color': (235, 235, 0), 'hover_color': (255, 255, 50), 'shadow_color': (195, 195, 0), 'frame_color': (125, 125, 0)},
    'red': {'color': (235, 0, 0), 'hover_color': (255, 50, 50), 'shadow_color': (175, 0, 0), 'frame_color': (100, 0, 0)}
    }