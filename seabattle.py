import random
import time

class BoardOutException(Exception):
    pass

class FullBoard(Exception):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True

    @staticmethod
    def get_key(a, value):
        for i, j in a.items():
            if j == value:
                return i
class Ship:
    _x = 0
    _y = 0
    _direction = 'h'
    def __init__(self, length):
        self.length = length
        self.lives = length

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if isinstance(value, int) and 0 < value < play.size:
            self._x = value
        elif value in dict.values():
            self._x = Dot.get_key(dict, value)
            if self._x == 0:
                self._x = 10
        else:
            raise BoardOutException

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value in range(1, play.size):
            self._y = value
        else:
            raise BoardOutException

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value == 'h' or 'v':
            self._direction = value
        else:
            raise BoardOutException

    def dots(self):
        lst = []
        for i in range(0, self.length):
            if self.direction == 'h':
                s_dot = Dot(self.x, self.y+i)
                lst.append(s_dot)
            if self.direction == 'v':
                s_dot = Dot(self.x+i, self.y)
                lst.append(s_dot)
        return lst

    def strike(self):
        self.lives -= 1
        if self.lives == 0:
            return True
        else:
            return False

class Board:
    def __init__(self):
        self.field = []
        self.ships = []
        self.lships = 0

    def clear(self):
        self.__init__()

    def create(self, size):
        for i in range(0, size):
            lst = []
            for j in range(0, size):
                if i == 0:
                    if j == 0:
                        lst.append(' ')
                    elif j == 10:
                        lst.append(0)
                    else:
                        lst.append(j)
                else:
                    if j == 0:
                        lst.append(Dot.get_key(dict, i))
                    else:
                        lst.append(' ')
            self.field.append(lst)

    def output(self):
        for i in range(0, len(self.field)):
            print(*self.field[i])

    def contour(self, ship):
        dots = ship.dots()
        for y in dots:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if self.field[y.x + i][y.y + j] == ' ':
                            self.field[y.x + i][y.y + j] = 'М'
                        self.field[0][0] = ' '
                    except IndexError:
                        pass

    def add_ship(self, ship):
        dots = ship.dots()
        if (dots[len(dots)-1].x < 0 or
            dots[len(dots)-1].x > (len(self.field) - 1) or
            (len(self.field) - 1) < dots[len(dots)-1].y or
            dots[len(dots)-1].y < 0):
            raise BoardOutException
        for i in dots:
            if self.field[i.x][i.y] != ' ':
                raise BoardOutException
        for i in dots:
            self.field[i.x][i.y] = 'Ц'
        self.contour(ship)
        self.ships.append(ship)

    def partially(self, point):
        self.field[point.x][point.y] = 'П'

    def miss(self, point):
        self.field[point.x][point.y] = 'М'

    def sunk(self, point):
        self.field[point.x][point.y] = 'У'

    def before(self):
        for i in range(1, len(self.field)):
            for j in range(1, len(self.field)):
                if self.field[i][j] == 'М':
                    self.field[i][j] = ' '

    def shot(self, point):
        if self.field[point.x][point.y] == ' ':
            self.miss(point)
            return False
        else:
            for i in self.ships:
                if point in i.dots():
                    is_sunk = i.strike()
                    if is_sunk:
                        self.lships -= 1
                        self.contour(i)
                        for j in i.dots():
                            self.sunk(j)
                        return i
                    else:
                        self.partially(point)
                        return point

    def array_free(self):
        free = []
        for i in range(1, len(self.field)):
            for j in range(1, len(self.field)):
                point = Dot(i, j)
                if self.field[point.x][point.y] == ' ':
                    free.append(point)
        return free

    def search_and_destroy(self, max_len):
        free = self.array_free()
        choise = []
        d_choise = []
        for i in free:
            count_h = 1
            count_v = 1
            try:
                for j in range(-1, (-max_len), -1):
                    if self.field[i.x + j][i.y] == ' ':
                        count_h += 1
                    else:
                        break
                for j in range(1, max_len):
                    if self.field[i.x + j][i.y] == ' ':
                        count_h += 1
                    else:
                        break
            except IndexError:
                pass
            try:
                for j in range(-1, (-max_len), -1):
                    if self.field[i.x][i.y + j] == ' ':
                        count_v += 1
                    else:
                        break
                for j in range(1, max_len):
                    if self.field[i.x][i.y + j] == ' ':
                        count_v += 1
                    else:
                        break
            except IndexError:
                pass
            if count_h >= max_len or count_v >= max_len:
                choise.append(i)
            if count_h >= max_len and count_v >= max_len:
                d_choise.append(i)
        if d_choise != []:
            return d_choise
        elif choise != []:
            return choise
        else:
            return free


