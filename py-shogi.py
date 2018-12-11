# https://pypi.org/project/python-shogi/

import shogi as s
import random, traceback, players

count_stock=[]
players = [players.AlphaBetaPlayer(0, 5), players.AlphaBetaPlayer(1, 5)]

for _ in range(3):
    board = s.Board()
    count = 0
    while(not board.is_checkmate()):
        # input()
        count += 1
        print("{}. {}".format(count,players[board.turn].move(board)))
        print(board.kif_str())
    print("まで{}手".format(count))
    count_stock.append(count)

print(count_stock)

# class MyBoard(s.Board):
#     def __init__(self):
#         super.__init__()
#         worth = 0
    

