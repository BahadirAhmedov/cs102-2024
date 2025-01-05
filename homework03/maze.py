from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd  # type: ignore


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■" for _ in range(cols)] for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    r, c = coord
    max_r = len(grid) - 1
    max_c = len(grid[0]) - 1

    directions = ["go_up", "go_right"]
    pick = choice(directions)

    if pick == "go_up" and 0 <= r - 2 <= max_r and 0 <= c <= max_c:
        grid[r - 1][c] = " "
    else:
        pick = "go_right"

    if pick == "go_right" and 0 <= r <= max_r and 0 <= c + 2 <= max_c:
        grid[r][c + 1] = " "
    elif pick == "go_right" and 0 <= r - 2 <= max_r and 0 <= c <= max_c:
        grid[r - 1][c] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """
    lab = create_grid(rows, cols)

    possible_cells = []
    for r_idx, row_data in enumerate(lab):
        for c_idx, _ in enumerate(row_data):
            if r_idx % 2 == 1 and c_idx % 2 == 1:
                lab[r_idx][c_idx] = " "
                possible_cells.append((r_idx, c_idx))

    while possible_cells:
        cur_cell = possible_cells.pop(0)
        lab = remove_wall(lab, cur_cell)

    if random_exit:
        entry_r = randint(0, rows - 1)
        exit_r = randint(0, rows - 1)
        if entry_r in (0, rows - 1):
            entry_c = randint(0, cols - 1)
        else:
            entry_c = choice((0, cols - 1))
        if exit_r in (0, rows - 1):
            exit_c = randint(0, cols - 1)
        else:
            exit_c = choice((0, cols - 1))
    else:
        entry_r, entry_c = 0, cols - 2
        exit_r, exit_c = rows - 1, 1

    lab[entry_r][entry_c] = "X"
    lab[exit_r][exit_c] = "X"

    return lab


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    res = []
    for r_idx, row in enumerate(grid):
        for c_idx, val in enumerate(row):
            if val == "X":
                res.append((r_idx, c_idx))
    return res


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    rows = len(grid)
    cols = len(grid[0])

    for row_idx in range(rows):
        for col_idx in range(cols):
            if grid[row_idx][col_idx] == k:
                for dr, dc in directions:
                    nr, nc = row_idx + dr, col_idx + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                        grid[nr][nc] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    ex_r, ex_c = exit_coord
    step_counter = 0

    while grid[ex_r][ex_c] == 0:
        step_counter += 1
        grid = make_step(grid, step_counter)

    route = [(ex_r, ex_c)]
    k_val = int(grid[ex_r][ex_c])
    cur_r, cur_c = ex_r, ex_c

    while grid[cur_r][cur_c] != 1 and k_val > 0:
        if (cur_r + 1 < len(grid)) and (grid[cur_r + 1][cur_c] == k_val - 1):
            cur_r += 1
        elif (cur_r - 1 >= 0) and (grid[cur_r - 1][cur_c] == k_val - 1):
            cur_r -= 1
        elif (cur_c + 1 < len(grid[0])) and (grid[cur_r][cur_c + 1] == k_val - 1):
            cur_c += 1
        elif (cur_c - 1 >= 0) and (grid[cur_r][cur_c - 1] == k_val - 1):
            cur_c -= 1
        else:
            break
        route.append((cur_r, cur_c))
        k_val -= 1

    if len(route) != grid[ex_r][ex_c]:
        grid[route[-1][0]][route[-1][1]] = " "
        route.pop()
        if route:
            r_next, c_next = route[-1]
            shortest_path(grid, (r_next, c_next))

    return route


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    r_count = len(grid)
    c_count = len(grid[0])
    r, c = coord

    if (
        (r == 0 and c == 0)
        or (r == 0 and c == c_count - 1)
        or (r == r_count - 1 and c == 0)
        or (r == r_count - 1 and c == c_count - 1)
    ):
        return True

    if r == 0 and grid[r + 1][c] == "■":
        return True
    if r == r_count - 1 and grid[r - 1][c] == "■":
        return True
    if c == 0 and grid[r][c + 1] == "■":
        return True
    if c == c_count - 1 and grid[r][c - 1] == "■":
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    exits_found = get_exits(grid)
    if len(exits_found) > 1:
        if encircled_exit(grid, exits_found[0]) or encircled_exit(grid, exits_found[1]):
            return grid, None

        working_copy = deepcopy(grid)
        r_start, c_start = exits_found[0]
        grid[r_start][c_start] = 1

        for rr in range(len(working_copy)):
            for cc in range(len(working_copy[0])):
                if grid[rr][cc] in (" ", "X"):
                    grid[rr][cc] = 0

        path_result = shortest_path(grid, exits_found[1])
        return working_copy, path_result
    else:
        return grid, exits_found


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    df_maze = bin_tree_maze(15, 15)
    print(pd.DataFrame(df_maze))

    new_maze = bin_tree_maze(15, 15)
    solved_grid, route = solve_maze(new_maze)
    final_map = add_path_to_grid(solved_grid, route)
    print(pd.DataFrame(final_map))
