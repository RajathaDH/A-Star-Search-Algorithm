import pygame
from queue import PriorityQueue

SIZE = 600 # length of width and height
SQUARES = 30 # number of squares in each row and column

SQUARE_SIZE = SIZE // SQUARES # length of each square

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

            # check if left mouse button is pressed
            if pygame.mouse.get_pressed()[0]:
                clicked_position = pygame.mouse.get_pos()
                row, col = get_clicked_node_position(clicked_position)
                node = grid[row][col]
                node.colour = colours["red"]
        
        draw(grid)

    pygame.quit()

def new_grid():
    grid = []
    
    for row in range(SQUARES):
        grid.append([])
        for col in range(SQUARES):
            node = Node(row, col, SQUARE_SIZE)
            grid[row].append(node)

    return grid

def draw(grid):
    WIN.fill(colours["black"])

    # draw nodes
    for row in grid:
        for node in row:
            node.draw()

    # draw lines
    for row in range(SQUARES):
        pygame.draw.line(WIN, colours["grey"], (0, row * SQUARE_SIZE), (SIZE, row * SQUARE_SIZE)) # horizontal lines
    for col in range(SQUARES):
        pygame.draw.line(WIN, colours["grey"], (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, SIZE)) # vertical lines

    pygame.display.update()

def get_clicked_node_position(position):
    x, y = position

    row = x // SQUARE_SIZE
    col = y // SQUARE_SIZE

    return row, col

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

    def get_position(self):
        return self.row, self.col


if __name__ == '__main__':
    main()