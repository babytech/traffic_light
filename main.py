# -*- coding: utf-8 -*-

# 本程序模拟红绿灯交通信号灯运行
# 行人根据红绿灯状态，通过人行横道斑马线
# 车辆根据路口红绿灯状态“红灯停，绿灯行”

# 导入程序相关的模块
import threading
import time
from pathlib import Path
import pygame

# 窗口大小与按钮字体颜色
display_width = 1024
display_height = 768
RED = (255, 0, 0)
BLUE = (0, 174, 239)
GREEN = (106, 168, 79)

# 全局状态
current_color = "green"  # 当前信号灯颜色（"green" 或 "red"，yellow可视情况处理）
objects_move_list = []  # 保存所有移动对象


class MoveObject:
    def __init__(self, item_, x, y, direction, begin, end, step, line_min, line_max):
        self._x = x
        self._y = y
        self._direction = direction  # "left"/"right" 表示车辆，"up"/"down" 表示行人
        self._item = item_
        self._begin = begin
        self._end = end
        self._step = step
        # 停止标志不再由区域判断控制，由信号直接决定
        self._line_min = line_min
        self._line_max = line_max

    def current_direction(self):
        return self._direction

    def current_position(self):
        return self._x, self._y

    def update(self, signal_color):
        # 对于车辆（左右行驶），只有在绿灯时正常行驶
        if self._direction in ["right", "left"]:
            if signal_color != "green":
                # 非绿灯时，车辆需要慢行直到停在停止线内，但如果已越过则继续
                if self._direction == "right":
                    # 停止线区域为 [line_min, line_max]
                    if self._x < self._line_min:
                        next_x = self._x + self._step
                        if next_x >= self._line_min:
                            self._x = self._line_min  # 到达停止线
                        else:
                            self._x = next_x
                    elif self._line_min <= self._x <= self._line_max:
                        # 已在停止线内，保持不动
                        return
                    else:  # self._x > self._line_max, 已越过停止线
                        self._x += self._step
                        if self._x > self._end + self._item.get_width():
                            self._x = self._begin - self._item.get_width()
                elif self._direction == "left":
                    # 对于向左行驶，若 x > line_max 表示还未到达停止线
                    if self._x > self._line_max:
                        next_x = self._x - self._step
                        if next_x <= self._line_max:
                            self._x = self._line_max
                        else:
                            self._x = next_x
                    elif self._line_min <= self._x <= self._line_max:
                        return
                    else:  # self._x < self._line_min, 已越过停止线
                        self._x -= self._step
                        if self._x < self._end - self._item.get_width():
                            self._x = self._begin + self._item.get_width()
            else:
                # 绿灯时，车辆正常行驶
                if self._direction == "right":
                    self._x += self._step
                    if self._x > self._end + self._item.get_width():
                        self._x = self._begin - self._item.get_width()
                elif self._direction == "left":
                    self._x -= self._step
                    if self._x < self._end - self._item.get_width():
                        self._x = self._begin + self._item.get_width()

        # 对于行人（上下行驶），只有在红灯时正常过街
        elif self._direction in ["down", "up"]:
            if signal_color != "red":
                # 非红灯时，行人慢行直至停止线内，若已越过则继续前进
                if self._direction == "down":
                    if self._y < self._line_min:
                        next_y = self._y + self._step
                        if next_y >= self._line_min:
                            self._y = self._line_min
                        else:
                            self._y = next_y
                    elif self._line_min <= self._y <= self._line_max:
                        return
                    else:  # self._y > self._line_max, 已越过停止线
                        self._y += self._step
                        if self._y > self._end + self._item.get_height():
                            self._y = self._begin - self._item.get_height()
                elif self._direction == "up":
                    if self._y > self._line_max:
                        next_y = self._y - self._step
                        if next_y <= self._line_max:
                            self._y = self._line_max
                        else:
                            self._y = next_y
                    elif self._line_min <= self._y <= self._line_max:
                        return
                    else:  # self._y < self._line_min, 已越过停止线
                        self._y -= self._step
                        if self._y < self._end - self._item.get_height():
                            self._y = self._begin + self._item.get_height()
            else:
                # 红灯时，行人正常过街
                if self._direction == "down":
                    self._y += self._step
                    if self._y > self._end + self._item.get_height():
                        self._y = self._begin - self._item.get_height()
                elif self._direction == "up":
                    self._y -= self._step
                    if self._y < self._end - self._item.get_height():
                        self._y = self._begin + self._item.get_height()

    def draw(self, _screen):
        _screen.blit(self._item, (int(self._x), int(self._y)))