class Player:
    def __init__(self, own_board, conter_board, counter_board_vis):
        self.own_board = own_board
        self.conter_board = conter_board
        self.conter_board_vis = counter_board_vis

    def ask(self, message='', board=None):
        pass

    def move(self):
        while True:
            try:
                message = 'Введите координаты выстрела'
                shot = self.ask(message=message, board=self.conter_board_vis)
                if isinstance(shot.x, str):
                    #print(f'Выстрел по координатам {coords}')
                    shot.x = dict[shot.x]
                    if shot.x == 0:
                        shot.x = 10
                else:
                    coords_pr = [shot.x, shot.y]
                    #if coords_pr[0] == 10:
                    #    coords_pr[0] = 0
                    if coords_pr[1] == 10:
                        coords_pr[1] = 0
                    coords_pr[0] = Dot.get_key(dict, coords_pr[0])
                    print(f'Выстрел по координатам {coords_pr}')
                if shot not in self.conter_board_vis.array_free():
                    raise BoardOutException
                check = self.conter_board.shot(shot)
                if isinstance(check, Ship):
                    print(f'Утопил! Осталось {self.conter_board.lships} кораблей')
                    for i in check.dots():
                        self.conter_board_vis.sunk(i)
                    self.conter_board_vis.contour(check)
                    time.sleep(1)
                    return True
                elif isinstance(check, Dot):
                    print('Попал!')
                    self.conter_board_vis.partially(check)
                    time.sleep(1)
                    return True
                else:
                    print('Мимо!')
                    self.conter_board_vis.miss(shot)
                    time.sleep(1)
                    return False
            except BoardOutException:
                print('В эту клетку бессмысленно стрелять')

class User(Player):
    def ship_set_up(self, size):
        if size == 7:
            shiplist_u = shiplist_u_s
        else:
            shiplist_u = shiplist_u_l
        while True:
            try:
                self.own_board.clear()
                self.own_board.create(size)
                self.own_board.output()
                for i in shiplist_u:
                    while True:
                        try:
                            message = f'Введите координаты верхней левой точки корбля, размер {i.length} клетка(и)'
                            coords = self.ask(message=message)
                            i.x = coords.x
                            i.y = coords.y
                            if i.length > 1:
                                while True:
                                    try:
                                        drtn = input('Выберите направление корабля: h - горизонтально, v - вертикально')
                                        drtn.lower()
                                        if not (drtn == 'h' or drtn == 'v'):
                                            raise BoardOutException
                                    except BoardOutException:
                                        print('Допустимы только буквы h и v')
                                    else:
                                        i.direction = drtn
                                        break
                            self.own_board.add_ship(i)
                            self.own_board.lships += 1
                            self.own_board.output()
                            count = len(self.own_board.array_free())
                            if count == 0 and len(self.own_board.ships) != len(shiplist_u):
                                raise FullBoard
                        except BoardOutException:
                            print('Здесь невозможно разместить корабль')
                        else:
                            break
            except FullBoard:
                print('Нет места для оставшихся кораблей. Постарайтесь разместить некоторые '
                      'корабли компактнее')
            else:
                break

    def ask(self, message='', board=None):
        coords = input(message)
        if len(coords) != 2:
            raise BoardOutException
        if coords[0].isalpha() and coords[1].isdigit():
            row = coords[0].upper()
            col = int(coords[1])
        elif coords[1].isalpha() and coords[0].isdigit():
            row = coords[1].upper()
            col = int(coords[0])
        else:
            raise BoardOutException
        if row not in dict.keys():
            raise BoardOutException
        if col == 0:
            col = 10
        row_n = dict[row]
        if row_n == 0:
            row_n = 10
        reply = Dot(row_n, col)
        return reply

