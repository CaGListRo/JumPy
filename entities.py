import pygame as pg
import math
from random import randint, choice
import utilities as ut
import settings as sett

from typing import TypeVar, Final

Game = TypeVar("Game")
Platform_objects = TypeVar("Platform_objects")
Platform_rects = TypeVar("Platform_rects")
Cloud = TypeVar("Cloud")


class Player:
    def __init__(self, game: Game, color: str, pos: tuple[int]) -> None:
        """
        Initialize the player object.
        Args:
        game (Game): The game object.
        color (str): The color of the player.
        pos (tuple[int]): The initial position of the player.
        """
        self.pos: list[int] = list(pos)
        self.game: Game = game
        self.color: str = color
        self.velocity: list[int] = [0, 0]

        self.player_rect: pg.Rect = pg.Rect(self.pos[0] - 16, self.pos[1] - 64, 32, 64)
        self.old_bottom_position: tuple[int] = self.player_rect.bottom
        self.frame_counter: int = 0

        self.score: int = 0
        self.font: pg.font.Font = pg.font.SysFont('comicsans', 32)

        self.is_flipped: bool = False

        if color == 'red':
            self.player_img: pg.Surface = pg.transform.scale(ut.load_image('player1'), (32, 64))
        else:
            self.player_img: pg.Surface = pg.transform.scale(ut.load_image('player2'), (32, 64))

    def update(self, platforms: list[Platform_objects], platform_rects: list[Platform_rects], movement: tuple[int] = (0, 0)) -> None:
        """
        Update the player position and velocity.
        Args:
        platforms (Platform_objects): The list of platform objects.
        platform_rects (Platform_rects): The list of platform rectangles.
        movement (tuple[int]): The movement of the player.
        """
        self.pos[0] += ((movement[1] - movement[0]) * 5)
        self.velocity[1] = min(8, self.velocity[1] + 0.1)
        i=0
        for i, platform_rect in enumerate(platform_rects):
            if self.player_rect.colliderect(platform_rect):
                if self.velocity[1] > 0 and self.old_bottom_position < platform_rect.top:
                    self.player_rect.bottom = platform_rect.top
                    self.velocity[1] = -4.5
                    if platforms[i][2] == 1:
                        self.score += 100
                        platforms[i][2] = 0

        self.player_rect.y += self.velocity[1]
        self.player_rect.centerx = self.pos[0]

        if self.player_rect.right > sett.GAME_WINDOW_RESOLUTION[0]:
            self.player_rect.right = sett.GAME_WINDOW_RESOLUTION[0]
            self.pos[0] = self.player_rect.centerx
        if self.player_rect.left < 0:
            self.player_rect.left = 0
            self.pos[0] = self.player_rect.centerx
        if self.player_rect.top < 0:
            self.player_rect.top = 0
            self.pos[1] = self.player_rect.centery
            self.velocity[1] = 0
        
        if self.frame_counter >= 20:
            self.old_bottom_position = self.player_rect.bottom
            self.frame_counter = 0
        self.frame_counter += 1

    def render(self, flip: bool, left: bool = True) -> None:
        """
        Render the player.
        Args:
        flip (bool): Whether to flip the player image.
        left (bool): Whether the player is on the left side of the screen.
        """
        x_pos = 175 if left else sett.MAIN_WINDOW_RESOLUTION[0] - 175
        score_to_render = self.font.render(str(self.score), True, 'white')
        self.game.MAIN_WINDOW.blit(score_to_render, (x_pos - score_to_render.get_width() // 2, 15))
        if flip and not self.is_flipped:
            self.player_img = pg.transform.flip(self.player_img, True, False)
            self.is_flipped = True
        elif not flip and self.is_flipped:
            self.player_img = pg.transform.flip(self.player_img, True, False)
            self.is_flipped = False
        self.game.GAME_WINDOW_SURF.blit(self.player_img, self.player_rect)
        # pg.draw.rect(self.game.GAME_WINDOW_SURF, self.color, self.player_rect)


class Platform:
    def __init__(self, game: Game, surf: pg.Surface, game_window_res: tuple[int], start_position: tuple[int], platform_size: tuple[int] = (100, 10), platform_distances: tuple[int] = (50, 100), angle_limit: tuple[int] = (10, 170)) -> None:
        """
        Initialize the platform.
        Args:
        game (Game): The game instance.
        surf (pg.Surface): The surface to draw the platform on.
        game_window_res (tuple[int]): The resolution of the game window.
        start_position (tuple[int]): The starting position of the platform.
        platform_size (tuple[int]): The size of the platform.
        platform_distances (tuple[int]): The distance between platforms.
        angle_limit (tuple[int]): The angle limit of one platform to the next platform.
        """
        self.game: Game = game
        self.surface: pg.Surface = surf
        self.game_res: tuple[int] = game_window_res
        self.start_position: tuple[int] = start_position
        self.size: tuple[int] = platform_size
        self.distances: tuple[int] = platform_distances
        self.angle_limit: tuple[int] = angle_limit

        self.scroll_factor: int = 1
        self.update_timer: float = 0.0
        self.timer_unit: float = 2.0

        self.platforms: list[Platform_objects] = []
        self.platform_rects: list[Platform_rects] = []
        self.platforms.append([self.start_position[0] - self.size[0] // 2, self.start_position[1] + 15, 0])
        self.platform_rects.append(pg.Rect(self.start_position[0] - self.size[0] // 2, self.start_position[1] + 15, *self.size))

        self.platform_img: pg.Surface = pg.transform.scale(ut.load_image('platform'), (self.size[0], self.size[0] // 10))

    def platform_builder(self) -> None:
        """ Build the platforms. """
        distance = randint(self.distances[0], self.distances[1])
        angle = randint(self.angle_limit[0], self.angle_limit[1])
        relativ_platform_pos = [int((math.cos(math.radians(angle)) * distance)), int((math.sin(math.radians(angle)) * distance))]
        if self.platforms[-1][0] + relativ_platform_pos[0] < 0 or self.platforms[-1][0] + relativ_platform_pos[0] + self.size[0] > self.game_res[0]:
            relativ_platform_pos[0] *= -1
        new_platform = [self.platforms[-1][0] + relativ_platform_pos[0], self.platforms[-1][1] - relativ_platform_pos[1], 1]
        self.platform_rects.append(pg.Rect(new_platform[0], new_platform[1], *self.size))
        self.platforms.append(new_platform)
   
    def platform_handler(self) -> None:
        """ Handle the platforms. """
        while self.platforms[-1][1] > -100:
            self.platform_builder()
            
        if self.platforms[1][1] > self.game_res[1] + 100:
            self.platforms.pop(0)
            self.platform_rects.pop(0)

    def scroll_platforms_down(self) -> None:
        """ Scroll the platforms down. """
        for platform in self.platforms:
            platform[1] += self.scroll_factor
        for platform_rect in self.platform_rects:
            platform_rect[1] += self.scroll_factor

    def render(self) -> None:
        """ Render the platforms. """
        for platform in self.platforms:
            self.surface.blit(self.platform_img, (platform[0], platform[1]))
            #pg.draw.rect(self.surface, 'black', (platform[0], platform[1], self.size[0], self.size[1]), border_radius=3)

    def update(self, moved: bool = True) -> None:
        """
        Update the platforms.
        Args:
        moved (bool): Whether the player has moved. Defaults to True.
        """
        self.platform_handler()
        if moved:
            self.update_timer += self.timer_unit
            if self.update_timer > 100:
                self.scroll_platforms_down()
                self.update_timer = 0
                self.timer_unit += 0.2

class Button:
    BUTTON_SIZE: Final[int] = 300
    BUTTON_OFFSET: Final[int] = 10

    def __init__(self, surf: pg.Surface, text: str, pos: tuple[int], color_theme: str) -> None:
        """
        Initialize an button object.
        Args:
        surf (pg.Surface): The surface to draw the button on.
        text (str): The text to display on the button.
        pos (tuple[int]): The position of the button.
        color_theme (str): The color theme of the button.
        """
        self.surf: pg.Surface = surf
        self.text: str = text
        self.pos: list[int] = list(pos)
        self.color_theme: str = color_theme
        self.font: pg.font.Font = pg.font.SysFont('comicsans', 32)
        self.button_top_rect: pg.Rect = pg.Rect(pos[0] - self.BUTTON_SIZE / 2, pos[1] - self.BUTTON_SIZE / 2, self.BUTTON_SIZE, self.BUTTON_SIZE)
        self.button_bottom_rect: pg.Rect = pg.Rect(pos[0] - self.BUTTON_SIZE / 2, pos[1] - self.BUTTON_SIZE / 2, self.BUTTON_SIZE, self.BUTTON_SIZE)
        self.button_offset: int = self.BUTTON_OFFSET
        self.button_color: tuple[int] = sett.BUTTON_COLORS[self.color_theme]['color']
        self.clicked: None | bool = None

    def render(self) -> None:
        """ Render the button. """
        pg.draw.rect(self.surf, sett.BUTTON_COLORS[self.color_theme]['shadow_color'], self.button_bottom_rect, border_radius=50)
        pg.draw.rect(self.surf, sett.BLACK, self.button_bottom_rect, border_radius=50, width=1)
        pg.draw.rect(self.surf, self.button_color, (self.button_top_rect[0], self.button_top_rect[1] - self.button_offset, self.button_top_rect[2], self.button_top_rect[3]), border_radius=50)
        pg.draw.rect(self.surf, sett.BUTTON_COLORS[self.color_theme]['frame_color'], (self.button_top_rect[0], self.button_top_rect[1] - self.button_offset, self.button_top_rect[2], self.button_top_rect[3]), border_radius=50, width=3)
        text_surf = self.font.render(self.text, True, sett.BLACK)
        self.surf.blit(text_surf, (self.pos[0] - text_surf.get_width() // 2, self.pos[1] - text_surf.get_height() // 2 - self.button_offset))

    def check_collision(self) -> None | bool:
        mouse_pos: tuple[int] = pg.mouse.get_pos()
        if self.button_top_rect.collidepoint(mouse_pos):
            self.button_color = sett.BUTTON_COLORS[self.color_theme]['hover_color']
            if pg.mouse.get_pressed()[0]:
                self.button_offset = 0
                self.clicked = True
            else:
                self.button_offset = self.BUTTON_OFFSET
                if self.clicked == True:
                    self.clicked = None
        else:
            self.button_color = sett.BUTTON_COLORS[self.color_theme]['color']
        return self.clicked


class Cloud:
    def __init__(self, pos: tuple[int], image: pg.Surface, depth: int) -> None:
        """
        Initialize a cloud object.
        Args:
        pos (tuple[int]): The position of the cloud.
        image (pg.Surface): The image of the cloud.
        depth (int): The depth of the cloud.
        """
        self.pos: list[int] = list(pos)
        self.image: pg.Surface = pg.transform.scale(image, (image.get_width() // depth, image.get_height() // depth))
        self.image = pg.transform.flip(self.image, choice([True, False]), False)
        self.depth: int = depth

    def update(self) -> None:
        """ Update the cloud's position. """
        self.pos[1] += 1 / (self.depth * 10)            

    def render(self, surf: pg.Surface) -> None:
        """
        Render the cloud on the given surface.
        Args:
        surf (pg.Surface): The surface to render the cloud on.
        """
        surf.blit(self.image, self.pos)


class Clouds:
    def __init__(self) -> None:
        """
        Initializes an Cloud-Manager object.
        """
        self.cloud_images: list[pg.Surface] = []
        self.clouds: list[Cloud] = []
        self.initial_start: bool = True
        for i in range(1, 4):
            self.cloud_images.append(ut.load_image('cloud' + str(i)))

    def update(self, count=16) -> None:
        """
        Creates and updates the clouds.
        Args:
        count (int): The number of clouds to create/have.
        """
        while True:
            if len(self.clouds) < count:
                y_pos = sett.GAME_WINDOW_RESOLUTION[1] if self.initial_start else -sett.GAME_WINDOW_RESOLUTION[1] // 4
                pos = (randint(0, sett.GAME_WINDOW_RESOLUTION[0]), (randint(0, y_pos) if y_pos > 0 else randint(y_pos, 0)))
                img_number = randint(0, 2)
                depth = randint(1, 3)
                cloud = Cloud(pos, self.cloud_images[img_number], depth)
                self.clouds.append(cloud)
            else:
                self.initial_start = False
                break

        self.clouds.sort(key=lambda x: x.depth)

    def render(self, surf: pg.Surface) -> None:
        """
        Renders all clouds on the given surface and deletes them if they are off the screen.
        Args:
        surf (pg.Surface): The surface to render the clouds on.
        """
        for cloud in self.clouds:
            cloud.update()
            cloud.render(surf)
            if cloud.pos[1] > sett.GAME_WINDOW_RESOLUTION[1] + 10:
                self.clouds.remove(cloud)