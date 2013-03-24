# Simple Tic-Tac-Toe Game
# tictactoe.py
# Written by James Wang
# 19 Mar 2013 - 24 Mar 2013
# Python 2.7.3, not compatible with Python 3 (see tictactoe3.py for Python 3
# compatible version)

# Ended up being a bit too 'clever' for my own good, I think, in trying to make
# this efficient for large grids and avoid recursive traversal to track win
# conditions -- readability/understandability suffers a bit here, with not much
# gain for smaller grids. I describe on GitHub my thought process behind the
# three coordinate systems used.

import math
import sys

class Grid:
    """Represents gameboard, can be called to fill individual cells"""
    cells = []
    max_row = 0
    max_col = 0
    _victory_routes = [] # represents each way to win (rows + cols + 2 diags)
    _connects_to_win = 0
        
    def __init__(self, rows, cols):
        """Initializes grid with the appropriate number of rows and columns
        Note: Implementation assumes that rows are equal to columns!
        
        """
        self.cells = [['-' for j in xrange(cols)] for i in xrange(rows)]
        self.max_row = rows
        self.max_col = cols
        self._victory_routes = [0 for x in xrange(rows + cols + 2)]
        self._connects_to_win = rows
        if rows != cols: raise ValueError("rows and cols must be equal")

    def fill_cell(self, row, col, xo):
        """Fills specified cell if unoccupied, notes progress to victory
        conditions, and return true. Returns false if cell occupied and does
        nothing.

        Arguments:
        row -- grid row (indexed from zero, e.g. 3x3 grid goes from 0 to 2)
        col -- grid column (indexed from zero, same as row)
        xo -- 'X' or 'O' character to specify player

        """
        if self.cells[row][col] != '-':
            return False # don't fill already filled spaces
        else:
            self.cells[row][col] = xo
            self._log_progress_to_victory(row, col, xo)
            return True

    def _log_diagonal_progress_to_victory(self, row, col, to_log):
        # Helper method to _log_progress_to_victory. Takes the row and col of
        # a grid cell and a list holding the victory routes affected by the
        # player move.

        maxr, maxc = self.max_row, self.max_col
        r, c = row + 1, col + 1 # math is easier when indexed from 1 vs 0
        
        # calculates diagonal ranges (when incrementing cells left to right)
        # (e.g. for 3x3: 1 2 3, 4 5 6, 7 8 9; 1 5 9 are a
        # diagonal). Ending cells have +1 b/c xrange goes up to 2nd arg - 1
        # This is essentially a second coordinate system (1st is row, col) to
        # better account for diagonal cells. Coord system is indexed from 1.
        diag_increment_lr = maxc - 1 + 2 # cells to move for next diag cell
        diag_increment_rl = maxc - 1 # same for right -> left direction
        top_l_bot_r_diag = xrange(1, maxr * maxc + 1, diag_increment_lr)
        top_r_bot_l_diag = xrange(maxc, maxr * (maxr-1) + 2, diag_increment_rl)
        cell_num = c + (r - 1) * maxr # cell ref in increment coord system

        # check if cell in diag, log if so -- center cell triggers both loops
        for i in top_l_bot_r_diag:
            if i == cell_num:
                to_log.append(maxr + maxc + 1 - 1) # -1 at end to reindex to 0

        for j in top_r_bot_l_diag:
            if j == cell_num:
                to_log.append(maxr + maxc + 2 - 1) # -1 at end to reindex to 0
        
    def _log_progress_to_victory(self, row, col, xo):
        # Logs the progress of X and O to victory through incrementing an array
        # holding 'routes' to victory (each row, column, & diagonal is a
        # route). O is represented with positives, X with negatives. A player
        # has won when any route contains abs(_connects_to_win). Implemented
        # this way to scale better than calling the more intuitive but costly
        # recursive traversal across the grid for each cell (or subset of
        # cells) to see if it's in a row.

        # This is essentially the third and final coordinate system, which
        # gives each route to victory its own array element

        # rows and columns are always v-routes, col converted to v-route coord
        v_routes_to_log = [row, col + self.max_row]
        self._log_diagonal_progress_to_victory(row, col, v_routes_to_log)
        
        v_incrementer = 0 # use proper sign for X vs O
        if xo == 'O':
            v_incrementer = 1
        elif xo == 'X':
            v_incrementer = -1
        else:
            raise ValueError("Needs to take X or O")

        # Track progress in each route to victory
        for x in v_routes_to_log:
            self._victory_routes[x] += v_incrementer
        
    def winner(self):
        """ Returns X or O if victory conditions (connections in a row) are met
        for either player, else returns False.

        """
        for x in self._victory_routes:
            if x >= self._connects_to_win: return 'O'
            elif x <= -(self._connects_to_win): return 'X'

        return False

