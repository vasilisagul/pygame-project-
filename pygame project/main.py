import os
import random
import sys

import pygame

FPS = 70
WIDTH = 640
HEIGHT = 480
START_POSITION = WIDTH // 2, HEIGHT - 20
OFFSET = 4
SIZE_BALL = (20, 20)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.init()

player = None
all_sprites = pygame.sprite.Group()
board_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
border_group = pygame.sprite.Group()

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Border(Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(border_group)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(self.image.get_width() * pos_x, self.image.get_height() * pos_y)


class Board(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(board_group)
        self.image = board_image
        self.rect = self.image.get_rect().move(pos_x - self.image.get_width() // 2, pos_y)
        self.pos = [pos_x, pos_y]


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(ball_group)
        self.image = ball_image
        self.rect = self.image.get_rect().move(pos_x - self.image.get_width() // 2, pos_y - SIZE_BALL[0])
        self.pos = [pos_x, pos_y]
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, -1)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if spr := pygame.sprite.spritecollideany(self, tiles_group):
            tiles_group.remove(spr)
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, board_group):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.vy >= 0:
                end_screen()
            else:
                self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '1':
                Tile('brick1', x, y)
            elif level[y][x] == '2':
                Tile('brick2', x, y)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return list(level_map)


tile_images = {'brick1': load_image('brick1.png'), 'brick2': load_image('brick2.png')}

board_image = load_image('board1.png')
board_width = board_image.get_width()
board_height = board_image.get_height()
board = Board(START_POSITION[0], START_POSITION[1])

ball_image = load_image('ball1.png')
ball_image = pygame.transform.scale(ball_image, SIZE_BALL)
ball = Ball(START_POSITION[0], START_POSITION[1])

Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

LEVELS = ["map.map", "map1.map", "map2.map", "map3.map"]
cnt_level = 0
level_map = load_level(LEVELS[cnt_level])
generate_level(level_map)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ARKANOID"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 190
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('SteelBlue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 130
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
    self.terminate()


def end_screen():
    fon = pygame.transform.scale(load_image('end_fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
    self.terminate()

def win_screen():
    fon = pygame.transform.scale(load_image('win.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
    self.terminate()



if __name__ == '__main__':
    start_screen()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Игра')

    screen.fill((0, 0, 0))
    all_sprites.update()
    running = True
    ball_true = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball_true = True
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if board.rect.x + OFFSET + board_width <= WIDTH:
                board.rect.x += OFFSET
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if board.rect.x - OFFSET >= 0:
                board.rect.x -= OFFSET

        screen.fill((0, 0, 0))

        border_group.draw(screen)
        board_group.draw(screen)
        ball_group.draw(screen)
        tiles_group.draw(screen)

        if ball_true:
            ball_group.update()
        pygame.display.flip()
        clock.tick(FPS)
        if not tiles_group:
            ball_group.empty()
            cnt_level += 1
            if cnt_level == 4:
                win_screen()
            level_map = load_level(LEVELS[cnt_level])
            generate_level(level_map)
            ball_true = False
            ball = Ball(START_POSITION[0], START_POSITION[1])
            ball_group.draw(screen)

    terminate()
