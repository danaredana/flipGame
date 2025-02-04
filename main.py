import os
import sys
import pygame

pygame.init()
pygame.mixer.init()

MOVE_SPEED = 7
JUMP_POWER = 15
GRAVITY = 0.9
size = width, height = 900, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
object_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
blue_blocks = pygame.sprite.Group()
red_blocks = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 60

pygame.mixer.music.load(os.path.join('data', 'Bad_Piggies.mpeg'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


def terminate():
    pygame.quit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    text = ["Новая игра", "Выбор уровня", "Выйти из игры"]
    background = load_image('loadingscreen.png')
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 40)
    coord = 150
    newgameButton = pygame.sprite.Sprite()
    choiceLvl = pygame.sprite.Sprite()
    exitButton = pygame.sprite.Sprite()
    lst = [newgameButton, choiceLvl, exitButton]
    for i, elem in enumerate(text):
        s = font.render(elem, True, pygame.Color('purple'))
        s_rect = s.get_rect()
        coord += 20
        s_rect.top = coord
        s_rect.x = 375
        lst[i].rect = s_rect
        coord += s_rect.height
        screen.blit(s, s_rect)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if lst:
                    # кнопка выхода из игры
                    if lst[2].rect.collidepoint(event.pos):
                        terminate()
                    elif lst[0].rect.collidepoint(event.pos):
                        new_game()
                    elif lst[1].rect.collidepoint(event.pos):
                        choiceLevel(lst)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)


def new_game():
    level1()
    level2()
    level3()
    level4()
    terminate()


def choiceLevel(lst):
    text = ["Level 1", "Level 2", "Level 3", "Level 4"]
    lst.clear()
    background = load_image('loadingscreen.png')
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 40)
    coord = 150
    # можно переделать кнопки
    level_1 = pygame.sprite.Sprite()
    level_2 = pygame.sprite.Sprite()
    level_3 = pygame.sprite.Sprite()
    level_4 = pygame.sprite.Sprite()
    lst = [level_1, level_2, level_3, level_4]
    for i, elem in enumerate(text):
        s = font.render(elem, True, pygame.Color('purple'))
        s_rect = s.get_rect()
        coord += 20
        s_rect.top = coord
        s_rect.x = 375
        lst[i].rect = s_rect
        coord += s_rect.height
        screen.blit(s, s_rect)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if lst[0].rect.collidepoint(event.pos):
                    new_game()
                elif lst[1].rect.collidepoint(event.pos):
                    level2()
                    level3()
                    level4()
                    terminate()
                elif lst[2].rect.collidepoint(event.pos):
                    level3()
                    level4()
                    terminate()
                elif lst[3].rect.collidepoint(event.pos):
                    level4()
                    terminate()

        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)


def load_level(name):
    name = 'data/' + name
    level_map = []
    with open(name) as f:
        for s in f:
            level_map.append(s.strip())
    return level_map


def draw_level(level_map):
    player1, player2, finish = None, None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '-':
                Object('blocks.png', x, y, 1)
            elif level_map[y][x] == '#':
                Object('purpleblock.png', x, y, 0)
            elif level_map[y][x] == '&':
                finish = Finish(x, y, 0)
            elif level_map[y][x] == '*':
                Object('blocks.png', x, y, 2)
            elif level_map[y][x] == 'X':
                player1 = Player(x, y, 1)
            elif level_map[y][x] == 'Y':
                player2 = Player(x, y, 2)
    return player1, player2, finish


class Object(pygame.sprite.Sprite):
    def __init__(self, img, x, y, fl):
        super().__init__(object_group, all_sprites)
        self.fl = fl
        if fl != 0:
            self.blue = load_image(img).subsurface(pygame.Rect(0, 0, 50, 50))
            self.red = load_image(img).subsurface(pygame.Rect(0, 50, 50, 50))
            if fl == 1:
                self.image = self.blue
                super().__init__(blue_blocks)
            else:
                self.image = self.red
                super().__init__(red_blocks)
        else:
            self.image = load_image(img)
        self.rect = self.image.get_rect().move(50 * x, 50 * y)
        self.add(object_group, all_sprites)

    def update(self):
        if self.fl != 0:
            if self.image == self.blue:
                self.image = self.red
                self.fl = 2
                self.add(red_blocks)
            else:
                self.image = self.blue
                self.fl = 1
                self.add(blue_blocks)


