from random import randint


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

    def shot(self, d):  # стрельба по доске
        if self.out(d):  # выбрасываю исключение, точка за границей
            raise BoardOutException()
        if d in self.busy:  # выбрасываю исключение, точка занята
            raise BoardUsedException()
        self.busy.append(d)
        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "x"  # корабль подбит
                if ship.lives == 0:
                    self.count += 1  # счётчик уничтоженных кораблей
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен")
                    return False
                else:
                    print("Корабль подбит")
                    return True
        self.field[d.x][d.y] = "."
        print("Мимо")
        return False

    def begin(self):
        self.busy = []


# Класс игрока
class Player:
    def __int__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:  # пытаемся выполнить выстрел
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


# Класс игрок компьютер
class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1}{d.y+1}")
        return d


# Класс игрок пользователь
class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print("Введите две координаты")
                continue
            x, y = cords
            if not(x.isdigit()) or not (y.isdigity()):
                print("Введите числа")
                continue
            x, y = int(x), int(y)
            return Dot(x-1, y-1)