class AI(Player):
    def ship_set_up(self, size):
        if size == 7:
            shiplist_c = shiplist_c_s
        else:
            shiplist_c = shiplist_c_l
        while True:
            self.own_board.clear()
            self.own_board.create(size)
            try:
                for i in shiplist_c:
                    count = 0
                    while True:
                        count += 1
                        if count == 5000:
                            raise BoardOutException
                        try:
                            edge = self.ask(board=self.own_board)
                            drtn = random.choice(['h', 'v'])
                            i.x = edge.x
                            i.y = edge.y
                            i.direction = drtn
                            self.own_board.add_ship(i)
                            self.own_board.lships += 1
                        except BoardOutException:
                            pass
                        else:
                            break
            except BoardOutException:
                pass
            else:
                break

    def ask(self, message='', board=None):
        free = board.array_free()
        hit = []
        for i in range(1, len(board.field)):
            for j in range(1, len(board.field)):
                point = Dot(i, j)
                if board.field[point.x][point.y] == 'П':
                    hit.append(point)
        if len(free) == 0:
            raise BoardOutException
        if len(hit) == 1:
            for i in hit:
                for j in [-1, 1]:
                    if i.x + j < len(board.field):
                        if board.field[i.x+j][i.y] == ' ':
                            point = Dot(i.x + j, i.y)
                            return point
                    if i.y + j < len((board.field)):
                        if board.field[i.x][i.y+j] == ' ':
                            point = Dot(i.x, i.y + j)
                            return point
        if len(hit) > 1:
            if hit[0].x == hit[1].x:
                if board.field[hit[0].x][(hit[0].y-1)] == ' ':
                    point = Dot(hit[0].x, hit[0].y - 1)
                    return point
                else:
                    point = Dot(hit[0].x, hit[len(hit)-1].y + 1)
                    return point
            if hit[0].y == hit[1].y:
                if board.field[(hit[0].x)-1][hit[0].y] == ' ':
                    point = Dot(hit[0].x - 1, hit[0].y)
                    return point
                else:
                    point = Dot(hit[len(hit)-1].x + 1, hit[0].y)
                    return point
        if message == 'Введите координаты выстрела':
            max_len = 1
            for i in self.conter_board.ships:
                if i.lives > max_len:
                    max_len = i.lives
            if max_len > 1:
                choise = board.search_and_destroy(max_len)
                point = (choise[random.randint(0, len(choise)-1)])
                return point
        point = (free[random.randint(0, len(free)-1)])
        return point

