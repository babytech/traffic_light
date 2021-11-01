# -*- coding: utf-8 -*-

# 本程序模拟红绿灯交通信号灯运行
# 行人根据红绿灯状态，通过人行横道斑马线
# 车辆根据路口红绿灯状态“红灯停，绿灯行”

# 导入程序相关的模块
import threading
import time
from pathlib import Path
import pygame

# 设置窗口大小与按钮字体颜色
display_width = 1024
display_height = 768
RED = (255, 0, 0)
BLUE = (0, 174, 239)
GREEN = (106, 168, 79)


class MoveObject:
    def __init__(self, item, x, y, direction, begin, end, step, line_min, line_max):
        self._x = x
        self._y = y
        self._direction = direction
        self._item = item
        self._begin = begin
        self._end = end
        self._step = step
        self._stop = False
        self._line_min = line_min
        self._line_max = line_max

    def current_direction(self):
        return self._direction

    def current_position(self):
        return self._x, self._y

    def yield_pedestrian(self, _objects_move_list):
        for element in _objects_move_list:
            if element.current_direction() == "up" or element.current_direction() == "down":
                x, y = element.current_position()
                if 200 < x < 400 and 200 < y < 600:
                    if self._direction == "left":
                        if x < self._x:
                            return True
                    elif self._direction == "right":
                        if x > self._x:
                            return True
                continue
        return False

    def check_stop(self, _objects_move_list):
        if self._direction == "left" or self._direction == "right":
            if self._line_min < self._x < self._line_max or self.yield_pedestrian(_objects_move_list):
                self._stop = True
        elif self._direction == "up" or self._direction == "down":
            if self._line_min < self._y < self._line_max:
                self._stop = True

    def move(self, _screen, _signal_color, _objects_move_list):
        if self._direction == "up" or self._direction == "down":
            if _signal_color == "red":
                _signal_color = "green"
            else:
                _signal_color = "red"
        self._stop = False

        if _signal_color == "red":
            self.check_stop(_objects_move_list)
        if self._stop:
            _screen.blit(self._item, (int(self._x), int(self._y)))
            return
        if self._direction == "right":
            self._x += self._step
            if self._x > self._end + self._item.get_width():
                self._x = self._begin - self._item.get_width()
            _screen.blit(self._item, (int(self._x), int(self._y)))
        elif self._direction == "left":
            self._x -= self._step
            if self._x < self._end - self._item.get_width():
                self._x = self._begin + self._item.get_width()
            _screen.blit(self._item, (int(self._x), int(self._y)))
        elif self._direction == "down":
            self._y += self._step
            if self._y > self._end + self._item.get_height():
                self._y = self._begin - self._item.get_height()
            _screen.blit(self._item, (int(self._x), int(self._y)))
        elif self._direction == "up":
            self._y -= self._step
            if self._y < self._end - self._item.get_height():
                self._y = self._begin + self._item.get_height()
            _screen.blit(self._item, (int(self._x), int(self._y)))


def light_thread(obj_lists):
    image_highway_red, image_highway_yellow, image_highway_green = image_objects[0:3]
    image_signal_red, image_signal_yellow, image_signal_green = image_objects[3:6]
    count = 0
    objects_move_list = []
    for element in obj_lists:
        obj, info = element
        direction, scope, pos, line = info
        begin, end, step = scope
        x, y = pos
        line_from, line_to = line
        it = MoveObject(obj, x, y, direction, begin, end, step, line_from, line_to)
        objects_move_list.append(it)
    _font = pygame.font.Font(font_default, 36)
    pygame.display.update()
    while True:
        pygame.display.update()
        color = "green"
        time.sleep(0.005)
        if count < 1000:
            # print("\033[42;1m--green light on--\r\033[0m")
            color = "green"
            screen.blit(image_highway_green, (0, 0))
        elif count < 1300:
            # print("\033[43;1m--yellow light on --\r\033[0m")
            color = "yellow"
            screen.blit(image_highway_yellow, (0, 0))
        elif count < 3200:
            # print("\033[41;1m--red light on--\r\033[0m")
            color = "red"
            screen.blit(image_highway_red, (0, 0))
        else:
            count = 0
        for item in objects_move_list:
            item.move(screen, color, objects_move_list)
        if color == "red":
            screen.blit(image_signal_red, (590, 480))
        elif color == "yellow":
            screen.blit(image_signal_yellow, (590, 480))
        elif color == "green":
            screen.blit(image_signal_green, (590, 480))
        count += 1
        pygame.display.update()
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit


