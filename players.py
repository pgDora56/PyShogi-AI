import random, shogi, traceback, copy, time

class Player:
    def __init__(self, _turn):
        self.turn = _turn

    def move(self, board):
        pass

    def str_hands(self, hand):
        color = "S"
        if self.turn == 1: color = "G"
        return "{} {}".format(color, hand)

class HumanPlayer(Player):
    alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    def make_hand_from_num(self, i,j):
        ix = int(i/9)
        iy = i % 9
        jx = int(j/9)
        jy = j % 9
        return "{}{}{}{}".format(ix,self.alphabets[iy],jx,self.alphabets[jy])

    def make_hand(self, x):
        if len(x) != 4:
            print("illegal hand")
            return None
        elif len(x) == 5:
            if x[4] == '+':
                if x[1] == '*': x1 = '*'
                else: x1 = self.alphabets[int(x[1])-1]
                x3 = self.alphabets[int(x[3])-1]
                return "{}{}{}{}+".format(x[0],x1,x[2],x3)
            print("illegal hand")
            return None
        else:
            if x[1] == '*': x1 = '*'
            else: x1 = self.alphabets[int(x[1])-1]
            x3 = self.alphabets[int(x[3])-1]
            return "{}{}{}{}".format(x[0],x1,x[2],x3)

    def move_sub(self, board, m):
        if(self.turn == board.turn):
            if(not shogi.Move.from_usi(m) in board.legal_moves):
                print("Don't Move {}".format(m))
                return False
            else:
                # board.push_usi(m)
                print("Move {}".format(m))
                return True
        print("Not your turn {}".format(m))
        return False
        
    def move(self, board):
        while True:
            plturn = self.make_hand(input("{} > ".format(board.turn)))
            try:
                b = self.move_sub(board, plturn)
                if b:
                    return plturn
            except:
                traceback.print_exc()
                pass
        
class WeakPlayer(Player):
    # 指せる手の中からひたすらランダムで指すクソザコ
    def move(self, board):
        r = str(random.choice(list(board.legal_moves)))
        board.push_usi(r)
        return self.str_hands(r)
        # print("ComMove {}".format(r))
        # return r

class WorthPlayer(Player):
    # 駒の価値のみを評価関数に組み込んでちょっと強くなった(弱い)
    # これだと端からさしてっちゃうからなんとかしなきゃ

    # 多少マシにはなったけど、まだまだ人間には程遠い…

    worth = {
        'P' : 100, 'p' : -100,
        'L' : 600, 'l' : -600,
        'N' : 700, 'n' : -700,
        'S' : 1000, 's' : -1000,
        'G' : 1200, 'g' : -1200,
        'B' : 1800, 'b' : -1800,
        'R' : 2000, 'r' : -2000,

        '+P' : 1200, '+p' : -1200,
        '+L' : 1200, '+l' : -1200,
        '+N' : 1200, '+n' : -1200,
        '+S' : 1200, '+s' : -1200,
        '+B' : 2000, '+b' : -2000,
        '+R' : 2200, '+r' : -2200,

        'K' : 100000, 'k' : -100000,

        'None' : 0
    }
    hands_worth = [0, 105, 630, 735, 1050, 1260, 1890, 2100]

    def move(self, board):
        self.tmp = copy.deepcopy(board)
        mov = None
        wor = -1
        for move in self.tmp.legal_moves:
            stream = []
            stream.append(str(move))
            self.tmp.push_usi(str(move))
            w = self.calculate_worth()
            stream.append(str(w))
            # print(':'.join(stream))
            if wor == -1: 
                wor = w
                mov = move
            else:
                if self.turn == 0:
                    if w > wor:
                        wor = w
                        mov = move
                else:
                    if w < wor:
                        wor = w
                        mov = move
            self.tmp.pop()
        board.push_usi(str(mov))
        return self.str_hands(mov)

    def calculate_worth(self):
        readstream = []

        score = 0
        start = time.time()
        for square in shogi.SQUARES:
            score += self.worth[str(self.tmp.piece_at(square))]
        readstream.append("square calculate:{}".format(time.time()-start))

        start = time.time()
        for color in [0, 1]:
            for piece_type, piece_count in self.tmp.pieces_in_hand[color].items():
                if color == 0: score += self.hands_worth[piece_type] * piece_count
                else: score -= self.hands_worth[piece_type] * piece_count
        readstream.append("hands calculate:{}".format(time.time()-start))

        start = time.time()
        ave_move = 0

        for mov in self.tmp.legal_moves:
            self.tmp.push_usi(str(mov))
            ave_move += len(list(self.tmp.legal_moves))
            self.tmp.pop()

        ave_move /= len(list(self.tmp.legal_moves))

        if self.turn == 0: score += ave_move
        if self.turn == 1: score -= ave_move
        readstream.append("moves_count calculate:{}".format(time.time()-start))
        print(" ".join(readstream))
        return score

