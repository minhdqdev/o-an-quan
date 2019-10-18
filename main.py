"""
Mini Project: O An Quan

Authors:
- Dang Quang Minh (minh.dq176823@sis.hust.edu.vn)
- Pham Tuan Son
- Nguyen Hung
- Nguyen Viet Hoang
"""

from oanquan import *
from random import choice, randint

def main():
    # SETUP
    table = Table()

    player_1 = Player()
    player_2 = Player()
    state = choice(True, False)

    print("+----- O AN QUAN -----+\n")
    table.print_table()
    print()

    # GAMELOOP
    while True:
        # Check game's state
        if table.llist.head.data == [0, 2] and table.llist.getDataAtPos(6) == [0, 2]:
            # HET QUAN TOAN DAN KEO VE

            i1, i2 = table.llist.head, table.llist.getDataAtPos(6)
            for i in range(6):
                player_1.points += i1.data[0]
                player_2.points += i2.data[0]
                
                i1, i2 = i1.next, i2.next

            player_1.points -= table.borrow
            player_2.points += table.borrow

            if player_1.points > player_2.points:
                print("You win !")
            elif player_1.points < player_2.points:
                print("You lose!")
            else:
                print("Draw !")

        if state: # USER's turn
            move = []

            while True:
                ans = input("USER's move: ", end='').strip().split(' ')

                if len(ans) == 2:
                    try:
                        ans[0] = int(ans[0])

                        if ans[0] > 6 or ans[0] < 1 or ans[1] not in ['l', 'r']:
                            raise(ValueError)

                    except ValueError:
                        print("Wrong command !")
                        continue

                    move = ans
                    break
                else:
                    print("Wrong command !")

            player_1.play(table, move)

            print(f"USER's move: {move[0]} {move[1]}")

        else: # AI's turn
            move = [randint(7, 11), choice('l', 'r')]

            player_2.play(table, move)

            print(f"AI's move: {move[0]} {move[1]}")

if __name__ == '__main__':
    main()