import pygame

SIZE = 600

WIN = pygame.display.set_mode((SIZE, SIZE))
FPS = 60

pygame.display.set_caption("A* Search Algorithm Visualization")

def main():
    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == '__main__':
    main()