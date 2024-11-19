import numpy as np

# TEST
class Rectangle():
    def __init__(self, width:int, height:int, id:int) -> None:
        self.width = width
        self.height = height
        self.id = id
        
# Grid class
class PackingProblem():
    rects = []

    def create_grid(self, width: int, height: int) -> None:
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.grid_width, self.grid_height = width, height
        print(len(self.grid))
    
    def generate_rectangle(self, width:int, height:int, id:int) -> None:
        self.rects.append(Rectangle(width,height,id))

    def add_rectangle(self, rect:Rectangle, x:int, y:int) -> None:
        for i in range(rect.height):
            for j in range(rect.width):
                self.grid[y+i][x+j] = rect.id

    def remove_rectangle(self, rect:Rectangle, x:int, y:int) -> None:
        for i in range(rect.height):
            for j in range(rect.width):
                self.grid[y+i][x+j] = 0

    def check_fit(self, rect:Rectangle, x:int, y:int) -> bool:
        if x + rect.width > self.grid_width or y + rect.height > self.grid_height:
            return False

        for i in range(rect.height):
            for j in range(rect.width):
                if self.grid[y+i][x+j] > 0:
                    return False # overlap occurs

        return True

    def calculate_area(self):
        return sum(row.count(0) == 0 for row in self.grid)

    # Packing
    def pack_brute_force(self, index=0, best_area=0, best_config=None) -> bool:
        if best_config is None:
            best_config = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        if index == len(self.rects):
            curr_area = self.calculate_area()
            # checks if current arrangement is best
            if curr_area > best_area:
                best_area = curr_area
                best_config = [row[:] for row in self.grid]

            return best_area, best_config

        rect = self.rects[index]
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.check_fit(rect, x, y):
                    self.add_rectangle(rect, x, y)
                    best_area, best_config = self.pack_brute_force(index+1, best_area, best_config)
                    self.remove_rectangle(rect, x, y)
            
        return best_area, best_config 



    def show_grid(self) -> None:
        for row in self.grid:
            print(row)

    def show_positions(self) -> None:
        ...

        
# run
p = PackingProblem()
p.create_grid(10,10)

# test 
p.generate_rectangle(2,4,1)
p.generate_rectangle(6,3,2)
p.generate_rectangle(3,2,3)
p.generate_rectangle(4,4,4)
p.generate_rectangle(3,6,5)
p.generate_rectangle(4,6,6)

p.show_grid()
best_area, best_config = p.pack_brute_force()

print("\nbest config:")
for row in best_config:
    print(row)

