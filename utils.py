from objects import Rectangle

import random
import time
import sys
import memory_profiler
import tracemalloc

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from functools import wraps
import matplotlib.pyplot as plt
import numpy as np


class Analyzer():
    '''
    Contains decorator methods to analyze runtime, memory usage, etc
    '''

    @staticmethod
    def analyze_runtime(func):
        '''
        runtime calc decorator - returns runtime in seconds
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            return result, elapsed_time # Return the result of the original function
        return wrapper
    
    @staticmethod
    def analyze_memory(func) -> float:
        '''
        memory usage calc decorator - returns memory in Kib
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Measure memory usage while executing the function
            mem_usage = memory_profiler.memory_usage((func, args, kwargs), max_usage=True)
            max_memory_kib = mem_usage * 1024  # Convert from MiB to KiB
            return func(*args, **kwargs), max_memory_kib  # Return the result of the original function
        return wrapper
    
    @staticmethod
    def analyze_memory_and_time(func):
        '''
        returns both memory profile and execution time. both mrmory tracing and time calculations have minimal overheads.
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            start_time = time.time()

            # executing the function and takes snapshots
            result = func(*args, **kwargs)

            # snapshotting memory usage
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno') 

            # gets execution time
            elapsed_time = time.time() - start_time
            tracemalloc.stop()

            max_memory_kib = max(stat.size for stat in top_stats) / 1024 # converting B to KiB

            return result, max_memory_kib, elapsed_time
        return wrapper


    
class TestGenerator():
    @staticmethod
    def gen_test_cases(n:int, min_rectangles:int, max_rectangles:int, min_dimensions:tuple[int, int], max_dimensions:tuple[int,int], seed:int = None) -> List[List['Rectangle']]: # type: ignore
        '''
        Generate list of list of rects to test - uses min & max dimensions & rectangles as constraints
        '''
        if seed is not None:
            random.seed(seed)
        test_cases = []

        # creates n number of tests
        for _ in range(n):
            
            # creates a random number of rect for each test case
            num_of_rects = random.randint(min_rectangles, max_rectangles)
            idx = 1 # indexing rects
            rects = []

            for _ in range(num_of_rects):
                width = random.randint(min_dimensions[0], max_dimensions[0])
                height = random.randint(min_dimensions[1], max_dimensions[1])
                rects.append(Rectangle(id = idx, width = width, height = height)) 
                idx += 1

            test_cases.append(rects) # adds test case
        
        return test_cases
    
    @staticmethod
    def gen_test_case(min_rectangles:int, max_rectangles:int, min_dimensions:tuple[int, int], max_dimensions:tuple[int,int], seed:int = None) -> List['Rectangle']: # type: ignore
        '''
        generate list of rectangles
        '''
        if seed is not None:
            random.seed(seed)

        # creates a random number of rect for each test case
        num_of_rects = random.randint(min_rectangles, max_rectangles)
        idx = 1 # indexing rects
        test_case = []

        for r in range(num_of_rects):
            width = random.randint(min_dimensions[0], max_dimensions[0])
            height = random.randint(min_dimensions[1], max_dimensions[1])
            test_case.append(Rectangle(id = idx, width = width, height = height)) 
            idx += 1

        return test_case


    
class Visualizer():
    @staticmethod
    def visualize(grid:List[List[int]]):
        '''
        Visualizes the grid using pyplot
        '''
        # converts 2d list into 2d numpy array
        grid = np.array(grid)

        plt.figure(figsize=(8,8))

        # Create a color map for each rect id
        l = len(np.unique(grid))
        cmap = plt.cm.get_cmap('brg', l)

        # Create a new colormap that starts with white
        if l > 1:
            cmap = cmap(np.arange(cmap.N))
            cmap[0] = [1, 1, 1, 1]  # Set the first color (for ID 0) to white
            cmap = plt.cm.colors.ListedColormap(cmap)

        # Display grid and adjusting for offset
        plt.imshow(grid, cmap=cmap, interpolation="nearest", origin='upper', extent=[0, grid.shape[1], grid.shape[0], 0])

        # Display the grid
        plt.title('Rectangle Packing Visualization')
        plt.xlabel('Width')
        plt.ylabel('Height')
        
        plt.show()

    