def print_game(game_grid):
    """Prints the tic-tac-toe grid"""
    pad_size = int(math.floor(math.log10(game_grid.max_col))) + 1 # max digits
    sys.stdout.write("\n")
    sys.stdout.write(' ' * pad_size + ' ')
    
    for cols in xrange(game_grid.max_col): # print col numbers
        sys.stdout.write(str(cols + 1).rjust(pad_size + 1))

    print("\n")
        
    for rows in xrange(game_grid.max_row):
        sys.stdout.write(str(rows + 1).rjust(pad_size + 1)) # print row number
        for col in xrange(game_grid.max_col): # print grid elements
            sys.stdout.write(str(game_grid.cells[rows][col]).rjust(pad_size+1))
        print("\n")

        #print(game_grid._victory_routes) #uncomment to see victory progression
    
def main_menu():
    """Prints and takes user input for the main menu of the game"""
    repeat_menu = True
    repeat_grid_select = True
    select = 0
    grid_size = 0
    
    print("* Tic-Tac-Toe Game! *\n")

    while repeat_menu:
        print("Menu selection")
        print("1) New Game")
        print("2) Quit")
        try:
            select = int(raw_input("Enter selection: "))
            if select != 1 and select != 2:
                print("Invalid selection.")
            else:
                repeat_menu = False
        except ValueError:
            print("Invalid selection.")

    if select == 2: return False # quit
            
    while repeat_grid_select:
        try:
            grid_size = int(raw_input(
                "Enter desired grid size (e.g. 3 for 3x3). Odd numbers only: "))
            if grid_size > 15: # starts to exceed screen sizes
                print("Grids this large are unsupported (may look ugly).")
                keep_going = raw_input("Continue anyway? (y/n): ")
                if str(keep_going) != "y":
                    grid_size = 0
                else:
                    repeat_grid_select = False
            elif grid_size % 2 == 0:
                print("Currently, the game only supports odd numbered grids.")
            elif grid_size == 1:
                print("That wouldn't be very interesting.")
            else: 
                repeat_grid_select = False
        except ValueError:
            print("Invalid selection.")

    return Grid(grid_size, grid_size)

def run_game():
    """Main loop running the tic-tac-toe game."""
    game = main_menu()
    turn = 0
    running = True
    end_message = "Thanks for playing!"
    
    if not game:
        print("Ending game...")
    else:
        max_turns = game.max_row * game.max_col
        while running:
            player = 'O' if turn % 2 == 0 else 'X'
            print_game(game)
            print("Player {}'s turn.".format(player)),
            print("Pick row and column to tick (q to quit)")
            row_input, col_input = True, True
            row, col = 0, 0

            while row_input:
                try:
                    row = raw_input("Row: ")
                    if row == "q": 
                        print(end_message)
                        return False
                    elif int(row) < 1 or int(row) > game.max_row:
                        print("Invalid row. Try again.")
                    else:
                        row_input = False
                except:
                    print("Invalid input, try again.")
                        
            while col_input and running:
                try:
                    col = raw_input("Column: ")
                    if col == "q": 
                        print(end_message)
                        return False
                    elif int(col) < 1 or int(col) > game.max_col:
                        print("Invalid column. Try again.")
                    else:
                        col_input = False
                except:
                    print("Invalid input, try again.")

            filled = game.fill_cell(int(row) - 1, int(col) - 1, player)

            if filled:
                turn += 1
                winner = game.winner()
                if winner or turn >= max_turns:
                    print_game(game)
                    if winner:
                        print("Player {} wins!".format(winner))
                    elif turn >= max_turns:
                        print("No one wins!")
                    try:
                        print("Press 1 to return to main menu,"),
                        print("or any other key to exit.")
                        again = raw_input("What do you want to do?: ")
                        if int(again) == 1:
                            return True
                        else:
                            print(end_message)
                            return False
                    except ValueError:
                        print(end_message)
                        return False
            else:
                print("Cell is already occupied! Try again.\n")

def main():
    run = True

    while run: # Lets the player restart game if he or she wishes to
        run = run_game()

if __name__ == "__main__":
    main()
                
