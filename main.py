import os
import sys
import pygame

pygame.init()
pygame.mixer.init()

# Константы для скорости игрока, силы прыжка, гравитации
MOVE_SPEED = 7
JUMP_POWER = 15
GRAVITY = 0.9
size = width, height = 900, 600
screen = pygame.display.set_mode(size)
# Все группы спрайтов объектов
all_sprites = pygame.sprite.Group()
object_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
blue_blocks = pygame.sprite.Group()
red_blocks = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 60

# Звук нажатия кнопки в главном меню
button_click_sound = pygame.mixer.Sound(os.path.join('data', 'button_click.mp3'))
button_click_sound.set_volume(0.5)

# Музыка главного меню
menu_sound = pygame.mixer.Sound(os.path.join('data', 'main_menu.mp3'))
menu_sound.set_volume(0.1)
# Зацикленное проигрывание

# Музыка в игре
game_sound = pygame.mixer.Sound(os.path.join('data', 'Bad_Piggies.mpeg'))
game_sound.set_volume(0.1)

fin_sound = pygame.mixer.Sound(os.path.join('data', 'fin_sound.mp3'))
fin_sound.set_volume(0.5)

win = pygame.mixer.Sound(os.path.join('data', 'total_win.mp3'))
win.set_volume(0.5)


def terminate():
    # Завершение игры
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    # Загрузка файлов из папки data
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
    # Текст для кнопок в главном меню
    menu_sound.play(-1)
    text = ["Новая игра", "Выбор уровня", "Выйти из игры"]
    background = load_image('loadingscreen.png')
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 40)
    coord = 150
    newgameButton = pygame.sprite.Sprite()
    choiceLvl = pygame.sprite.Sprite()
    exitButton = pygame.sprite.Sprite()
    lst = [newgameButton, choiceLvl, exitButton]
    # Располагаем кнопки на экране
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
                button_click_sound.play()
                if lst:
                    # Выход из игры
                    if lst[2].rect.collidepoint(event.pos):
                        terminate()
                    # Новая игра
                    elif lst[0].rect.collidepoint(event.pos):
                        new_game(0)
                    # Выбор уровня
                    elif lst[1].rect.collidepoint(event.pos):
                        choiceLevel(lst)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)


def new_game(ind):
    levels = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt',
              "level5.txt", "level6.txt", "level7.txt", "level8.txt"]
    # При выборе уровня через choice level начинаем игру с этого уровня и проходим все последующие
    # Запускаем музыку игры зацикленно
    game_sound.play(-1)
    menu_sound.stop()
    for level in levels[ind:]:
        run_level(level)
    # Возвращаемся в главное меню после завершения всех уровней
    game_sound.stop()
    win.play()
    start_screen()


def choiceLevel(lst):
    # Текст для кнопок
    text = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8"]
    lst.clear()
    background = load_image('loadingscreen.png')
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 40)
    coord = 150
    level_1 = pygame.sprite.Sprite()
    level_2 = pygame.sprite.Sprite()
    level_3 = pygame.sprite.Sprite()
    level_4 = pygame.sprite.Sprite()
    level_5 = pygame.sprite.Sprite()
    level_6 = pygame.sprite.Sprite()
    level_7 = pygame.sprite.Sprite()
    level_8 = pygame.sprite.Sprite()
    lst = [level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8]
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
                button_click_sound.play()
                if lst[0].rect.collidepoint(event.pos):
                    new_game(0)
                elif lst[1].rect.collidepoint(event.pos):
                    new_game(1)
                elif lst[2].rect.collidepoint(event.pos):
                    new_game(2)
                elif lst[3].rect.collidepoint(event.pos):
                    new_game(3)
                elif lst[4].rect.collidepoint(event.pos):
                    new_game(4)
                elif lst[5].rect.collidepoint(event.pos):
                    new_game(5)
                elif lst[6].rect.collidepoint(event.pos):
                    new_game(6)
                elif lst[7].rect.collidepoint(event.pos):
                    new_game(7)

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
    # Обрабатываем объекты из txt файла и создаем их спрайты
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            # Синий блок
            if level_map[y][x] == '-':
                Object('blocks.png', x, y, 1)
            # Фиолетовый блок
            elif level_map[y][x] == '#':
                Object('purpleblock.png', x, y, 0)
            # Финиш
            elif level_map[y][x] == '&':
                finish = Finish(x, y, 0)
            # Красный блок
            elif level_map[y][x] == '*':
                Object('blocks.png', x, y, 2)
            elif level_map[y][x] == '^':
                Object('spike.png', x, y, -1)
            # Синий игрок
            elif level_map[y][x] == 'X':
                player1 = Player(x, y, 1)
            # Красный игрок
            elif level_map[y][x] == 'Y':
                player2 = Player(x, y, 2)
    return player1, player2, finish


