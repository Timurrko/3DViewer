import pygame
from math import sin, cos, pi

fps = 50  # количество кадров в секунду
clock = pygame.time.Clock()
running = True
vectors = [[1, 0, 0], [0, 1, 0], [0, 0, -1]]
pressed = False
scale = 64
lines = []
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
        #print(what_we_see.index(True) if True in what_we_see else 'NF')
        if what_we_see[20]:
            line = []
            for i in range(2):
                try:
                    point = list(map(float, input().split()))
                    if len(point) != 3:
                        raise TypeError
                except TypeError:
                    point = [0, 0, 0]
                line += point
            lines.append(line)
        for line in lines:
            s_x, s_y, s_z, e_x, e_y, e_z = line
            s_x, s_y, s_z = vectors[0][0] * s_x + vectors[1][0] * s_y + vectors[2][0] * s_z, \
                            vectors[0][1] * s_x + vectors[1][1] * s_y + vectors[2][1] * s_z, \
                            vectors[0][2] * s_x + vectors[1][2] * s_y + vectors[2][2] * s_z
            e_x, e_y, e_z = vectors[0][0] * e_x + vectors[1][0] * e_y + vectors[2][0] * e_z, \
                            vectors[0][1] * e_x + vectors[1][1] * e_y + vectors[2][1] * e_z, \
                            vectors[0][2] * e_x + vectors[1][2] * e_y + vectors[2][2] * e_z
            pygame.draw.line(screen, (255, 255, 255), (250 + s_x * scale, 200 + s_z * scale),
                             (250 + e_x * scale, 200 + e_z * scale), 1)
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
