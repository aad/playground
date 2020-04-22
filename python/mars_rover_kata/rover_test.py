import unittest
import pytest
from rover import Position, Grid, Rover


class TestPosition(unittest.TestCase):
    def test_init_with_default(self):
        position = Position()
        self.assertEqual(position.x, 0)
        self.assertEqual(position.y, 0)

    def test_init_with_positive(self):
        position = Position(1, 2)
        self.assertEqual(position.x, 1)
        self.assertEqual(position.y, 2)


class TestGrid(unittest.TestCase):
    def test_init_with_default(self):
        grid = Grid()
        self.assertEqual(grid.x, 50)
        self.assertEqual(grid.y, 50)
        self.assertEqual(grid.obstacles, [])

    def test_init_with_positive(self):
        grid = Grid(10, 20, [[1, 2], [2, 3], [3, 4]])
        self.assertEqual(grid.x, 10)
        self.assertEqual(grid.y, 20)
        self.assertEqual(grid.obstacles, [[1, 2], [2, 3], [3, 4]])


class TestRover(unittest.TestCase):
    def test_init_with_default(self):
        rover = Rover()
        self.assertEqual(rover.position.x, 0)
        self.assertEqual(rover.position.y, 0)
        self.assertEqual(rover.aspect, "N")

    def test_init_with_position_and_aspect(self):
        position = Position(1, 2)
        rover = Rover(position, "W")
        self.assertEqual(rover.position.x, 1)
        self.assertEqual(rover.position.y, 2)
        self.assertEqual(rover.aspect, "W")

    def test_get_position(self):
        position = Position(1, 2)
        rover = Rover(position, "W")
        self.assertEqual(rover.get_position(), (1, 2))

    def test_can_receive_commands(self):
        rover = Rover()
        rover.receive_commands("ffll")
        self.assertEqual(rover.commands, ["f", "f", "l", "l"])
        rover.receive_commands(["f", "f", "l"])
        self.assertEqual(rover.commands, ["f", "f", "l"])

    def test_guess_next_move(self):
        position = Position(2, 3)
        rover = Rover(position)
        self.assertEqual(rover.guess_next_move("f"), [0, 1])
        self.assertEqual(rover.guess_next_move("b"), [0, -1])
        position = Position(2, 3)
        rover = Rover(position, "E")
        self.assertEqual(rover.guess_next_move("f"), [1, 0])
        self.assertEqual(rover.guess_next_move("b"), [-1, 0])

    def test_can_load_grid(self):
        rover = Rover()
        grid = Grid()
        rover.load_grid(grid)
        self.assertEqual(rover.grid.x, 50)
        self.assertEqual(rover.grid.y, 50)
        self.assertEqual(rover.grid.obstacles, [])
        rover = Rover()
        grid = Grid(10, 20, [[1, 2], [2, 3], [3, 4]])
        rover.load_grid(grid)
        self.assertEqual(rover.grid.x, 10)
        self.assertEqual(rover.grid.y, 20)
        self.assertEqual(rover.grid.obstacles, [[1, 2], [2, 3], [3, 4]])

    def test_detect_obstacles(self):
        position = Position(1, 1)
        rover = Rover(position, "N")
        grid = Grid(obstacles=[[1, 2]])
        rover.load_grid(grid)
        rover.detect_obstacles([1, 0])
        with pytest.raises(Exception) as e:
            rover.detect_obstacles([0, 1])
        assert str(e.value) == "obstacle [1, 2] detected"

    def test_can_move(self):
        position = Position(3, 4)
        grid = Grid()
        rover = Rover(position)
        rover.load_grid(grid)
        rover.f()
        self.assertEqual(rover.get_position(), (3, 5))
        rover.b()
        self.assertEqual(rover.get_position(), (3, 4))
        rover = Rover(position, "W")
        rover.load_grid(grid)
        rover.b()
        self.assertEqual(rover.get_position(), (4, 4))
        rover.b()
        self.assertEqual(rover.get_position(), (5, 4))

    def test_can_turn(self):
        rover = Rover(aspect="N")
        self.assertEqual(rover.get_next_aspect("r"), "E")
        self.assertEqual(rover.get_next_aspect("l"), "W")
        rover.r()
        self.assertEqual(rover.aspect, "E")
        rover = Rover(aspect="W")
        rover.l()
        self.assertEqual(rover.aspect, "S")

    def test_rove(self):
        grid = Grid()
        rover = Rover()
        rover.load_grid(grid)
        rover.receive_commands("ffrff")
        rover.rove()
        self.assertEqual(rover.get_position(), (2, 2))
        self.assertEqual(rover.aspect, "E")

    def test_rove_with_obstacles(self):
        position = Position(10, 6)
        grid = Grid()
        rover = Rover(position, "E")
        rover.load_grid(grid)
        rover.receive_commands("fffblffrbrf")
        rover.rove()
        self.assertEqual(rover.get_position(), (11, 7))
        self.assertEqual(rover.aspect, "S")
        position = Position(10, 6)
        grid = Grid(obstacles=[[11, 7]])
        rover = Rover(position, "E")
        rover.load_grid(grid)
        rover.receive_commands("fffblffrbrf")
        with self.assertRaises(Exception) as e:
            rover.rove()
        self.assertEqual(str(e.exception), "obstacle [11, 7] detected")
        self.assertEqual(rover.get_position(), (11, 8))


if __name__ == "__main__":
    unittest.main()
