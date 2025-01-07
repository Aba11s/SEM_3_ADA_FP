from dataclasses import dataclass, field
from typing import List, Tuple, Optional

# Rectangle class
@dataclass
class Rectangle:
    id: int
    width: int
    height: int
    x: Optional[int] = None
    y: Optional[int] = None

    def __str__(self):
        if self.x or self.y is not None:
            return f'Rect ID: {self.id} size: ({self.width}x{self.height}) at: ({self.x},{self.y}) '
        else:
            return f'Rect ID: {self.id} size: ({self.width}x{self.height})'

@dataclass
class Grid:
    width: int
    height: int
    config: Optional[List[List[int]]] = None

@dataclass
class PackingResult:
    config: List[List[int]] = None
    placed_rects: List[Rectangle] = field(default_factory=list)
    discarded_rects: List[Rectangle] = field(default_factory=list)
    grid_usage: float = 0.0

    def __str__(self):
        # String representation of the grid configuration
        config_str = '\n'.join(' '.join(str(cell) for cell in row) for row in self.config)

        # String represnetation of placed rectangles
        placed_str = '\n'.join(str(rect) for rect in self.placed_rects) if self.placed_rects else None

        # String representation of discarded rectangles
        discarded_str = '\n'.join(str(rect) for rect in self.discarded_rects) if self.discarded_rects else None

        # Final string
        return (
            f"\nGrid Configuration:\n{config_str}\n"
            f"\nPlaced Rectangles:\n{placed_str}\n"
            f"\nDiscarded Rectangles:\n{discarded_str}\n"
            f"\nGrid Usage: {self.grid_usage:.4f}\n"
        )
        