class Game:
    def __init__(self, user, board_u, ai, board_c):
        self.user = user
        self.board_user = board_u
        self.comp = ai
        self.board_comp = board_c
        self.size = 0

    def set_up(self):
        self.board_user.create(self.size)
        self.board_comp.create(self.size)
        board_u_vis.create(self.size)
        board_c_vis.create(self.size)
        self.user.ship_set_up(self.size)
        self.comp.ship_set_up(self.size)
        self.board_user.before()
        self.board_comp.before()

    def greet(self):
        print('Добро пожаловать в игру "Морской бой"! Формат команд реализован в виде')
        print('координат строк в буквенном выражении и столбцов в цифровом. Выбор направления размещения')
        print('корабля осуществляется буквами h и v. Состояние клеток на поле означает: Ц - целый корабль,')
        print('П - подбитый корабль, У - утонувший корабль, М - мимо. Наслаждайтесь!')
        print('')
        success = False
        while not success:
            request = input('Хотите сыграть в короткую (поле 6х6) или классическую (поле 10х10) игру?'
                            's - короткая, l - классическая')
            request.lower()
            if request == 's':
                self.size = 7
                success = True
            elif request == 'l':
                self.size = 11
                success = True

    def status(self):
        print('')
        print('Доска игрока:')
        board_u.output()
        print('')
        print('Доска компьтера:')
        board_c_vis.output()

    def loop(self):
        while True:
            first = input('Чей ход первый? u - пользователь, c - компьютер')
            first.lower()
            if first == 'u' or first == 'c':
                break
        self.status()
        while self.board_user.lships > 0 and self.board_comp.lships > 0:
            if first == 'u':
                turn = self.user.move()
                self.status()
                while turn and self.board_comp.lships > 0:
                    turn = self.user.move()
                    self.status()
                if self.board_comp.lships == 0:
                    print('Пользователь выиграл!')
                    break
                print('Выстрел компьютера!')
                turn = self.comp.move()
                self.status()
                time.sleep(1)
                while turn and self.board_user.lships > 0:
                    print('Выстрел компьютера!')
                    turn = self.comp.move()
                    self.status()
                    time.sleep(1)
                if self.board_user.lships == 0:
                    print('Компьютер выиграл!')
            if first == 'c':
                print('Выстрел компьютера!')
                turn = self.comp.move()
                self.status()
                time.sleep(1)
                while turn and self.board_user.lships > 0:
                    print('Выстрел компьютера!')
                    turn = self.comp.move()
                    self.status()
                    time.sleep(1)
                if self.board_user.lships == 0:
                    print('Компьютер выиграл!')
                    break
                turn = self.user.move()
                self.status()
                while turn and self.board_comp.lships > 0:
                    turn = self.user.move()
                    self.status()
                if self.board_comp.lships == 0:
                    print('Пользователь выиграл!')


dict = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5,
        'F':6, 'G':7, 'H':8, 'I':9, 'J':10}

battleship_u = Ship(4)
battleship_c = Ship(4)
cruiser1_u = Ship(3)
cruiser2_u = Ship(3)
cruiser1_c = Ship(3)
cruiser2_c = Ship(3)
destroyer1_u = Ship(2)
destroyer2_u = Ship(2)
destroyer1_c = Ship(2)
destroyer2_c = Ship(2)
destroyer3_u = Ship(2)
destroyer3_c = Ship(2)
boat1_u = Ship(1)
boat2_u = Ship(1)
boat3_u = Ship(1)
boat4_u = Ship(1)
boat1_c = Ship(1)
boat2_c = Ship(1)
boat3_c = Ship(1)
boat4_c = Ship(1)
shiplist_u_s = [cruiser1_u, destroyer1_u, destroyer2_u, boat1_u,
              boat2_u, boat3_u, boat4_u]
shiplist_c_s = [cruiser1_c, destroyer1_c, destroyer2_c, boat1_c,
              boat2_c, boat3_c, boat4_c]
shiplist_u_l = [battleship_u, cruiser1_u, cruiser2_u, destroyer1_u, destroyer2_u,
                destroyer3_u, boat1_u, boat2_u, boat3_u, boat4_u]
shiplist_c_l = [battleship_c, cruiser1_c, cruiser2_c, destroyer1_c, destroyer2_c,
                destroyer3_c, boat1_c, boat2_c, boat3_c, boat4_c]

board_u = Board()
board_u_vis = Board()
board_c = Board()
board_c_vis = Board()

us = User(board_u, board_c, board_c_vis)
comp = AI(board_c, board_u, board_u_vis)

play = Game(us, board_u, comp, board_c)

play.greet()
play.set_up()

#print('Доска игрока:')
#board_u.output()
#print('')
#print('Доска компьютера:')
#board_c.output()                    Показать корабли AI для отладки

play.loop()
