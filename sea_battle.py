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


# Класс доски
class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0  # Количество поражённых кораблей
        self.field = [["o"] * size for _ in range(size)]  # Инициализирую сетку
        self.busy = []  # точки занятые кораблём или стреляли
        self.ships = []  # список кораблей доски

    def __str__(self):  # вывод корабля на доску
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:  # Параметр hid нужно ли скрывать корабли на доске
            res = res.replace("■", "o")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):  # метод контур корабля
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."  # показываем, что точка занята
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        self.ships.append(ship)  # добавляем список собственных кораблей
        self.contour(ship)  # обводим по контуру
