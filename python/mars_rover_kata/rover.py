#!/usr/bin/env python


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Grid:
    def __init__(self, x=50, y=50, obstacles=None):
        self.x = x
        self.y = y
        self.obstacles = obstacles if obstacles else []


class Rover:
    def __init__(self, position=Position(), aspect="N"):
        self.position = position
        self.aspect = aspect
        self.commands = None
        self.grid = None
        self.f = self.move_forward
        self.b = self.move_backward
        self.l = self.turn_left
        self.r = self.turn_right

    def load_grid(self, grid):
        self.grid = grid

    def get_position(self):
        return (self.position.x, self.position.y)

    def receive_commands(self, commands):
        self.commands = commands if isinstance(commands, list) else list(commands)

    def detect_obstacles(self, next_move):
        next_x = self.position.x + next_move[0]
        next_y = self.position.y + next_move[1]
        if [next_x, next_y] in self.grid.obstacles:
            raise Exception(f"obstacle {[next_x, next_y]} detected")

    def guess_next_move(self, direction):
        forward_aspect_mapping = {
            "N": [0, 1],
            "S": [0, -1],
            "W": [-1, 0],
            "E": [1, 0]
        }
        return {
            "f": forward_aspect_mapping[self.aspect],
            "b": [-i for i in forward_aspect_mapping[self.aspect]],
        }[direction]

    def get_next_aspect(self, direction):
        turn_aspect_mapping = {
            "N": ["W", "E"],
            "S": ["E", "W"],
            "W": ["S", "N"],
            "E": ["N", "S"],
        }
        return {
            "l": turn_aspect_mapping[self.aspect][0],
            "r": turn_aspect_mapping[self.aspect][1],
        }[direction]

    def move_forward(self):
        # self.position.x, self.position.y += self.guess_next_move("f")
        next_move = self.guess_next_move("f")
        self.detect_obstacles(next_move)
        self.position.x += next_move[0]
        self.position.y += next_move[1]

    def move_backward(self):
        next_move = self.guess_next_move("b")
        self.detect_obstacles(next_move)
        self.position.x += next_move[0]
        self.position.y += next_move[1]

    def turn_left(self):
        self.aspect = self.get_next_aspect("l")

    def turn_right(self):
        self.aspect = self.get_next_aspect("r")

    def rove(self):
        for command in self.commands:
            method_name = getattr(self, command)
            if callable(method_name):
                method_name()
