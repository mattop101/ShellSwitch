import pygame
import sys
from shellswitch_lib import ShellSwitchGameGrid

DISPLAY_WIDTH = 512
DISPLAY_HEIGHT = 384
            
class ShellSwitcher:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("Shell Switch")

        self.background = pygame.image.load("assets/bg0.png").convert()
        self.tile_sprites = (pygame.image.load("assets/tile_bomb.png"),
                             pygame.image.load("assets/tile_1.png"),
                             pygame.image.load("assets/tile_2.png"),
                             pygame.image.load("assets/tile_3.png"),
                             pygame.image.load("assets/tile_0.png"))

        self.sounds = {'click': pygame.mixer.Sound("assets/click.ogg"),
                       'expl': pygame.mixer.Sound("assets/expl.ogg"),
                       'point': pygame.mixer.Sound("assets/point.ogg")}

        pygame.mixer.music.load("assets/main.ogg")
        pygame.mixer.music.play(loops=-1)

        self.grid_data = ShellSwitchGameGrid()
        self.level = 0
        self.score = 0
        self.score_display = 0
        self.max_score = 0
        self.game_over = False



        self.load_grid()

    def load_grid(self):
        """
        Generates the game grid and associates each tile with the blank tile sprite
        """
        self.grid_data.gen_grid(self.level)
        self.max_score = self.grid_data.max_score()

        for row in range(self.grid_data.rows):
            for col in range(self.grid_data.cols):
                data_tile = self.grid_data.get_cell(row, col)
                data_tile.sprite = self.tile_sprites[4]

        self.counter_bombs_y = [self.grid_data.bombs_in_row(i) for i in range(self.grid_data.rows)]
        self.counter_bombs_x = [self.grid_data.bombs_in_col(j) for j in range(self.grid_data.cols)]
        self.counter_score_y = [self.grid_data.points_in_row(k) for k in range(self.grid_data.rows)]
        self.counter_score_x = [self.grid_data.points_in_col(l) for l in range(self.grid_data.cols)]

    def check_tiles(self, mouse_pos):
        """
        Change the clicked tile to the corresponding sprite
        """
        for tile in self.grid_data:
            if tile.area.collidepoint(mouse_pos) and not tile.is_clicked:
                if self.score == 0:
                    self.score = tile.mult
                else:
                    self.score *= tile.mult

                self.sounds['click'].play()
                tile.sprite = self.tile_sprites[tile.mult]
                tile.is_clicked = True

                # If bomb is clicked
                if tile.mult == 0:
                    self.screen.blit(tile.sprite, tile.pos.get_tuple())
                    pygame.display.update()
                    pygame.time.wait(500)
                    self.sounds['expl'].play()
                    self.score_display = 0
                    self.game_over = True


    def run(self):
        """
        Run the main game loop
        """
        clock = pygame.time.Clock()
        pygame.font.init()
        font_score = pygame.font.SysFont("Impact", 44)
        font_counter_score = pygame.font.SysFont("Impact", 12)
        font_counter_bombs = pygame.font.SysFont("Impact", 24)
        
        while True:
            clock.tick(25)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.check_tiles(pygame.mouse.get_pos())

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))

            for tile in self.grid_data:
                self.screen.blit(tile.sprite, tile.pos.get_tuple())

            if self.game_over:
                pygame.time.wait(1500)
                self.load_grid()
                self.game_over = False

            # Handle scoring
            if self.score_display != self.score:
                self.score_display += 1
                self.sounds['point'].play()
            self.screen.blit(font_score.render(str(self.score_display), -1, (255, 222, 0)), (54, 128))

            # Draw counters
            for i in range(5):
                self.screen.blit(font_counter_score.render(str(self.counter_score_y[i]), -1, (67, 67, 67)), (464, 8 + i * (self.grid_data.gap_x + self.grid_data.tile_size)))
                self.screen.blit(font_counter_bombs.render(str(self.counter_bombs_y[i]), -1, (67, 67, 67)), (482, 26 + i * (self.grid_data.gap_x + self.grid_data.tile_size)))

                self.screen.blit(font_counter_score.render(str(self.counter_score_x[i]), -1, (67, 67, 67)), (146 + i * (self.grid_data.gap_x + self.grid_data.tile_size), 328))
                self.screen.blit(font_counter_bombs.render(str(self.counter_bombs_x[i]), -1, (67, 67, 67)), (164 + i * (self.grid_data.gap_x + self.grid_data.tile_size), 346))

            if self.score_display == self.grid_data.max_score():
                self.level += 1
                self.score = 0
                self.score_display = 0
                print(self.level)
                self.load_grid()

            pygame.display.update()

if __name__ == "__main__":
    ShellSwitcher().run()