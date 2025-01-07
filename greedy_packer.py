# Heuristic - Greedy

#local packages
from objects import Rectangle, Grid, PackingResult
from utils import Analyzer, TestGenerator, Visualizer

# tools
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from functools import wraps
import numpy as np


# Packing problem solver
class GreedyPacker:
    '''
    Class that contains methods to solve the packing problem with greedy-heuristics
    '''
    def _check_fit(self, grid:Grid, config:List[List[int]], rect:Rectangle, x:int, y:int) -> bool:
        '''
        Checks if the given rectangle fits at the given position
        '''
        # Condition 1: checks if the rectangle overlaps the border of the grid (out of bounds)
        if x + rect.width > grid.width or y + rect.height > grid.height:
            return False
        
        # Condtion 2: checks if the rectangle doesn't overlap with another rectangle
        for i in range(rect.height):
            for j in range(rect.width):
                if config[y + i][x + j] > 0:
                    return False
        
        # Otherwise...
        return True

    def _place_rectangle(self, config:List[List[int]], rect:Rectangle, x:int, y:int) -> None:
        '''
        Places rectangle onto a given grid - inplace
        '''
        rect.x, rect.y = x, y
        for i in range(rect.height):
            for j in range(rect.width):
                config[y + i][x + j] = rect.id

    def _split_space(self, space:tuple[int, int, int, int], rect:Rectangle, x:int, y:int) -> List[tuple[int,int,int,int]]:
        '''
        Splits space if the given rectangle fits into the available space
        '''
        space_x, space_y, space_width, space_height = space
        new_spaces = []
        if x + rect.width < space_x + space_width:
            new_spaces.append((x + rect.width, y, space_x + space_width - (x + rect.width), rect.height))
        if y + rect.height < space_y + space_height:
            new_spaces.append((x, y + rect.height, rect.width, space_y + space_height - (y + rect.height)))
        if x + rect.width < space_x + space_width and y + rect.height < space_y + space_height:
            new_spaces.append((x + rect.width, y + rect.height, space_x + space_width - (x + rect.width), space_y + space_height - (y + rect.height)))
        return new_spaces

    def by_best_fit(self, grid:Grid, rectangles:List[Rectangle]) -> PackingResult:
        '''
        Attempts to find a solution by best-fit---placing the rectangle with the largest area first
        '''
        # Sorts rectangles
        sorted_rectangles = sorted(rectangles, key=lambda r: r.width * r.height, reverse=True)

        # sets the initial grid configuration
        grid.config = [[0 for _ in range(grid.width)] for _ in range(grid.height)]

        # assigns new PackingResult instance and its config
        result = PackingResult(config=grid.config)

        # intializes free spaces
        free_spaces = [(0, 0, grid.width, grid.height)]

        # AHAHAHAHAHAHAHAH\
        for i, rect in enumerate(sorted_rectangles):
            best_fit = None
            min_leftover_space = float('inf')

            for space in free_spaces:
                x, y, space_width, space_height = space

                #????????
                if rect.width <= space_width and rect.height <= space_height:
                    leftover_space = (space_width - rect.width) * (space_height - rect.height)

                    # HUH
                    if leftover_space < min_leftover_space:
                        min_leftover_space = leftover_space
                        best_fit = (x, y, space)

            if best_fit:
                x, y, chosen_space = best_fit

                # places rectangle
                self._place_rectangle(result.config, rect, x, y)
                result.placed_rects.append(rect)

                # splits the remaining space
                free_spaces.remove(chosen_space)
                free_spaces.extend(self._split_space(chosen_space, rect, x, y))
            else:
                # discards that rectangle
                result.discarded_rects.append(rect)


        # calculates total area used and the total grid area usage
        used_area = sum(1 for row in result.config for cell in row if cell > 0)
        result.grid_usage = used_area / (grid.width * grid.height)

        return result
    
    def by_worst_fit(self, grid:Grid, rectangles:List[Rectangle]) -> PackingResult:
        '''
        Attempts to find a solution by worst-fit---placing the rectangle with the smallest area first
        '''
        # Sorts rectangles
        sorted_rectangles = sorted(rectangles, key=lambda r: r.width * r.height, reverse=False)

        # sets the initial grid configuration
        grid.config = [[0 for _ in range(grid.width)] for _ in range(grid.height)]

        # assigns new PackingResult instance and its config
        result = PackingResult(config=grid.config)

        # intializes free spaces
        free_spaces = [(0, 0, grid.width, grid.height)]

        # AHAHAHAHAHAHAHAH\
        for i, rect in enumerate(sorted_rectangles):
            best_fit = None
            min_leftover_space = float('inf')

            for space in free_spaces:
                x, y, space_width, space_height = space

                #????????
                if rect.width <= space_width and rect.height <= space_height:
                    leftover_space = (space_width - rect.width) * (space_height - rect.height)

                    # HUH
                    if leftover_space < min_leftover_space:
                        min_leftover_space = leftover_space
                        best_fit = (x, y, space)

            if best_fit:
                x, y, chosen_space = best_fit

                # places rectangle
                self._place_rectangle(result.config, rect, x, y)
                result.placed_rects.append(rect)

                # splits the remaining space
                free_spaces.remove(chosen_space)
                free_spaces.extend(self._split_space(chosen_space, rect, x, y))
            else:
                # discards that rectangle
                result.discarded_rects.append(rect)

        # calculates total area used and the total grid area usage
        used_area = sum(1 for row in result.config for cell in row if cell > 0)
        result.grid_usage = used_area / (grid.width * grid.height)

        return result
 

    def by_first_fit(self, grid:Grid, rectangles:List[Rectangle]) -> PackingResult:
        '''
        Attempts to find a solution by first-fit---placing the rectangles that fits in the available grid, regardless of order
        '''
        # sets the initial grid configuration
        grid.config = [[0 for _ in range(grid.width)] for _ in range(grid.height)]

        # assigns new PackingResult instance and its config
        result = PackingResult(config=grid.config)

        empty_spaces = [(0,0)]

        for _, rect in enumerate(rectangles):
            #rect.id = i + 1
            placed = False

            # Tries to place rectangle in each empty space
            for _, (x, y) in enumerate(empty_spaces):
                if self._check_fit(grid, result.config, rect, x, y):
                    self._place_rectangle(result.config, rect, x, y)
                    result.placed_rects.append((rect, (x, y)))

                    # Add new empty spaces at right and bottom of placed rectangle
                    empty_spaces.append((x + rect.width, y))
                    empty_spaces.append((x, y + rect.height))

                    # Sort spaces by y then x for optimal placement
                    empty_spaces.sort(key=lambda pos: (pos[1], pos[0]))
                    placed = True
                    break
                
            if not placed:
                # discards that rectangle
                result.discarded_rects.append(rect)

        # calculates total area used and the total grid area usage
        used_area = sum(1 for row in result.config for cell in row if cell > 0)
        result.grid_usage = used_area / (grid.width * grid.height)

        return result


    @Analyzer.analyze_memory_and_time
    def solve(self, method, grid:Grid, rectangles:List[Rectangle]) -> PackingResult:
        '''
        wrapper method that serves as the entrypoint to the solver
        '''
        return method(grid, rectangles)
    

'''# TEST USAGE

# parameters
grid = Grid(10,10)
seed = 42
rectangles = TestGenerator.gen_test_case(5,10, (2,2), (6,6), seed)
packer = GreedyPacker()
method = packer.by_worst_fit

# solve
result:PackingResult; result, memory_usage, execution_time = packer.solve(method, grid, rectangles)

for row in result.config:
    print(" ".join(map(str, row)))

print(f"grid_usage: {result.grid_usage}")
Visualizer.visualize(result.config)
'''


    
