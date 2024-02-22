import pygame as pg
import math
from random import randint
import utilities as ut


class Player:
    def __init__(self, game, color, pos):
        self.pos = list(pos)
        self.game = game
        self.color = color
        self.velocity = [0, 0]

        self.player_rect = pg.Rect(self.pos[0] - 16, self.pos[1] - 64, 32, 64)
        self.old_bottom_position = self.player_rect.bottom
        self.frame_counter = 0

        self.score = 0
        self.font = pg.font.SysFont('comicsans', 32)

    def update(self, platforms, platform_rects, movement=(0, 0)):
        self.pos[0] += ((movement[1] - movement[0]) * 5)
        self.velocity[1] = min(8, self.velocity[1] + 0.1)
        i=0
        for i, platform_rect in enumerate(platform_rects):
            if self.player_rect.colliderect(platform_rect):
                if self.velocity[1] > 0 and self.old_bottom_position < platform_rect.top:
                    self.player_rect.bottom = platform_rect.top
                    self.velocity[1] = -4.5
                    try:
                        if platforms[i][2] == 1:
                            self.score += 100
                            platforms[i][2] = 0
                            
                    except IndexError:
                        print(i, platforms, platform_rect)

        self.player_rect.y += self.velocity[1]
        self.player_rect.centerx = self.pos[0]

        if self.player_rect.right > ut.GAME_WINDOW_RESOLUTION[0]:
            self.player_rect.right = ut.GAME_WINDOW_RESOLUTION[0]
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

    def render(self, left=True):
        x_pos = 175 if left else ut.MAIN_WINDOW_RESOLUTION[0] - 175
        score_to_render = self.font.render(str(self.score), True, 'white')
        self.game.MAIN_WINDOW.blit(score_to_render, (x_pos - score_to_render.get_width() // 2, 15))
        pg.draw.rect(self.game.GAME_WINDOW_SURF, self.color, self.player_rect)


class Platform:
    def __init__(self, game, surf, game_window_res, start_position, platform_size = (100, 10), platform_distances = (50, 100), angle_limit = (10, 170)):
        self.game = game
        self.surface = surf
        self.game_res = game_window_res
        self.start_position = start_position
        self.size = platform_size
        self.distances = platform_distances
        self.angle_limit = angle_limit

        self.update_timer = 0
        self.timer_unit = 2

        self.platforms = []
        self.platform_rects = []
        self.platforms.append([self.start_position[0] - self.size[0] // 2, self.start_position[1] + 15, 0])
        self.platform_rects.append(pg.Rect(self.start_position[0] - self.size[0] // 2, self.start_position[1] + 15, *self.size))

    def platform_builder(self):
        distance = randint(self.distances[0], self.distances[1])
        angle = randint(self.angle_limit[0], self.angle_limit[1])
        relativ_platform_pos = [int((math.cos(math.radians(angle)) * distance)), int((math.sin(math.radians(angle)) * distance))]
        if self.platforms[-1][0] + relativ_platform_pos[0] < 0 or self.platforms[-1][0] + relativ_platform_pos[0] + self.size[0] > self.game_res[0]:
            relativ_platform_pos[0] *= -1
        new_platform = [self.platforms[-1][0] + relativ_platform_pos[0], self.platforms[-1][1] - relativ_platform_pos[1], 1]
        self.platform_rects.append(pg.Rect(new_platform[0], new_platform[1], *self.size))
        self.platforms.append(new_platform)
   
    def platform_handler(self):
        while self.platforms[-1][1] > -100:
            self.platform_builder()
            
        if self.platforms[1][1] > self.game_res[1] + 100:
            self.platforms.pop(0)
            self.platform_rects.pop(0)

    def scroll_platforms_down(self):
        for platform in self.platforms:
            platform[1] += 1
        for platform_rect in self.platform_rects:
            platform_rect[1] += 1

    def render(self):
        for platform in self.platforms:
            pg.draw.rect(self.surface, 'black', (platform[0], platform[1], self.size[0], self.size[1]), border_radius=3)

    def update(self, moved=True):
        self.platform_handler()
        if moved:
            self.update_timer += self.timer_unit
            if self.update_timer > 100:
                self.scroll_platforms_down()
                self.update_timer = 0
                self.timer_unit += 0.2

class Button:
    def __init__(self, surf, text, pos, color_thema):
        self.surf = surf
        self.text = text
        self.pos = list(pos)
        self.color_thema = color_thema
        self.button_size = 300
        self.font = pg.font.SysFont('comicsans', 32)
        self.button_top_rect = pg.Rect(pos[0] - self.button_size / 2, pos[1] - self.button_size / 2, self.button_size, self.button_size)
        self.button_bottom_rect = pg.Rect(pos[0] - self.button_size / 2, pos[1] - self.button_size / 2, self.button_size, self.button_size)
        self.button_offset = 10
        self.button_color = ut.BUTTON_COLORS[self.color_thema]['color']

    def render(self):
        pg.draw.rect(self.surf, ut.BUTTON_COLORS[self.color_thema]['shadow_color'], self.button_bottom_rect, border_radius=50)
        pg.draw.rect(self.surf, ut.BLACK, self.button_bottom_rect, border_radius=50, width=1)
        pg.draw.rect(self.surf, self.button_color, (self.button_top_rect[0], self.button_top_rect[1] - self.button_offset, self.button_top_rect[2], self.button_top_rect[3]), border_radius=50)
        pg.draw.rect(self.surf, ut.BUTTON_COLORS[self.color_thema]['frame_color'], (self.button_top_rect[0], self.button_top_rect[1] - self.button_offset, self.button_top_rect[2], self.button_top_rect[3]), border_radius=50, width=3)
        text_surf = self.font.render(self.text, True, ut.BLACK)
        self.surf.blit(text_surf, (self.pos[0] - text_surf.get_width() // 2, self.pos[1] - text_surf.get_height() // 2 - self.button_offset))

    def check_collision(self):
        mouse_pos = pg.mouse.get_pos()
        if self.button_top_rect.collidepoint(mouse_pos):
            self.button_color = ut.BUTTON_COLORS[self.color_thema]['hover_color']
            if pg.mouse.get_pressed()[0]:
                self.button_offset = 0
                return True
            else:
                self.button_offset = 10
                return None
        else:
            self.button_color = ut.BUTTON_COLORS[self.color_thema]['color']