class Object(pygame.sprite.Sprite):
    # Класс для блоков (красных, синих, фиолетовых, финиша)
    def __init__(self, img, x, y, fl):
        super().__init__(object_group, all_sprites)
        # Запоминаем тип блока: 0 - финиш или фиолетовый, 1 - синий, 2 - красный
        self.fl = fl
        if fl in [1, 2]:
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
        if fl == -1:
            self.mask = pygame.mask.from_surface(self.image)
        self.add(object_group, all_sprites)

    def update(self):
        # При нажатии на пробел меняем красные блоки на синие, синие на красные
        if self.fl in [1, 2]:
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

            # Спрайты первого игрока
            if col >= 4:
                frames_player1.append(frame)
            # Спрайты второго игрока
            else:
                frames_player2.append(frame)

    return frames_player1, frames_player2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, typ):
        super().__init__(player_group, all_sprites)
        # Запоминаем начальные координаты, чтобы вернуть игрока, если выйдет за пределы
        self.startpos = (50 * x, 50 * y)
        self.typ = typ

        # Получаем список всех спрайтов из players_sprite.png
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

        # Проверка на тип игрока (1 - синий, 2 - красный)
        if self.typ == 1:
            self.image = self.frames_player1[self.animation_frames['inactive'][self.current_frame]]
        else:
            self.image = self.frames_player2[self.animation_frames_player2['inactive'][self.current_frame]]

        self.rect = self.image.get_rect().move(50 * x, 50 * y)
        # Флаги: стояния на земле, движения влево/вправо/вверх; скорость по x, по y
        self.onGround = False
        self.left = False
        self.right = False
        self.up = False
        self.x_v = 0
        self.y_v = 0

    def update(self):
        if self.up:
            # Прыгаем только если на земле
            if self.onGround:
                self.y_v = -JUMP_POWER
        if self.left:
            self.x_v = -MOVE_SPEED
            # Пока в полете проигрываем анимацию ходьбы
            if not self.onGround:
                self.current_animation = 'walk'
        if self.right:
            self.x_v = MOVE_SPEED
            if not self.onGround:
                self.current_animation = 'walk'

        # Анимация бездействия
        if not (self.left or self.right):
            self.x_v = 0
            self.current_animation = 'inactive'

        # В полете падаем под действием гравитации
        if not self.onGround:
            self.y_v += GRAVITY

        # Проигрываем анимацию
        self.animate()

        self.onGround = False
        self.rect.y += self.y_v
        self.collider(0, self.y_v)
        self.rect.x += self.x_v
        self.collider(self.x_v, 0)

        # Возвращаемся в начальные координаты, если вышли за пределы
        if self.rect.y > 660:
            x, y = self.startpos
            self.rect = self.image.get_rect().move(x, y)

    def animate(self):
        # Проверяем что за игрок (красный/синий) и проигрываем соответсвующую анимацию
        if self.typ == 1:
            animation_frames = self.animation_frames[self.current_animation]
            frame_index = animation_frames[self.current_frame % len(animation_frames)]
            self.image = self.frames_player1[frame_index]
        else:
            animation_frames = self.animation_frames_player2[self.current_animation]
            frame_index = animation_frames[self.current_frame % len(animation_frames)]
            self.image = self.frames_player2[frame_index]

        # Зеркалим спрайт в зависимости от направления движения
        if self.right and self.typ == 1 or self.typ == 2 and (not self.right):
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.left and self.typ == 1 or self.typ == 2 and (not self.left):
            self.image = pygame.transform.flip(self.image, False, False)

        self.current_frame += 1

    def collider(self, xv, yv):
        # Проверка пересечения с блоками
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
            elif obj.fl == -1:
                if pygame.sprite.collide_mask(self, obj):
                    self.rect = self.image.get_rect().move(self.startpos)


