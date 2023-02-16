# Класс координат
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # сравниваю две координаты
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


# Классы исключений
class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Попытка выстрелить за пределы игрового поля"


class BoardUsedException(BoardException):
    def __str__(self):
        return "В эту клетку уже стреляли"


class BoardWrongShipException(BoardException):
    pass


# Класс корабля
class Ship:
    def __init__(self, bow, parl, orient):  # параметр orient ориентация корабля (0 вертикальный, 1 горизонтальный)
        self.bow = bow
        self.parl = parl
        self.orient = orient
        self.lives = parl

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.parl):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orient == 0:
                cur_x += i

            elif self.orient == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shoten(self, shot):  # метод показывает попадание в корабль
        return shot in self.dots
