# Brute force approach

#local packages
from objects import Rectangle, Grid, PackingResult
from utils import Analyzer, TestGenerator, Visualizer

# tools
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Callable
from functools import wraps
import numpy as np


# Packing Problem Class
class BruteForcePacker:
    def __init__(self):
        self.rects:List[Rectangle] = []
        self.grid = []
        self.grid_width = 0
        self.grid_height = 0
        self.memo = {} # for memoization

    def _place_rectangle(self, rect:Rectangle, x:int, y:int) -> None:
        '''
        places rectangle at postion x,y
        '''
        rect.x, rect.y = x, y
        for i in range(rect.height):
            for j in range(rect.width):
                self.grid[y + i][x + j] = rect.id

    def _remove_rectangle(self, rect:Rectangle) -> None:
        '''
        removes rectangle for backtracking purposes
        '''
        for i in range(rect.height):
            for j in range(rect.width):
                self.grid[rect.y + i][rect. x + j] = 0

    def _check_fit(self, rect:Rectangle, x:int, y:int) -> bool:
        '''
        checks if a rectangle can be placed at a given position x,y - returns True if its possible, else False
        '''
        # Case 1 - rectangle doesnt fit in grid
        if x + rect.width > self.grid_width or y + rect. height > self.grid_height:
            return False
        
        # Case 2 - rectangle overlapping with another rectangle
        for i in range(rect.height):
            for j in range(rect.width):
                if self.grid[y + i][x + j] > 0:
                    return False
        
        # Otherwise
        return True
    
    def _get_occupied_area(self) -> int:
        '''
        calcs total area occupied by the placed rectangles - returns area:int
        '''
        # bazinga
        return sum(1 for row in self.grid for cell in row if cell > 0)
    
    def _get_placed_and_discarded_rectangles(self, config:List[List[int]], rects:List[Rectangle]) -> Tuple[List[Rectangle], List[Rectangle]]:
        '''
        gets placed rectangles based on present IDs on the configuration - returns list of placed rectangles
        '''
        # gets a list of present ids
        unique_ids = list(set(value for row in config for value in row))

        # adds rectangle to return variable if rect.id == unique_id
        placed_rectangles = []
        discarded_rectangles = []

        for rect in rects:
            if rect.id in unique_ids:
                placed_rectangles.append(rect)
            else:
                discarded_rectangles.append(rect)

        return placed_rectangles, discarded_rectangles
    
    def _serialize_grid(self,  config:List[List[int]]) -> str:
        '''
        serializes the configuration into string
        '''
        return '\n'.join(''.join(str(cell) for cell in row) for row in config)
    
    def _update_rect_pos(self, best_config: List[List[int]]) -> None:
        '''
        Updates the positions of rectangles based on the best configuration.
        '''
        # Reset positions first
        for rect in self.rects:
            rect.x, rect.y = None, None
        
        # Set positions based on the best configuration
        checked = []
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                rect_id = best_config[y][x]
                if rect_id > 0:  # If there's a rectangle placed
                    for rect in self.rects:
                        if rect.id == rect_id and rect_id not in checked:
                            rect.x, rect.y = x, y  # Set the position based on the best config
                            checked.append(rect_id)
    
    def by_brute_force(self, index:int=0) -> tuple[int, List[List[int]]]:
        '''
        packing solution with basic recursive brute-force approach - returns a tuple (best_area:int, best_config:list[list[int]])
        '''
        # Base case: all rectangles have been considered
        if index >= len(self.rects):
            return self._get_occupied_area(), [row[:] for row in self.grid]
            
        # Recursive case 
        best_area = 0
        best_config = [row[:] for row in self.grid] # creates shallow copy of outer list & deep copy of inner

        # Case 1: skips current rectangle
        area, config = self.by_brute_force(index + 1)
        if area > best_area:
            best_area = area
            best_config = config

        # Case 2: tries to place current rectangle
        rect = self.rects[index]

        for y in range(self.grid_height - rect.height + 1): # tries every position
            for x in range(self.grid_width - rect.width + 1):
                if self._check_fit(rect, x, y):
                    self._place_rectangle(rect, x, y)
                    area, config = self.by_brute_force(index + 1)

                    if area > best_area:
                        best_area = area
                        best_config = config

                    self._remove_rectangle(rect)

        return best_area, best_config
    
    # AHAHAHAHAHAHHAHAHAHAHAHAHAHAHAH
    def by_memoization(self, index:int=0) -> Tuple[int, List[List[int]]]:
        '''
        brute-force packing solution implementing memoization technique
        '''
        # Create a unique state key based on the current index and grid state
        state_key = (index, self._serialize_grid(self.grid))

        # Check if the result is already cached
        if state_key in self.memo:
            print("CACHE FOUND")
            return self.memo[state_key]

        # Base case: all rectangles have been considered
        if index >= len(self.rects):
            curr_area = self._get_occupied_area()
            self.memo[state_key] = (curr_area, [row[:] for row in self.grid])
            return self.memo[state_key]

        # Recursive case
        rect = self.rects[index]
        best_area = 0
        best_config = [row[:] for row in self.grid]

        # Case 1: Skip the current rectangle
        area, config = self.by_memoization(index + 1)
        if area > best_area:
            best_area = area
            best_config = config

        # Case 2: Attempt to place the current rectangle
        for y in range(self.grid_height - rect.height + 1):
            for x in range(self.grid_width - rect.width + 1):
                if self._check_fit(rect, x, y):
                    self._place_rectangle(rect, x, y)
                    area, config = self.by_memoization(index + 1)

                    if area > best_area:
                        best_area = area
                        best_config = config

                    self._remove_rectangle(rect)

        # Store the best result in the memoization dictionary
        self.memo[state_key] = (best_area, best_config)
        return self.memo[state_key]
    
    # INCOMPLETE - DO NOT USE - SAFETY HAZARD
    def by_iter(self) -> Tuple[int, List[List[int]]]:
        max_area = 0
        best_config = []

        # Try to place each rectangle in every position of the grid
        for rect in self.rects:
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if self.check_fit(rect, x, y):
                        self.place_rectangle(rect, x, y)
                        # Calculate the current occupied area
                        current_area = sum(row.count(rect.id) for row in self.grid)
                        if current_area > max_area:
                            max_area = current_area
                            best_config = [row[:] for row in self.grid]  # Store the best configuration
                        self.remove_rectangle(rect)  # Backtrack

        return max_area, best_config

    @Analyzer.analyze_memory_and_time
    def solve(self, method:Callable[[],Tuple[int, List[List[int]]]], grid:Grid, rects:List[Rectangle]) -> PackingResult:
        '''
        wrapper function as the solution entrypoint - ensure grid and rectangles are properly set-up -
        returns PackingResult
        '''
        result = PackingResult()

        # initiates grid & rects instance variables
        grid.config = [[0 for _ in range(grid.width)] for _ in range(grid.height)]
        self.grid = [row[:] for row in grid.config]
        self.grid_height, self.grid_width = grid.height, grid.width
        self.rects = rects

        # solver
        best_area, best_config = method()

        # setting the packing result
        self._update_rect_pos(best_config)
        result.config = best_config
        result.placed_rects, result.discarded_rects = self._get_placed_and_discarded_rectangles(result.config, rects)
        result.grid_usage = best_area / (grid.width * grid.height)

        return result
    

# TEST USAGE 

'''# parameters
seed = 1 # randomizer seed
grid = Grid(6, 6)
rectangles = TestGenerator.gen_test_case(4,8, (2,2), (4,4), seed)
packer = BruteForcePacker()
method = packer.by_brute_force

# solve

result:PackingResult;result, memory_usage, execution_time = packer.solve(method, grid, rectangles)

for row in result.config:
    print(" ".join(map(str, row)))

print(f"\nplaced rectangles:")
for placed in result.placed_rects:
    print(f"Rect [{placed.id}] at ({placed.x},{placed.y})")

print(f"\ndiscarded rectangles:")
for discarded in result.discarded_rects:
    print(f"Rect [{discarded.id}]")

print(f"grid_usage: {result.grid_usage}")
Visualizer.visualize(result.config)
'''



    



    


