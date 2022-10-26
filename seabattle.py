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
        if isinstance(value, int) and 0 < value < len(board_u.field):
            self._x = value
        elif value in dict.values():
            self._x = get_key(dict, value)
            if self._x == 0:
                self._x = 10
        else:
            raise BoardOutException

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value in range(1, len(board_u.field)):
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
                lst.append([self.x, self.y + i])
            if self.direction == 'v':
                lst.append([self.x + i, self.y])
        return lst

class Board:
    def __init__(self):
        self.field =[]
        self.ships = []
        self.lships = 0

    def clear(self):
        self.field = []
        self.ships = []
        self.lships = 0

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
                        if i == 10:
                            lst.append(dict.get(0))
                        else:
                            lst.append(dict.get(i))
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
                        if self.field[y[0]+i][y[1]+j] == ' ':
                            self.field[y[0] + i][y[1] + j] = 'М'
                        self.field[0][0] = ' '
                    except IndexError:
                        pass

    def add_ship(self, ship):
        dots = ship.dots()
        if (dots[len(dots)-1][0] < 0 or
            dots[len(dots)-1][0] > (len(self.field) - 1) or
            (len(self.field) - 1) < dots[len(dots)-1][1] or
            dots[len(dots)-1][1] < 0):
            raise BoardOutException
        for i in dots:
            if self.field[i[0]][i[1]] != ' ':
                raise BoardOutException
        for i in dots:
            self.field[i[0]][i[1]] = 'Ц'
        self.contour(ship)
        self.ships.append(ship)

    def before(self):
        for i in range(1, len(self.field)):
            for j in range(1, len(self.field)):
                if self.field[i][j] == 'М':
                    self.field[i][j] = ' '

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
                coords = self.ask(message=message, board=self.conter_board_vis)
                if isinstance(coords[0], str):
                    #print(f'Выстрел по координатам {coords}')
                    coords[0] = get_key(dict, coords[0])
                    if coords[0] == 0:
                        coords[0] = 10
                else:
                    coords_pr = coords.copy()
                    if coords_pr[0] == 10:
                        coords_pr[0] = 0
                    if coords_pr[1] == 10:
                        coords_pr[1] = 0
                    coords_pr[0] = dict.get(coords_pr[0])
                    print(f'Выстрел по координатам {coords_pr}')
                if self.conter_board_vis.field[coords[0]][coords[1]] != ' ':
                    raise BoardOutException
                if self.conter_board.field[coords[0]][coords[1]] == ' ':
                    self.conter_board.field[coords[0]][coords[1]] = 'М'
                    self.conter_board_vis.field[coords[0]][coords[1]] = 'М'
                    print('Мимо!')
                    time.sleep(3)
                    return False
                else:
                    shot = Dot(coords[0], coords[1])
                    for i in self.conter_board.ships:
                        dotlist = []
                        for j in i.dots():
                            shipdot = Dot(j[0], j[1])
                            dotlist.append(shipdot)
                        if shot in dotlist:
                            i.lives -= 1
                            if i.lives == 0:
                                self.conter_board.lships -= 1
                                self.conter_board_vis.contour(i)
                                self.conter_board.contour(i)
                                print(f'Утопил! Осталось {self.conter_board.lships} кораблей')
                                time.sleep(3)
                                for k in i.dots():
                                    self.conter_board_vis.field[k[0]][k[1]] = 'У'
                                    self.conter_board.field[k[0]][k[1]] = 'У'
                            else:
                                self.conter_board_vis.field[shot.x][shot.y] = 'П'
                                self.conter_board.field[shot.x][shot.y] = 'П'
                                print('Попал!')
                                time.sleep(3)
                    return True
            except BoardOutException:
                print('В эту клетку бессмысленно стрелять')


class User(Player):
    def ship_set_up(self, size):
        if size == 7:
            shiplist_u = shiplist_u_s
        else:
            shiplist_u = shiplist_u_l
        success_out = False
        while not success_out:
            try:
                self.own_board.clear()
                self.own_board.create(size)
                self.own_board.output()
                for i in shiplist_u:
                    success = False
                    while not success:
                        try:
                            message = f'Введите координаты верхней левой точки корбля, размер {i.length} клетка(и)'
                            coords = self.ask(message=message)
                            i.x = coords[0]
                            i.y = coords[1]
                            if i.length > 1:
                                success_in = False
                                while not success_in:
                                    try:
                                        drtn = input('Выберите направление корабля: h - горизонтально, v - вертикально')
                                        drtn.lower()
                                        if not (drtn == 'h' or drtn == 'v'):
                                            raise BoardOutException
                                    except BoardOutException:
                                        print('Допустимы только буквы h и v')
                                    else:
                                        success_in = True
                                        i.direction = drtn
                            board_u.add_ship(i)
                            board_u.lships += 1
                            board_u.output()
                            count = 0
                            for a in range(1, len(self.own_board.field)):
                                for b in range(1 , len(self.own_board.field)):
                                    if self.own_board.field[a][b] == ' ':
                                        count += 1
                            if count == 0 and len(self.own_board.ships) != len(shiplist_u):
                                raise FullBoard
                        except BoardOutException:
                            print('Здесь невозможно разместить корабль')
                        else:
                            success = True
            except FullBoard:
                print('Нет места для оставшихся кораблей. Постарайтесь разместить некоторые '
                      'корабли компактнее')
            else:
                success_out = True

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
        if row not in dict.values():
            raise BoardOutException
        if col == 0:
            col = 10
        return [row, col]

