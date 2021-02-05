import pygame
from queue import PriorityQueue
#import time

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
    "yellow": (255, 255, 0),
    "line": (51, 51, 51),
    "visited": (242, 158, 6),
    "path": (220, 12, 180)
}

def main():
    grid = new_grid()
    start_node = None
    end_node = None

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
                
                if not start_node:
                    start_node = node
                    node.make_node_start()
                elif not end_node:
                    end_node = node
                    node.make_node_end()
                elif node != start_node and node != end_node:
                    node.make_node_barrier()
            
            # check if right mouse button is pressed
            elif pygame.mouse.get_pressed()[2]:
                clicked_position = pygame.mouse.get_pos()
                row, col = get_clicked_node_position(clicked_position)
                node = grid[row][col]
                node.reset()
                if node == start_node:
                    start_node = None
                elif node == end_node:
                    end_node = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    a_star_search(lambda: draw(grid), grid, start_node, end_node)
                elif event.key == pygame.K_BACKSPACE:
                    grid = new_grid()
                    start_node = None
                    end_node = None
        
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
    WIN.fill(colours["white"])

    # draw nodes
    for row in grid:
        for node in row:
            node.draw()

    # draw lines
    for row in range(SQUARES):
        pygame.draw.line(WIN, colours["line"], (0, row * SQUARE_SIZE), (SIZE, row * SQUARE_SIZE)) # horizontal lines
    for col in range(SQUARES):
        pygame.draw.line(WIN, colours["line"], (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, SIZE)) # vertical lines

    pygame.display.update()

def get_clicked_node_position(position):
    y, x = position

    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE

    return row, col

def heuristic(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return abs(x2 - x1) + abs(y2 - y1)

def a_star_search(draw, grid, start_node, end_node):
    count = 0

    open_set = PriorityQueue()
    open_set.put((0, count, start_node))

    came_from = {}

    g_scores = { node: float("inf") for row in grid for node in row }
    g_scores[start_node] = 0
    f_scores = { node: float("inf") for row in grid for node in row }
    f_scores[start_node] = heuristic(start_node.get_position(), end_node.get_position())

    open_set_hash = { start_node }

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = open_set.get()[2]
        open_set_hash.remove(current_node)

        if current_node == end_node:
            construct_path(came_from, end_node, draw)
            end_node.make_node_end()
            return True

        for neighbour in current_node.neighbours:
            temp_g_score = g_scores[current_node] + 1

            if temp_g_score < g_scores[neighbour]:
                came_from[neighbour] = current_node
                g_scores[neighbour] = temp_g_score
                f_scores[neighbour] = temp_g_score + heuristic(neighbour.get_position(), end_node.get_position())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_scores[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_node_open()

        draw()

        if current_node != start_node:
            current_node.make_node_visited()

        #time.sleep(0.1)

    return False

def construct_path(came_from, current_node, draw):
    while current_node in came_from:
        current_node = came_from[current_node]
        current_node.make_node_path()
        draw()

class Node:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.x_pos = row * size
        self.y_pos = col * size
        self.colour = colours["white"]
        self.neighbours = []

    def draw(self):
        pygame.draw.rect(WIN, self.colour, (self.x_pos, self.y_pos, self.size, self.size))

    def get_position(self):
        return self.row, self.col

    def reset(self):
        self.colour = colours["white"]

    def make_node_start(self):
        self.colour = colours["green"]

    def make_node_end(self):
        self.colour = colours["red"]

    def make_node_barrier(self):
        self.colour = colours["black"]

    def make_node_open(self):
        self.colour = colours["yellow"]

    def make_node_visited(self):
        self.colour = colours["visited"]

    def make_node_path(self):
        self.colour = colours["path"]

    def is_node_barrier(self):
        return self.colour == colours["black"]

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < SQUARES - 1 and not grid[self.row + 1][self.col].is_node_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_node_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])
        if self.col < SQUARES - 1 and not grid[self.row][self.col + 1].is_node_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_node_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])

if __name__ == '__main__':
    main()