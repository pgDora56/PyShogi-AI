from enum import Enum

class Koma(Enum):
    EMP = 0
    SFu = 1
    SKy = 2
    SKe = 3
    SGi = 4
    SKi = 5
    SKa = 6
    SHi = 7
    SOu = 8
    STo = 9
    SNy = 10
    SNk = 11
    SNg = 12
    SUm = 14
    SRy = 15
    
    EFu = 17
    EKy = 18
    EKe = 19
    EGi = 20
    EKi = 21
    EKa = 22
    EHi = 23
    EOu = 24
    ETo = 25
    ENy = 26
    ENk = 27
    ENg = 28
    EUm = 30
    ERy = 31

    WAL = 32

class Kyokumen:
    def __init__(self):
        self.Board = []
        self.Board.append([Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL])
        self.Board.append([Koma.WAL, Koma.EKy, Koma.EKe, Koma.EGi, Koma.EKi, Koma.EOu, Koma.EKi, Koma.EGi, Koma.EKe, Koma.EKy, Koma.WAL])
        self.Board.append([Koma.WAL, Koma.EMP, Koma.EKa, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EHi, Koma.EMP, Koma.WAL])
        self.Board.append([Koma.WAL, Koma.EFu, Koma.EFu, Koma.EFu, Koma.EFu, Koma.EFu, Koma.EFu, Koma.EFu, Koma.EFu, Koma.EFu, Koma.WAL])
        self.Board.append([Koma.WAL, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.WAL])
        self.Board.append([Koma.WAL, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.WAL])
        self.Board.append([Koma.WAL, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.WAL])
        self.Board.append([Koma.WAL, Koma.SFu, Koma.SFu, Koma.SFu, Koma.SFu, Koma.SFu, Koma.SFu, Koma.SFu, Koma.SFu, Koma.SFu, Koma.WAL])
        self.Board.append([Koma.WAL, Koma.EMP, Koma.SHi, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.EMP, Koma.SKa, Koma.EMP, Koma.WAL])
        self.Board.append([Koma.WAL, Koma.SKy, Koma.SKe, Koma.SGi, Koma.SKi, Koma.SOu, Koma.SKi, Koma.SGi, Koma.SKe, Koma.SKy, Koma.WAL])
        self.Board.append([Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL, Koma.WAL])
        self.Hands = [0] * (Koma.EHi.value + 1)

    def __str__(self):
        op = ""
        for i in range(1, 10):
            row = ""
            for j in range(9, 0, -1):
                row += self.Board[i][j].name + " "
            op += row + "\n"
        return op

    def move(self, player, te):
        cap = self.Board[te.to.dan][te.to.suji].value % 8
        if te.fr.suji != 0:
            self.Board[te.fr.dan][te.fr.suji] = Koma.EMP
        else:
            self.Hands[(player<<4) + te.koma.value] -= 1
        if te.promote:
            self.Board[te.to.dan][te.to.suji] = te.koma<<3
        else:
            self.Board[te.to.dan][te.to.suji] = te.koma
        if cap != Koma.EMP:
            self.Hands[(player<<4) + cap] += 1

    def search(self, start_pos, _dir):
        pos = Position(0, 0)
        pos.add_dir(_dir)
        while self.Board[pos.dan][pos.suji] == Koma.EMP:
            pos.add_dir(_dir)
        return pos

    def make_pin_inf(self):
        pin = [[0] * 10 for _ in range(10)]
        KingS = Position(9, 5)
        KingE = Position(1, 5)
        for d in range(1, 10):
            for s in range(1, 10):
                if self.Board[d][s] == Koma.SOu:
                    KingS = Position(d, s)
                elif self.Board[d][s] == Koma.EOu:
                    KingE = Position(d, s)
        # KingSのpinチェック
        for i in range(8):
            p = self.search(KingS, Direct[i])
            if 0 < self.Board[p.dan][p.suji].value < 16:
                m = self.search(p, Direct[i])
                if 16 < self.Board[p.dan][p.suji].value < 32 and can_jump[i][self.Board[p.dan][p.suji].value]:
                    pin[p.dan][p.suji] = Direct[i]
        # KingEのpinチェック
        for i in range(8):
            p = self.search(KingE, Direct[i])
            if 16 < self.Board[p.dan][p.suji].value < 32:
                m = self.search(p, Direct[i])
                if 0 < self.Board[p.dan][p.suji].value < 16 and can_jump[i][self.Board[p.dan][p.suji].value]:
                    pin[p.dan][p.suji] = Direct[i]


class Position:
    def __init__(self, _dan, _suji):
        self.dan = _dan
        self.suji = _suji

    def add_dir(self, _dir):
        self.dan += _dir.dan
        self.suji += _dir.dan


class Hand:
    def __init__(self, _fr, _to, _koma, _promote):
        self.fr = _fr # Position
        self.to = _to # Position
        self.koma = _koma # Koma
        self.promote = _promote # bool
    
    def __str__(self):
        op = ""
        if self.fr.suji != 0:
            op += "{}{}".format(self.fr.suji, self.fr.dan)
        op += "{}{}{}".format(self.to.suji, self.to.dan, self.koma.name)
        if self.fr.suji == 0:
            op += "打"
        elif self.promote:
            op += "成"
        else:
            op += "　"
        return op



class Direction:
    def __init__(self, d, s):
        self.dan = d
        self.suji = s
    
    def __add__(self, other):
        return Direction(self.dan + other.dan, self.suji + other.suji)

    def __sub__(self, other):
        return Direction(self.dan - other.dan, self.suji - other.suji)

    def __eq__(self,  other):
        return self.dan == other.dan and self.suji == other.suji

    def __neg__(self):
        return Direction(-self.dan, -self.suji)

Direct = [
    Direction(0,1),
    Direction(1,1),
    Direction(1,0),
    Direction(1,-1),
    Direction(0,-1),
    Direction(-1,-1),
    Direction(-1,0),
    Direction(-1,1),

    Direction(1,-2),
    Direction(-1,-2),
    Direction(1,2),
    Direction(-1,-2)
]

can_move = [
    # (0, 1)下
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
    0, 1, 1, 0, 1, 1, 0 ,1, 1, 1, 1, 1, 1, 1, 1, 1],
    # (1, 1)左下
    [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1,
	0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    # (1, 0)左
	[0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    # (1, -1)左上
    [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    # (0, -1)上
    [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    # (-1, -1)右上
    [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    # (-1, 0)右
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    # (-1, 1)右下
    [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1,
    0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    # (1, -2), (-1, -2) 先手桂馬飛び
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # (1, 2), (-1, 2) 後手桂馬飛び
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

can_jump = [
    # (0, 1)下
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 
    0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    # (1, 1)左下
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
	0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    # (1, 0)左
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 
    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    # (1, -1)左上
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
	0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    # (0, -1)上
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 
    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    # (-1, -1)右上
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
	0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    # (-1, 0)右
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 
    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    # (-1, 1)右下
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
	0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    # (1, -2), (-1, -2) 先手桂馬飛び
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # (1, 2), (-1, 2) 後手桂馬飛び
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

k = Kyokumen()

print(k)

