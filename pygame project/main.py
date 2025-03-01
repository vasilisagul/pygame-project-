import os
import random
import sys

import pygame

FPS = 50
WIDTH = 640
HEIGHT = 480
START_POSITION = WIDTH // 2, HEIGHT - 50
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
        super().__init__(all_sprites)
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
        # self.image = tile_images[tile_type]
        # self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Board(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(board_group)
        self.image = board_image
        self.rect = self.image.get_rect().move(pos_x - self.image.get_width() // 2, pos_y)
        self.pos = [pos_x, pos_y]
        print(self.pos)

    # def move(self):
    #     # self.pos = (x, y)
    #     self.rect = self.image.get_rect().move(self.pos)

    # def update(self):
    #     self.rect = self.rect.move(self.vx, self.vy)
    #     pass


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(ball_group)
        self.image = ball_image
        self.rect = self.image.get_rect().move(pos_x - self.image.get_width() // 2, pos_y)
        self.pos = [pos_x, pos_y]
        print(self.pos)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, -1)
        print(pos_x, pos_y)
        print(self.vx, self.vy)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        print('123')


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

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}

board_image = load_image('board1.png')

ball_image = load_image('ball1.png')
ball_image = pygame.transform.scale(ball_image, SIZE_BALL)

board_width = board_image.get_width()
board_height = board_image.get_height()
board = Board(START_POSITION[0], START_POSITION[1])
ball = Ball(START_POSITION[0], START_POSITION[1])
# Border(0, 0, WIDTH - 1, 0)  # верхняя
# Border(0, 0,0, HEIGHT - 1)  # левая
# Border(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)  # правая
# Border(0, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)  # нажняя


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
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


if __name__ == '__main__':
    start_screen()
    # main()
    # pygame.init()
    # w, h = 600, 300
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Игра')
    # clock = pygame.time.Clock()
    # all_sprites = pygame.sprite.Group(Car('img.png', w))
    # level_map = load_level("map.map")
    # screen.fill((255, 255, 255))
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
                    print(ball_true)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if board.rect.x + OFFSET + board_width <= WIDTH:
                board.rect.x += OFFSET
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if board.rect.x - OFFSET >= 0:
                board.rect.x -= OFFSET

        screen.fill(pygame.Color("black"))

        # all_sprites.update()
        # all_sprites.draw(screen)
        # all_sprites.update()
        board_group.draw(screen)
        ball_group.draw(screen)

        if ball_true:
            ball_group.update()
            print('1')
        pygame.display.flip()
        clock.tick(FPS)

    terminate()
