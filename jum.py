import pygame as pg
import math, sys
from random import randint
from entities import Player, Platform, Button
import utilities as ut

class Game:
    def __init__(self):
        pg.init()
        
        self.MAIN_WINDOW = pg.display.set_mode(ut.MAIN_WINDOW_RESOLUTION)
        self.GAME_WINDOW_SURF = pg.Surface(ut.GAME_WINDOW_RESOLUTION)

        self.start_screen = pg.Surface(ut.MAIN_WINDOW_RESOLUTION)
        self.show_start_screen = True
        self.difficulty_screen = pg.Surface(ut.MAIN_WINDOW_RESOLUTION)
        self.show_difficulty_screen = True
        self.button_surface = pg.Surface(ut.MAIN_WINDOW_RESOLUTION)

        self.CLOCK = pg.time.Clock()
        self.FPS = 60
        self.running = True

        self.single_player = None
        self.movement_player1 = [False, False]  # [left, right]
        self.movement_player2 = [False, False]  # [left, right]
        self.moved = False
        self.platform_size = (500, 50)
        self.platform_distances = (250, 500)

        self.single_player_button_center_pos = (ut.MAIN_WINDOW_RESOLUTION[0] // 3, ut.MAIN_WINDOW_RESOLUTION[1] // 2)
        self.two_player_button_center_pos = (ut.MAIN_WINDOW_RESOLUTION[0] // 3 * 2, ut.MAIN_WINDOW_RESOLUTION[1] // 2)
        self.easy_button_center_pos = (ut.MAIN_WINDOW_RESOLUTION[0] // 4, ut.MAIN_WINDOW_RESOLUTION[1] // 2)
        self.normal_button_center_pos = (ut.MAIN_WINDOW_RESOLUTION[0] // 2, ut.MAIN_WINDOW_RESOLUTION[1] // 2)
        self.hard_button_center_pos = (ut.MAIN_WINDOW_RESOLUTION[0] // 4 * 3, ut.MAIN_WINDOW_RESOLUTION[1] // 2)

        self.easy = False
        self.normal = False
        self.hard = False
        
    def create_game_window(self):
        self.MAIN_WINDOW.fill('black')
        pg.draw.rect(self.MAIN_WINDOW, 'white', (ut.WINDOW_FRAME_POSITION, ut.WINDOW_FRAME_SIZE), border_radius=3)
        self.GAME_WINDOW_SURF.fill((23, 123, 223))
        self.platforms1.render()
        self.player1.render()
        if not self.single_player:
            self.platforms2.render()
            self.player2.render(left=False)

        self.MAIN_WINDOW.blit(self.GAME_WINDOW_SURF, (350, 25))

    def create_game_data(self):
        if self.easy:
            self.platform_size = (150, 15)
            self.platform_distances = (40, 80)
            self.angle_limit = (10, 170)
        elif self.normal:
            self.platform_size = (100, 10)
            self.platform_distances = (50, 100)
            self.angle_limit = (30, 150)
        elif self.hard:
            self.platform_size = (50, 5)
            self.platform_distances = (90, 100)
            self.angle_limit = (50, 130)

        if self.single_player:
            self.player_1_start_pos = [ut.GAME_WINDOW_RESOLUTION[0] // 2, ut.GAME_WINDOW_RESOLUTION[1] - 100]
            self.first_platform1 = [ut.GAME_WINDOW_RESOLUTION[0] // 2 - self.platform_size[0] // 2, ut.GAME_WINDOW_RESOLUTION[1] - 50]
        else:
            self.player_1_start_pos = [ut.GAME_WINDOW_RESOLUTION[0] // 4, ut.GAME_WINDOW_RESOLUTION[1] - 100]
            self.first_platform1 = [ut.GAME_WINDOW_RESOLUTION[0] // 4 - self.platform_size[0] // 2, ut.GAME_WINDOW_RESOLUTION[1] - 50]
            self.player_2_start_pos = [ut.GAME_WINDOW_RESOLUTION[0] // 4 * 3, ut.GAME_WINDOW_RESOLUTION[1] - 100]
            self.first_platform2 = [ut.GAME_WINDOW_RESOLUTION[0] // 4 - self.platform_size[0] // 2, ut.GAME_WINDOW_RESOLUTION[1] - 50]

        self.player1 = Player(self, 'red', self.player_1_start_pos)
        self.platforms1 = Platform(self, self.GAME_WINDOW_SURF, ut.GAME_WINDOW_RESOLUTION, self.player_1_start_pos, self.platform_size, self.platform_distances, self.angle_limit)
        if not self.single_player:
            self.player2 = Player(self, 'green', self.player_2_start_pos)
            self.platforms2 = Platform(self, self.GAME_WINDOW_SURF, ut.GAME_WINDOW_RESOLUTION, self.player_2_start_pos, self.platform_size, self.platform_distances, self.angle_limit)

    def create_difficulty_screen(self): 
        easy_button = Button(self.button_surface, 'Easy', self.easy_button_center_pos, 'green')
        normal_button = Button(self.button_surface, 'Normal', self.normal_button_center_pos, 'yellow')
        self.hard = hard_button = Button(self.button_surface, 'Hard', self.hard_button_center_pos, 'red')
        self.easy = easy_button.check_collision()
        self.normal = normal_button.check_collision()
        self.hard = hard_button.check_collision()
        self.MAIN_WINDOW.fill((23, 123, 223))
        self.difficulty_screen.fill((23, 123, 223))
        self.difficulty_stairs.render()
        self.difficulty_screen.set_alpha(125)
        self.MAIN_WINDOW.blit(self.difficulty_screen, (0, 0))
        self.button_surface.set_colorkey('black')
        self.MAIN_WINDOW.blit(self.button_surface, (0, 0))
        easy_button.render()
        normal_button.render()
        hard_button.render()
        if self.easy or self.normal or self.hard:
            self.show_difficulty_screen = False

    def create_start_screen(self):
        single_player_button = Button(self.button_surface, 'One Player', self.single_player_button_center_pos, 'green')
        two_player_button = Button(self.button_surface, 'Two Players', self.two_player_button_center_pos, 'green')
        self.single_player= single_player_button.check_collision()
        two_player = two_player_button.check_collision()
        if two_player:
            self.single_player = False
        self.MAIN_WINDOW.fill((23, 123, 223))
        self.start_screen.fill((23, 123, 223))
        self.start_stairs.render()
        self.start_screen.set_alpha(125)
        self.MAIN_WINDOW.blit(self.start_screen, (0, 0))
        
        self.button_surface.set_colorkey('black')
        self.MAIN_WINDOW.blit(self.button_surface, (0, 0))
        single_player_button.render()
        two_player_button.render()
        if self.single_player or two_player:
            self.show_start_screen = False
            self.show_difficulty_screen = True

    def slide_screen_down(self, screen):
        for i in range((ut.MAIN_WINDOW_RESOLUTION[1] // 10)):
            self.MAIN_WINDOW.blit(screen, (0, i * 10))
            self.MAIN_WINDOW.blit(self.button_surface, (0, i))
            pg.display.update()

    def draw_window(self):
        if self.show_start_screen:
            self.create_start_screen()
        elif self.show_difficulty_screen:
            self.create_difficulty_screen()
        elif not self.show_start_screen and not self.show_difficulty_screen:
            self.create_game_window()
        pg.display.update() 

    def event_handler(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if not self.moved:
                        self.moved = True
                    if event.key == pg.K_LEFT:
                        self.movement_player1[0] = True
                    if event.key == pg.K_RIGHT:
                        self.movement_player1[1] = True
                    
                    if event.key == pg.K_a:
                        self.movement_player2[0] = True
                    if event.key == pg.K_d:
                        self.movement_player2[1] = True

                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT:
                        self.movement_player1[0] = False
                    if event.key == pg.K_RIGHT:
                        self.movement_player1[1] = False

                    if event.key == pg.K_a:
                        self.movement_player2[0] = False
                    if event.key == pg.K_d:
                        self.movement_player2[1] = False

    def run(self):
        self.start_stairs = Platform(self, self.start_screen, ut.MAIN_WINDOW_RESOLUTION, (ut.MAIN_WINDOW_RESOLUTION[0] // 2, ut.MAIN_WINDOW_RESOLUTION[1]), self.platform_size, self.platform_distances)
        while self.show_start_screen:
            self.CLOCK.tick(self.FPS)
            self.event_handler()
            self.start_stairs.update()
            self.draw_window()

        self.slide_screen_down(self.start_screen)
        self.button_surface.fill((0, 0, 0))
        self.difficulty_stairs = Platform(self, self.difficulty_screen, ut.MAIN_WINDOW_RESOLUTION, (ut.MAIN_WINDOW_RESOLUTION[0] // 2, ut.MAIN_WINDOW_RESOLUTION[1]), self.platform_size, self.platform_distances)
        while self.show_difficulty_screen:
            self.CLOCK.tick(self.FPS)
            self.event_handler()
            self.difficulty_stairs.update()
            self.draw_window()

        self.slide_screen_down(self.difficulty_screen)
        self.create_game_data()
        self.moved = False
        while self.running:
            self.CLOCK.tick(self.FPS)
            self.event_handler()
            self.draw_window()
            
            self.player1.update(platforms=self.platforms1.platforms, platform_rects=self.platforms1.platform_rects, movement=self.movement_player1)
            self.platforms1.update(self.moved)
            if not self.single_player:
                self.platforms2.update(self.moved)
                self.player2.update(platforms=self.platforms2.platforms, platform_rects=self.platforms2.platform_rects, movement=self.movement_player2)
            

if __name__ == '__main__':
    Game().run()    