class Finish(pygame.sprite.Sprite):
    # Класс финиша
    def __init__(self, x, y, fl):
        super().__init__(all_sprites, finish_group)
        self.image = load_image('finish.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * x, 50 * y)
        self.fl = fl


def draw_pause_screen():
    # Затемнение фона
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Полупрозрачный черный цвет
    screen.blit(overlay, (0, 0))

    # Располагаем надпись "ПАУЗА" в центре экрана
    font = pygame.font.Font(None, 74)
    text = font.render("ПАУЗА", True, pygame.Color('white'))
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(text, text_rect)

    # Кнопка "Выйти в главное меню"
    font = pygame.font.Font(None, 65)
    menu_text = font.render("Выйти в главное меню", True, pygame.Color('white'))
    menu_rect = menu_text.get_rect(center=(width // 2, height // 2 + 25))
    screen.blit(menu_text, menu_rect)

    return menu_rect


def run_level(level_file):
    global menu_rect
    player1, player2, finish = draw_level(load_level(level_file))
    running = True
    # Сколько проверять пересечений с финишем в зависимости от количества игроков
    fin_per = 2 if player2 is not None else 1
    # Флаг для отслеживания состояния паузы
    paused = False
    # Переменная для хранения последнего кадра игры
    last_frame = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                # Переключение паузы по нажатию Escape
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        # Сохраняем последний кадр игры
                        last_frame = screen.copy()
                        # Пауза музыки
                        pygame.mixer.pause()
                    else:
                        # Сбрасываем состояние кнопок при выходе из паузы
                        player1.right = False
                        player1.left = False
                        player1.up = False
                        if player2:
                            player2.right = False
                            player2.left = False
                            player2.up = False
                        # Возобновление музыки
                        pygame.mixer.unpause()
                # Обрабатываем управление только если игра не на паузе
                if not paused:
                    if event.key == pygame.K_d:
                        player1.right = True
                    if event.key == pygame.K_a:
                        player1.left = True
                    if event.key == pygame.K_w:
                        player1.up = True
                    if event.key == pygame.K_RIGHT and player2:
                        player2.right = True
                    if event.key == pygame.K_LEFT and player2:
                        player2.left = True
                    if event.key == pygame.K_UP and player2:
                        player2.up = True
            # Обрабатываем отпускание клавиш только если игра не на паузе
            if event.type == pygame.KEYUP and not paused:
                if event.key == pygame.K_d:
                    player1.right = False
                if event.key == pygame.K_a:
                    player1.left = False
                if event.key == pygame.K_w:
                    player1.up = False
                if event.key == pygame.K_RIGHT and player2:
                    player2.right = False
                if event.key == pygame.K_LEFT and player2:
                    player2.left = False
                if event.key == pygame.K_UP and player2:
                    player2.up = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not paused:
                red_blocks.empty()
                blue_blocks.empty()
                object_group.update()
            if event.type == pygame.MOUSEBUTTONDOWN and paused:
                # Проверка нажатия кнопки "Выйти в главное меню"
                if menu_rect.collidepoint(event.pos):
                    # Возвращаемся в главное меню
                    all_sprites.empty()
                    object_group.empty()
                    red_blocks.empty()
                    blue_blocks.empty()
                    player_group.empty()
                    finish_group.empty()
                    pygame.mixer.music.unpause()
                    start_screen()
                    return

        # Обновляем игру только если игра не на паузе
        if not paused:
            if len(pygame.sprite.spritecollide(finish, player_group, False)) != fin_per:
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
                fin_sound.play()
                all_sprites.empty()
                object_group.empty()
                red_blocks.empty()
                blue_blocks.empty()
                player_group.empty()
                finish_group.empty()
                return
        # Если игра на паузе, отображаем сохраненный кадр
        else:
            if last_frame:
                screen.blit(last_frame, (0, 0))
            menu_rect = draw_pause_screen()

        pygame.display.flip()
        clock.tick(fps)


start_screen()