class AI(Player):
    def ship_set_up(self, size):
        if size == 7:
            shiplist_c = shiplist_c_s
        else:
            shiplist_c = shiplist_c_l
        success = False
        while not success:
            self.own_board.clear()
            self.own_board.create(size)
            try:
                for i in shiplist_c:
                    success_in = False
                    count = 0
                    while not success_in:
                        count += 1
                        if count == 5000:
                            raise BoardOutException
                        try:
                            x, y = self.ask(board=self.own_board)
                            drtn = random.choice(['h', 'v'])
                            i.x = x
                            i.y = y
                            i.direction = drtn
                            self.own_board.add_ship(i)
                            self.own_board.lships += 1
                        except BoardOutException:
                            pass
                        else:
                            success_in = True
            except BoardOutException:
                pass
            else:
                success = True

    def ask(self, message='', board=None):
        free = []
        hit = []
        for i in range(1, len(board.field)):
            for j in range(1, len(board.field)):
                if board.field[i][j] == ' ':
                    free.append([i, j])
                if board.field[i][j] == 'П':
                    hit.append([i, j])
        if len(free) == 0:
            raise BoardOutException
        if len(hit) == 1:
            for i in hit:
                for j in [-1, 1]:
                    if i[0] + j < len(board.field):
                        if board.field[i[0]+j][i[1]] == ' ':
                            return [i[0]+j, i[1]]
                    if i[1] + j < len((board.field)):
                        if board.field[i[0]][i[1]+j] == ' ':
                            return [i[0], i[1]+j]
        if len(hit) > 1:
            if hit[0][0] == hit[1][0]:
                if board.field[hit[0][0]][(hit[0][1]-1)] == ' ':
                    return [hit[0][0], (hit[0][1]-1)]
                else:
                    return [hit[0][0], (hit[len(hit)-1][1]+1)]
            if hit[0][1] == hit[1][1]:
                if board.field[(hit[0][0])-1][hit[0][1]] == ' ':
                    return [(hit[0][0])-1, hit[0][1]]
                else:
                    return [(hit[len(hit)-1][0]+1), hit[0][1]]
        if message == 'Введите координаты выстрела':
            max_len = 1
            for i in board_u.ships:
                if i.lives > max_len:
                    max_len = i.lives
            if max_len > 1:
                choise = []
                d_choise = []
                for i in free:
                    count_h = 1
                    count_v = 1
                    #if i[0] < (len(board.field) - max_len + 1):
                    try:
                        for j in range(-1, (-max_len), -1):
                            if board.field[i[0]+j][i[1]] == ' ':
                                count_h += 1
                            else:
                                break
                        for j in range (1, max_len):
                            if board.field[i[0]+j][i[1]] == ' ':
                                count_h += 1
                            else:
                                break
                    except IndexError:
                        pass
                    #if i[1] < (len(board.field) - max_len + 1):
                    try:
                        for j in range(-1, (-max_len), -1):
                            if board.field[i[0]][i[1]+j] == ' ':
                                count_v += 1
                            else:
                                break
                        for j in range(1, max_len):
                            if board.field[i[0]][i[1]+j] == ' ':
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
                    x, y = (d_choise[random.randint(0, len(d_choise)-1)])
                    return [x, y]
                x, y = (choise[random.randint(0, len(choise)-1)])
                return [x, y]
        x, y = (free[random.randint(0, len(free)-1)])
        return [x, y]

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
        success = False
        while not success:
            first = input('Чей ход первый? u - пользователь, c - компьютер')
            first.lower()
            if first == 'u' or first == 'c':
                success = True
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
                time.sleep(2)
                while turn and self.board_user.lships > 0:
                    print('Выстрел компьютера!')
                    turn = self.comp.move()
                    self.status()
                    time.sleep(2)
                if self.board_user.lships == 0:
                    print('Компьютер выиграл!')
            if first == 'c':
                print('Выстрел компьютера!')
                turn = self.comp.move()
                self.status()
                time.sleep(2)
                while turn and self.board_user.lships > 0:
                    print('Выстрел компьютера!')
                    turn = self.comp.move()
                    self.status()
                    time.sleep(2)
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


def get_key(a:dict, value):
    for i, j in a.items():
        if j == value:
            return i

dict = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E',
        6:'F', 7:'G', 8:'H', 9:'I', 0:'J'}

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