class Button(object):
    def __init__(self, _font, text, color, x=None, y=None, **kwargs):
        self.surface = _font.render(text, True, color)
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()
        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = display_width // 2 - self.WIDTH // 2
        else:
            self.x = x
            self.x = x
        if 'centered_y' in kwargs and kwargs['centered_y']:
            self.y = display_height // 2 - self.HEIGHT // 2
        else:
            self.y = y

    def display(self):
        screen.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        x_match = self.x < position[0] < self.x + self.WIDTH
        y_match = self.y < position[1] < self.y + self.HEIGHT
        if x_match and y_match:
            return True
        else:
            return False


def starting_screen(_background, _font):
    screen.blit(_background, (0, 0))
    play_button = Button(_font, 'Play', RED, None, 400, centered_x=True)
    exit_button = Button(_font, 'Exit', BLUE, None, 450, centered_x=True)
    play_button.display()
    exit_button.display()
    pygame.display.update()

    while True:
        if play_button.check_click(pygame.mouse.get_pos()):
            play_button = Button(_font, 'Play', GREEN, None, 400, centered_x=True)
        else:
            play_button = Button(_font, 'Play', BLUE, None, 400, centered_x=True)
        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button(_font, 'Exit', RED, None, 450, centered_x=True)
        else:
            exit_button = Button(_font, 'Exit', BLUE, None, 450, centered_x=True)
        play_button.display()
        exit_button.display()
        pygame.display.update()

        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if play_button.check_click(pygame.mouse.get_pos()):
                break
            if exit_button.check_click(pygame.mouse.get_pos()):
                raise SystemExit


if __name__ == '__main__':
    # 背景图以及移动小车图
    pygame.init()

    # 生成窗口以及窗口标题
    image_base_dir = Path("resource")
    bg_location = str(image_base_dir / 'welcome.png')
    screen = pygame.display.set_mode((display_width, display_height), 0, 32)
    pygame.display.set_caption("小叮当红绿灯程序")
    bg = pygame.image.load(bg_location)
    font_default = pygame.font.get_default_font()
    font = pygame.font.Font(font_default, 36)
    starting_screen(bg, font)

    # 加载并转换图片
    image_lists = ["highway_red.png", "highway_yellow.png", "highway_green.png",
                   "signal_red.png", "signal_yellow.png", "signal_green.png",
                   "car_yellow.png", "car_green.png", "car_driver.png", "car_purple.png",
                   "car_brown.png", "children.png", "doraemon.png"]
    image_covert_types = ["standard", "standard", "standard",
                          "standard", "standard", "standard",
                          "alpha", "alpha", "alpha", "alpha",
                          "alpha", "alpha", "alpha"]
    image_dict = dict(zip(image_lists, image_covert_types))
    image_objects = []
    for key, value in image_dict.items():
        image_file = str(image_base_dir / key)
        if value == "standard":
            img = pygame.image.load(image_file).convert()
        elif value == "alpha":
            img = pygame.image.load(image_file).convert_alpha()
        else:
            img = None
        image_objects.append(img)

    # 开启红绿灯线程
    event = threading.Event()
    # direction, scope(begin, end, step), position(x,y), stop(from, to)
    objects_information = [("left", (680, 0, 2), (720, 270), (570, 670)),
                           ("left", (680, 0, 0.8), (700, 350), (570, 670)),
                           ("right", (0, 680, 1.1), (200, 470), (60, 130)),
                           ("right", (0, 680, 2), (205, 570), (40, 100)),
                           ("right", (0, 680, 1), (195, 660), (50, 110)),
                           ("down", (280, 680, 1), (400, 150), (140, 180)),
                           ("down", (280, 680, 1.05), (310, 170), (180, 200))]
    objects_list = []
    for idx in range(6, len(image_objects)):
        idx_tuple = image_objects[idx], objects_information[idx - 6]
        objects_list.append(idx_tuple)
    light = threading.Thread(target=light_thread, args=(objects_list,))
    light.start()
