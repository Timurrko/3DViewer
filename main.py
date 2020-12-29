import pygame
from math import sin, cos, pi

fps = 50  # количество кадров в секунду
clock = pygame.time.Clock()
running = True
vectors = [[1, 0, 0], [0, 1, 0], [0, 0, -1]]
pressed = False
scale = 64
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 400))
    pygame.display.set_caption('3d')
    while running:
        screen.fill((0, 0, 0))
        vectors1 = []
        a1 = 0
        a2 = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        what_we_see = list(pygame.key.get_pressed())
        if what_we_see[26]:
            a1 += pi / 256
        if what_we_see[22]:
            a1 += - pi / 256
        if what_we_see[4]:
            a2 += pi / 256
        if what_we_see[7]:
            a2 += - pi / 256
        if what_we_see[45]:
            scale /= 1.0625
        if what_we_see[46]:
            scale *= 1.0625
        for v in vectors:
            v = v[0] * cos(a2) - v[1] * sin(a2), v[1] * cos(a2) + v[0] * sin(a2), v[2]
            v = v[0], v[1] * cos(a1) + v[2] * sin(a1), v[2] * cos(a1) - v[1] * sin(a1)
            vectors1.append(v)
        vectors = vectors1
        for i in range(3):
            pygame.draw.line(screen, [(255, 0, 0), (0, 255, 0), (0, 0, 255)][i], (250, 200),
                             (250 + vectors[i][0] * scale, 200 + vectors[i][2] * scale), 1)

        pygame.display.flip()
        clock.tick(fps)