def light_thread(obj_lists):
    global current_color, objects_move_list
    # 从 image_objects 中获取公路背景图片（顺序按前6张）
    # image_highway_red, image_highway_yellow, image_highway_green = image_objects[0:3]
    # 构造移动对象列表
    for element in obj_lists:
        obj, info = element
        direction, scope, pos, line = info
        begin, end, step = scope
        x, y = pos
        line_from, line_to = line
        it = MoveObject(obj, x, y, direction, begin, end, step, line_from, line_to)
        objects_move_list.append(it)
    count = 0
    while True:
        time.sleep(0.005)
        # 设置信号灯状态：当 count 在 [0,1000) 内视为绿灯， [1000,1300) 为黄灯（可按需求处理），[1300,3200) 为红灯
        if count < 1000:
            current_color = "green"
        elif count < 1300:
            current_color = "yellow"
        elif count < 3200:
            current_color = "red"
        else:
            count = 0
        # 更新所有对象位置（根据当前信号）
        for _item in objects_move_list:
            _item.update(current_color)
        count += 1


class Button(object):
    def __init__(self, _font, text, color, x=None, y=None, **kwargs):
        self.surface = _font.render(text, True, color)
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()
        if kwargs.get('centered_x'):
            self.x = display_width // 2 - self.WIDTH // 2
        else:
            self.x = x
        if kwargs.get('centered_y'):
            self.y = display_height // 2 - self.HEIGHT // 2
        else:
            self.y = y

    def display(self):
        screen.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        return (self.x < position[0] < self.x + self.WIDTH and
                self.y < position[1] < self.y + self.HEIGHT)


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

        for _event_ in pygame.event.get():
            if _event_.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if play_button.check_click(pygame.mouse.get_pos()):
                break
            if exit_button.check_click(pygame.mouse.get_pos()):
                raise SystemExit


if __name__ == '__main__':
    pygame.init()
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
    image_convert_types = ["standard"] * 6 + ["alpha"] * 7
    image_dict = dict(zip(image_lists, image_convert_types))
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

    # 准备对象信息（方向、移动范围、起始位置、停止区间）
    # 假设车辆方向为 "left" 或 "right"，行人方向为 "up" 或 "down"
    objects_information = [
        ("left", (680, 0, 2), (720, 270), (570, 670)),
        ("left", (680, 0, 0.8), (700, 350), (570, 670)),
        ("right", (0, 680, 1.1), (200, 470), (60, 130)),
        ("right", (0, 680, 2), (205, 570), (40, 100)),
        ("right", (0, 680, 1), (195, 660), (50, 110)),
        # 假设后面两个为行人，方向 "down"
        ("down", (280, 680, 1), (400, 150), (140, 180)),
        ("down", (280, 680, 1.05), (310, 170), (180, 200))
    ]
    objects_list = []
    # 从 image_objects 中取出车辆及行人图像（下标 6 以后）
    for idx in range(6, len(image_objects)):
        idx_tuple = image_objects[idx], objects_information[idx - 6]
        objects_list.append(idx_tuple)

    # 启动子线程，仅更新对象状态
    light = threading.Thread(target=light_thread, args=(objects_list,))
    light.daemon = True
    light.start()

    # 主线程负责事件处理与绘制
    image_highway_red, image_highway_yellow, image_highway_green = image_objects[0:3]
    image_signal_red, image_signal_yellow, image_signal_green = image_objects[3:6]
    clock = pygame.time.Clock()
    while True:
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # 根据当前信号灯绘制背景
        if current_color == "red":
            screen.blit(image_highway_red, (0, 0))
        elif current_color == "yellow":
            screen.blit(image_highway_yellow, (0, 0))
        else:
            screen.blit(image_highway_green, (0, 0))

        # 绘制所有移动对象
        for item in objects_move_list:
            item.draw(screen)

        # 绘制信号灯图像（放在固定位置）
        if current_color == "red":
            screen.blit(image_signal_red, (590, 480))
        elif current_color == "yellow":
            screen.blit(image_signal_yellow, (590, 480))
        elif current_color == "green":
            screen.blit(image_signal_green, (590, 480))

        pygame.display.update()
        clock.tick(60)