def load_sprite_sheet(image_path, cell_width, cell_height, rows, cols):
    sheet = load_image(image_path, colorkey=-1)
    frames_player1 = []
    frames_player2 = []

    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
            frame = sheet.subsurface(rect)
            frame = pygame.transform.scale(frame, (50, 50))

            if col >= 4:  # первый игрок
                frames_player1.append(frame)
            else:  # второй игрок
                frames_player2.append(frame)

    return frames_player1, frames_player2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, typ):
        super().__init__(player_group, all_sprites)
        self.startpos = (50 * x, 50 * y)
        self.typ = typ

        self.frames_player1, self.frames_player2 = load_sprite_sheet('players_sprite.png', 24, 24, 11, 8)

        self.animation_frames = {
            'inactive': [28, 29, 30, 31],
            'walk': [8, 9, 10],
        }

        self.animation_frames_player2 = {
            'inactive': [28, 29, 30, 31],
            'walk': [8, 9, 10],
        }

        self.current_frame = 0
        self.current_animation = 'inactive'

        if self.typ == 1:
            self.image = self.frames_player1[self.animation_frames['inactive'][self.current_frame]]
        else:
            self.image = self.frames_player2[self.animation_frames_player2['inactive'][self.current_frame]]

        self.rect = self.image.get_rect().move(50 * x, 50 * y)
        self.onGround = False
        self.left = False
        self.right = False
        self.up = False
        self.x_v = 0
        self.y_v = 0

    def update(self):
        if self.up:
            if self.onGround:
                self.y_v = -JUMP_POWER
        if self.left:
            self.x_v = -MOVE_SPEED
            if not self.onGround:
                self.current_animation = 'walk'
        if self.right:
            self.x_v = MOVE_SPEED
            if not self.onGround:
                self.current_animation = 'walk'

        if not (self.left or self.right):
            self.x_v = 0
            self.current_animation = 'inactive'

        if not self.onGround:
            self.y_v += GRAVITY

        self.animate()

        self.onGround = False
        self.rect.y += self.y_v
        self.collider(0, self.y_v)
        self.rect.x += self.x_v
        self.collider(self.x_v, 0)

        if self.rect.y > 660:
            x, y = self.startpos
            self.rect = self.image.get_rect().move(x, y)

    def animate(self):
        if self.typ == 1:
            animation_frames = self.animation_frames[self.current_animation]
            frame_index = animation_frames[self.current_frame % len(animation_frames)]
            self.image = self.frames_player1[frame_index]
        else:
            animation_frames = self.animation_frames_player2[self.current_animation]
            frame_index = animation_frames[self.current_frame % len(animation_frames)]
            self.image = self.frames_player2[frame_index]

        # зеркалим спрайт в зависимости от направления движения
        if self.right and self.typ == 1 or self.typ == 2 and (not self.right):
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.left and self.typ == 1 or self.typ == 2 and (not self.left):
            self.image = pygame.transform.flip(self.image, False, False)

        self.current_frame += 1

    def collider(self, xv, yv):
        for obj in object_group:
            if self.typ == obj.fl or obj.fl == 0:
                if pygame.sprite.collide_rect(self, obj):
                    if xv > 0:
                        self.rect.right = obj.rect.left
                    if xv < 0:
                        self.rect.left = obj.rect.right
                    if yv > 0:
                        self.rect.bottom = obj.rect.top
                        self.onGround = True
                        self.y_v = 0
                    if yv < 0:
                        self.rect.top = obj.rect.bottom
                        self.y_v = 0


