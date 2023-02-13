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
