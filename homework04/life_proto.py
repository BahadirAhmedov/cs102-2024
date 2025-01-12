import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        :param randomize: Если True, клетки будут случайно живыми или мертвыми.
        :return: Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = [
            [random.randint(0, 1) if randomize else 0 for _ in range(self.cell_width)] for _ in range(self.cell_height)
        ]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Возвращает список состояний соседей клетки.

        :param cell: Клетка для которой нужно найти соседей.
        :return: Список состояний соседних клеток.
        """
        row, col = cell
        neighbours = [
            (row + i, col + j)
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            if not (i == 0 and j == 0) and 0 <= row + i < self.cell_height and 0 <= col + j < self.cell_width
        ]
        return [self.prev_generation[r][c] for r, c in neighbours]

    def get_next_generation(self) -> Grid:
        """
        Генерирует следующее поколение клеток.

        :return: Новый список клеток.
        """
        next_generation = []
        for row in range(self.cell_height):
            next_row = []
            for col in range(self.cell_width):
                state = self.curr_generation[row][col]
                neighbours = self.get_neighbours((row, col))
                live_neighbours = sum(neighbours)

                if state == 1 and live_neighbours in [2, 3]:
                    next_row.append(1)  # Оживает или остаётся живой
                elif state == 0 and live_neighbours == 3:
                    next_row.append(1)  # Клетка возрождается
                else:
                    next_row.append(0)  # Клетка умирает
            next_generation.append(next_row)
        return next_generation

    def step(self) -> None:
        """Выполняет один шаг игры (обновление клеток)."""
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
