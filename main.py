import pygame
from numpy import sin, cos, array, tan
from math import pi


def get_spin_matrix(angle):
    return array([[cos(-angle), -sin(-angle)], [sin(-angle), cos(-angle)]])


def generate_vector(h_angle=0, v_angle=0, ad_h_angle=0, length=1):
    x = 0
    y = 1
    z = 0
    x, y = (sum(i) for i in array([x, y]) * get_spin_matrix(ad_h_angle))
    z, y = (sum(i) for i in array([z, y]) * get_spin_matrix(v_angle))
    x, y = (sum(i) for i in array([x, y]) * get_spin_matrix(h_angle))
    return array([x, y, z]) * length


class Camera:
    def __init__(self, x=0, y=0, z=0, angle_of_view=pi/4, v_angle=0, h_angle=0):
        self.angle_of_view = angle_of_view
        self.coords = array([float(x), float(y), float(z)])
        self.v_angle = v_angle
        self.h_angle = h_angle

    def rotate(self, v_angle=0, h_angle=0):
        self.h_angle += h_angle
        self.h_angle = self.h_angle % (2 * pi)
        self.v_angle += v_angle
        self.v_angle = self.v_angle % (2 * pi)

    def move_forward(self, step=0.5):
        self.coords += generate_vector(self.h_angle, self.v_angle) * step

    def move_back(self, step=0.5):
        self.coords -= generate_vector(self.h_angle, self.v_angle) * step

    def draw(self, screen, space):
        width, height = screen.get_size()
        rad = ((width ** 2 + height ** 2) ** 0.5)
        points = space.get_points()
        points -= self.coords
        rotate_points = []
        for x, y, z in points:
            x, y = (sum(i) for i in array([x, y]) * get_spin_matrix(-self.h_angle))
            z, y = (sum(i) for i in array([z, y]) * get_spin_matrix(-self.v_angle))
            rotate_points.append(array([x, y, z]))
        for point in rotate_points:
            way = (sum(point ** 2) ** 0.5)
            if sum(point * array([0, 1, 0])) / way >= cos(self.angle_of_view):
                x, y, z = point
                pygame.draw.circle(screen, (255, 255, 255), (int(width / 2 + rad * x / (y * tan(self.angle_of_view))), int(height / 2 - rad * z / (y * tan(self.angle_of_view)))), max((1, int(15 / way))))


class Space:
    def __init__(self, points):
        self.points = [array(coords) for coords in points]

    def add_point(self, x=0, y=0, z=0):
        self.points.append(array(x, y, z))

    def get_points(self):
        return self.points.copy()


running = True
fps = 25
clock = pygame.time.Clock()
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 400))
    print(screen.get_size())
    pygame.display.set_caption('3DEngine')
    camera = Camera(pi / 1.5)
    space = Space([[i * 0.05, 1, 0] for i in range(-90, 91)])
    while running:
        screen.fill((0, 0, 0))

        camera.draw(screen, space)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pressed_keys = list(pygame.key.get_pressed())
        print(pressed_keys.index(True) if True in pressed_keys else 'NF')
        if pressed_keys[26]:
            camera.move_forward(0.125)
        if pressed_keys[7]:
            camera.rotate(h_angle=pi/32)
        if pressed_keys[4]:
            camera.rotate(h_angle=-pi/32)
        if pressed_keys[22]:
            camera.move_back(0.125)
        if pressed_keys[82]:
            camera.rotate(v_angle=pi/32)
        if pressed_keys[81]:
            camera.rotate(v_angle=-pi/32)
        if pressed_keys[46]:
            camera.angle_of_view *= 1.0625
        if pressed_keys[45]:
            camera.angle_of_view /= 1.0625

        pygame.display.flip()
        clock.tick(fps)