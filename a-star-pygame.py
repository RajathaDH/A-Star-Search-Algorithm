import pygame
from queue import PriorityQueue

SIZE = 600 # length of width and height
SQUARES = 30 # number of squares in each row and column

WIN = pygame.display.set_mode((SIZE, SIZE))
FPS = 60

pygame.display.set_caption("A* Search Algorithm Visualization")

colours = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (247, 239, 5),
    "grey": (80, 80, 74),
    "orange": (242, 140, 15),
    "purple": (220, 12, 180),
    "lightblue": (12, 144, 220)
}

def main():
    grid = new_grid()
    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        draw(grid)

    pygame.quit()

def new_grid():
    grid = []
    square_size = SIZE // SQUARES # length of each square
    
    for row in range(SQUARES):
        grid.append([])
        for col in range(SQUARES):
            node = Node(row, col, square_size)
            grid[row].append(node)

    return grid

def draw(grid):
    WIN.fill(colours["black"])

    # draw nodes
    for row in grid:
        for node in row:
            node.draw()

    # draw lines
    square_size = SIZE // SQUARES
    for row in range(SQUARES):
        pygame.draw.line(WIN, colours["grey"], (0, row * square_size), (SIZE, row * square_size)) # horizontal lines
    for col in range(SQUARES):
        pygame.draw.line(WIN, colours["grey"], (col * square_size, 0), (col * square_size, SIZE)) # vertical lines

    pygame.display.update()

class Node:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.x_pos = row * size
        self.y_pos = col * size
        self.colour = colours["white"]

    def draw(self):
        pygame.draw.rect(WIN, self.colour, (self.x_pos, self.y_pos, self.size, self.size))


if __name__ == '__main__':
    main()