class AlphaBetaPlayer(Player):
    # alpha-beta法を採用、自力で角道を開けるようになった！

    # やはり駒の交換ができないので、そこをちゃんとやるべきだろう。
    
    def __init__(self, t, _depthMax):
        self.turn = t
        self.depth_max = _depthMax

    worth = {
        'P' : 100, 'p' : -100,
        'L' : 600, 'l' : -600,
        'N' : 700, 'n' : -700,
        'S' : 1000, 's' : -1000,
        'G' : 1200, 'g' : -1200,
        'B' : 1800, 'b' : -1800,
        'R' : 2000, 'r' : -2000,

        '+P' : 1200, '+p' : -1200,
        '+L' : 1200, '+l' : -1200,
        '+N' : 1200, '+n' : -1200,
        '+S' : 1200, '+s' : -1200,
        '+B' : 2000, '+b' : -2000,
        '+R' : 2200, '+r' : -2200,

        'K' : 100000, 'k' : -100000,

        'None' : 0
    }
    hands_worth = [0, 105, 630, 735, 1050, 1260, 1890, 2100]

    def move(self, altboard):
        board = copy.deepcopy(altboard)
        mov = self.rec_move(board, 0, float('-inf'), float('inf'))
        altboard.push_usi(str(mov))
        return self.str_hands(mov)

    def rec_move(self, board, depth, alpha, beta, tur = -1):
        if tur == -1:
            tur = self.turn # 手番の設定がない場合は自身の手番を入れる
        if depth == self.depth_max:
            return self.calculate_worth(board) # 深さに達した場合は局面の評価値を返す
        
        mov = None
        wor = -1
        for move in board.legal_moves:
            stream = []
            stream.append(str(move))
            board.push_usi(str(move))
            w = self.rec_move(board, depth + 1, alpha, beta)
            stream.append(str(w))
            # print(':'.join(stream))
            if wor == -1: 
                wor = w
                mov = move
            else:
                if tur == 0:
                    if w > beta:
                        return w
                    if w > wor:
                        wor = w
                        mov = move
                        alpha = max(alpha, w)
                else:
                    if w < alpha:
                        return w
                    if w < wor:
                        wor = w
                        mov = move
                        beta = min(beta, w)
            board.pop()
        if depth == 0: return mov
        return wor

    # 駒交換の損得を見るアルゴリズムを組みたい
    def calculate_worth(self, _board):
        score = 0
        for square in shogi.SQUARES:
            score += self.worth[str(_board.piece_at(square))]

        for color in [0, 1]:
            for piece_type, piece_count in _board.pieces_in_hand[color].items():
                if color == 0: score += self.hands_worth[piece_type] * piece_count
                else: score -= self.hands_worth[piece_type] * piece_count
        
        # ave_move = 0

        # for mov in self.tmp.legal_moves:
        #     self.tmp.push_usi(str(mov))
        #     ave_move += len(list(self.tmp.legal_moves))
        #     self.tmp.pop()

        # ave_move /= len(list(self.tmp.legal_moves))

        # if self.turn == 0: score += ave_move
        # if self.turn == 1: score -= ave_move
        
        
        return score

class MontecarloPlayer(Player):
    # モンテカルロ木探索をやる

    def move(self, board):
        pass