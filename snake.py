"""
keyboard need permission.
works better under tmux.
"""

from typing import List
import os
import time
import random
import keyboard
import copy


class Game:
    run = True
    width = 180
    height = 30
    map_style = '.'

    def __init__(self):
        self.pause = False
        self.map = [self.map_style * self.width for _ in range(self.height)]
        self.obj_list: List[Obj] = []
        self.snake = Snake(self.width, self.height)

        self.food = Food(self.width, self.height)

    def _form_obj_list(self):
        self.obj_list = []
        for body in self.snake.body_list:
            body.style = "#"

        self.snake.body_list[-1].style = "A"

        self.obj_list.extend(self.snake.body_list)
        self.obj_list.append(self.food)

    def start(self):
        while self.run:
            if keyboard.is_pressed('p'):
                self.pause = True
                while self.pause:
                    time.sleep(0.02)
                    if keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('a') or keyboard.is_pressed('d'):
                        self.pause = False

            self._form_obj_list()
            self.update()
            self.snake.move()

            if self.snake.body_list[-1].pos == self.food.pos:  # update food
                self.food = Food(self.width, self.height)
                self.snake.eat()

            if keyboard.is_pressed('up') or keyboard.is_pressed('w'):
                self.snake.move(0)
                continue
            if keyboard.is_pressed('down') or keyboard.is_pressed('s'):
                self.snake.move(1)
                continue
            if keyboard.is_pressed('left') or keyboard.is_pressed('a'):
                self.snake.move(2)
                continue
            if keyboard.is_pressed('right') or keyboard.is_pressed('d'):
                self.snake.move(3)
                continue

    def update(self):
        # update map by object state.

        os.system('clear')
        view_map = copy.deepcopy(self.map)  # the view map is a deep copy of map, discarded in each update.
        print('snake head: ', self.snake.body_list[-1].pos, 'length: ', len(self.snake.body_list))

        for o in self.obj_list:
            x, y = o.pos
            if x < self.height and y < self.width:  # if x, y are outside of the map
                map_row = view_map[x]
                map_dots = [map_row[i] for i in range(len(map_row))]
                map_dots[y] = o.style

                new_row = ''
                for dot in map_dots:
                    new_row += dot
                view_map[x] = new_row

        for row in view_map:  # print row by row
            print(row)

        time.sleep(0.03)


class Obj:
    def __init__(self, x, y, style):
        self.pos = (x, y)
        self.style = style


class Food(Obj):
    def __init__(self, width, height):
        super().__init__(random.randint(0, height - 1), random.randint(0, width - 1), '@')


class SnakeBody(Obj):
    def __init__(self, x, y):
        super().__init__(x, y, '#')


class Snake:
    body_list: List[SnakeBody] = []

    def __init__(self, width, height):
        self.body_list.append(SnakeBody(random.randint(0, height - 1), random.randint(0, width - 1)))
        self.direction = 0  # init direction 0 left, 1 right, 2 up, 3 down.

    def eat(self):
        last_x, last_y = self.body_list[-1].pos
        if self.direction == 0:
            self.body_list.append(SnakeBody(last_x - 1, last_y))

        if self.direction == 1:
            self.body_list.append(SnakeBody(last_x + 1, last_y))

        if self.direction == 2:
            self.body_list.append(SnakeBody(last_x, last_y - 1))

        if self.direction == 3:
            self.body_list.append(SnakeBody(last_x, last_y + 1))

    def move(self, direction: int = -1):
        snake_head = self.body_list[-1]
        x, y = snake_head.pos

        if direction == -1:
            direction = self.direction

        if direction == 0:
            self.direction = 0
            self.body_list.append(SnakeBody(x - 1, y))
            self.body_list.pop(0)

        if direction == 1:
            self.direction = 1
            self.body_list.append(SnakeBody(x + 1, y))
            self.body_list.pop(0)

        if direction == 2:
            self.direction = 2
            self.body_list.append(SnakeBody(x, y - 1))
            self.body_list.pop(0)

        if direction == 3:
            self.direction = 3
            self.body_list.append(SnakeBody(x, y + 1))
            self.body_list.pop(0)


if __name__ == "__main__":
    game = Game()
    game.start()

