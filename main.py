# Импорт библиотек и математических функций
import pygame
from numpy import sin, cos, array, tan
from math import pi


# Функция, возвращающая 2-мерный массив, позволяющий свести поворот точки
# к умножению её координат на его соответствующие элементы
def get_spin_matrix(angle):
    return array([[cos(-angle), -sin(-angle)], [sin(-angle), cos(-angle)]])


# Функция, поворачивающая единичный вектор по 2 заданным углам и
# возвращающая результат в виде массива из 3 точек
def generate_vector(h_angle=0, v_angle=0, ad_h_angle=0, length=1):
    x = 0
    y = 1
    z = 0
    x, y = (sum(i) for i in array([x, y]) * get_spin_matrix(ad_h_angle))
    z, y = (sum(i) for i in array([z, y]) * get_spin_matrix(v_angle))
    x, y = (sum(i) for i in array([x, y]) * get_spin_matrix(h_angle))
    return array([x, y, z]) * length


# Абстракция, имитирующая физическую камеру.
class Camera:
    def __init__(self, x=0, y=0, z=0, angle_of_view=pi/4, v_angle=0, h_angle=0):
        self.angle_of_view = angle_of_view
        # Обладает собственными координатами в пространстве
        self.coords = array([float(x), float(y), float(z)])
        # Угол наклона
        self.v_angle = v_angle
        # Угол поворота
        self.h_angle = h_angle

    # Метод для изменения углов поворота и наклона камеры
    def rotate(self, v_angle=0, h_angle=0):
        # Прибавляем полученный угол поворота к уже имеющемуся
        self.h_angle += h_angle
        # Для рационализации удерживаем этот угол на полуинтервале [0; 2 * pi)
        self.h_angle = self.h_angle % (2 * pi)
        # Прибавляем полученный угол наклона к уже имеющемуся
        self.v_angle += v_angle
        #  Для рационализации удерживаем этот угол на полуинтервале [0; 2 * pi)
        self.v_angle = self.v_angle % (2 * pi)

    # Метод для перемещения камеры вперёд
    def move_forward(self, step=0.5):
        # Строим единичный вектор, основываясь на углах поворота камеры,
        # умножаем на полученную длину перемещения и прибавляем его координаты к координатам камеры
        self.coords += generate_vector(self.h_angle, self.v_angle) * step

    # Метод для перемещения камеры назад
    def move_back(self, step=0.5):
        # Строим единичный вектор, основываясь на углах поворота камеры,
        # умножаем на полученную длину перемещения и вычитаем его координаты из координат камеры
        self.coords -= generate_vector(self.h_angle, self.v_angle) * step

    # Метод отрисовки изображения с камеры на холст
    def draw(self, screen, space):
        # Получение размеры холста для корректировки размера отрисовываемого изображения
        width, height = screen.get_size()
        rad = ((width ** 2 + height ** 2) ** 0.5)
        # Получение все точки пространства
        points = space.get_points()
        # Перемещение все точки копии пространства в систему координат,
        # для которой центром является камера
        points -= self.coords
        # Поворот всех полученных точек таким образом,
        # чтобы в полученной системе координат углы поворота и наклона камеры были нулевыми
        rotate_points = []
        for x, y, z in points:
            x, y = (sum(i) for i in array([x, y]) * get_spin_matrix(-self.h_angle))
            z, y = (sum(i) for i in array([z, y]) * get_spin_matrix(-self.v_angle))
            rotate_points.append(array([x, y, z]))

        # Анализ всех точек на предмет попадания в область видимости камеры и их отрисовка
        # в соответствии с расстоянием от начала координат до этих точек
        for point in rotate_points:
            # Расстояние от начала координат до точки
            way = (sum(point ** 2) ** 0.5)
            # Сортировка точек и отрисовка их на холсте в виде окружностей
            if sum(point * array([0, 1, 0])) / way >= cos(self.angle_of_view):
                x, y, z = point
                pygame.draw.circle(screen, (255, 255, 255), (int(width / 2 + rad * x / (y * tan(self.angle_of_view))), int(height / 2 - rad * z / (y * tan(self.angle_of_view)))), max((1, int(15 / way))))


# Класс для хранения точек пространства
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