class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y, fl):
        super().__init__(all_sprites, finish_group)
        self.image = load_image('finish.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * x, 50 * y)
        self.fl = fl


def level1():
    player1, player2, finish = draw_level(load_level('level1.txt'))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                player1.right = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                player1.left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                player1.up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                player1.right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                player1.left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                player1.up = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                red_blocks.empty()
                blue_blocks.empty()
                object_group.update()
        if not pygame.sprite.collide_rect(player1, finish):
            screen.fill(pygame.Color('white'))
            object_group.draw(screen)
            player_group.update()
            player_group.draw(screen)
            finish_group.draw(screen)
        else:
            all_sprites.empty()
            object_group.empty()
            red_blocks.empty()
            blue_blocks.empty()
            player_group.empty()
            finish_group.empty()
            return
        pygame.display.flip()
        clock.tick(fps)


def level2():
    player1, player2, finish = draw_level(load_level('level2.txt'))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                player1.right = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                player1.left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                player1.up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                player1.right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                player1.left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                player1.up = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player2.right = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player2.left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player2.up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                player2.right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                player2.left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                player2.up = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                red_blocks.empty()
                blue_blocks.empty()
                object_group.update()
        if len(pygame.sprite.spritecollide(finish, player_group, False)) != 2:
            if len(pygame.sprite.spritecollide(finish, player_group, False)) == 1:
                fin_player = pygame.sprite.spritecollide(finish, player_group, False)[0]
                if fin_player.y_v > 0:
                    fin_player.rect.bottom = finish.rect.top
                    fin_player.onGround = True
                    fin_player.y_v = 0
            screen.fill(pygame.Color('white'))
            object_group.draw(screen)
            player_group.update()
            player_group.draw(screen)
            finish_group.draw(screen)
        else:
            all_sprites.empty()
            object_group.empty()
            red_blocks.empty()
            blue_blocks.empty()
            player_group.empty()
            finish_group.empty()
            return
        pygame.display.flip()
        clock.tick(fps)


def level3():
    player1, player2, finish = draw_level(load_level('level3.txt'))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                for pl in player1, player2:
                    x, y = pl.startpos
                    pl.rect.x, pl.rect.y = x, y
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                player1.right = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                player1.left = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                player1.up = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_d:
                player1.right = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_a:
                player1.left = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_w:
                player1.up = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player2.right = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player2.left = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player2.up = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                player2.right = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                player2.left = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
                player2.up = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                red_blocks.empty()
                blue_blocks.empty()
                object_group.update()
        if len(pygame.sprite.spritecollide(finish, player_group, False)) != 2:
            if len(pygame.sprite.spritecollide(finish, player_group, False)) == 1:
                fin_player = pygame.sprite.spritecollide(finish, player_group, False)[0]
                if fin_player.y_v > 0:
                    fin_player.rect.bottom = finish.rect.top
                    fin_player.onGround = True
                    fin_player.y_v = 0
            screen.fill(pygame.Color('white'))
            object_group.draw(screen)
            player_group.update()
            player_group.draw(screen)
            finish_group.draw(screen)
        else:
            all_sprites.empty()
            object_group.empty()
            red_blocks.empty()
            blue_blocks.empty()
            player_group.empty()
            finish_group.empty()
            return
        pygame.display.flip()
        clock.tick(fps)


def level4():
    player1, player2, finish = draw_level(load_level('level4.txt'))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                player1.right = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                player1.left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                player1.up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                player1.right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                player1.left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                player1.up = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                red_blocks.empty()
                blue_blocks.empty()
                object_group.update()
        if not pygame.sprite.collide_rect(player1, finish):
            screen.fill(pygame.Color('white'))
            object_group.draw(screen)
            player_group.update()
            player_group.draw(screen)
            finish_group.draw(screen)
        else:
            all_sprites.empty()
            object_group.empty()
            red_blocks.empty()
            blue_blocks.empty()
            player_group.empty()
            finish_group.empty()
            return
        pygame.display.flip()
        clock.tick(fps)


start_screen()
