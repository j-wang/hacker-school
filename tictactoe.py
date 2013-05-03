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
        if cell_num in top_l_bot_r_diag:
            to_log.append(maxr + maxc + 1 - 1) # -1 at end to reindex to 0

        if cell_num in top_r_bot_l_diag:
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

class GameNotOver(Exception):
    """GameInterface.end_game is called and game is not over."""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class GameInterface:
    """Textual interface for Tic-Tac-Toe game."""
    game = 0
    
    def __init__(self):
        self.game = self.main_menu()

    def print_game(self):
        max_col = self.game.max_col
        max_row = self.game.max_row
        
        """Prints the tic-tac-toe grid"""
        pad_size = int(math.floor(math.log10(max_col))) + 1 # max digits
        sys.stdout.write("\n")
        sys.stdout.write(' ' * pad_size + ' ')

        for cols in xrange(max_col): # print col numbers
            sys.stdout.write(str(cols + 1).rjust(pad_size + 1))

        print("\n")

        for rows in xrange(max_row):
            sys.stdout.write(str(rows + 1).rjust(pad_size + 1)) # print row number
            for col in xrange(max_col): # print grid elements
                sys.stdout.write(str(self.game.cells[rows][col]).rjust(pad_size+1))
            print("\n")

            #print(game_grid._victory_routes) #uncomment to see victory progression
    
    def main_menu(self):
        """Runs a text-based main menu for the game, returning a Grid object
        based on user input

        """
        print("* Tic-Tac-Toe Game! *\n")
        selected = self.print_menu()
        if not selected: return False

        return self.select_grid()
        
    def print_menu(self):
        """Prints and takes user input for the main menu of the game"""
        repeat_menu = True
        select = 0
        
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
        else: return select

    def select_grid(self):
        """Takes user input for a grid size, returns a Grid object based on
        selection

        """
        repeat_grid_select = True
        grid_size = 0
        
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

    def run_game(self):
        """Main loop running the tic-tac-toe game. Takes a Grid object."""
        turn = 0
        running = True
        game_again = True
        end_message = "Thanks for playing!"

        if not self.game:
            print("Ending game...")
        else:
            while running:
                player = 'O' if turn % 2 == 0 else 'X'
                self.print_game()
                print("Player {}'s turn.".format(player)),
                print("Pick row and column to tick (q to quit)")
                row, col = 0, 0

                row = self.take_row_col("row", self.game.max_row)
                if not row: # user selected q
                    print(end_message)
                    return False

                col = self.take_row_col("col", self.game.max_col)
                if not col:
                    print(end_message)
                    return False

                filled = self.game.fill_cell(int(row) - 1, int(col) - 1, player)

                if filled:
                    turn += 1
                    try:
                        game_again = self.end_game(turn)
                    except GameNotOver:
                        pass
                    else:
                        if not game_again:
                            print(end_message)
                        return game_again
                else:
                    print("Cell is already occupied! Try again.\n")

    def end_game(self, turn):
        """Takes a turn number. Runs appropriate end-game messages, based on
        status (if there is a winner or if game has exceeded its max number of
        turns. Asks user whether or not to play again and returns True if yes, False if no.

        Raises GameNotOver Exception if game isn't over.
 
        """
        winner = self.game.winner()
        max_turns = self.game.max_row * self.game.max_col

        if winner or turn >= max_turns:
            self.print_game()
            if winner:
                print("Player {} wins!".format(winner))
            else:
                print("No one wins!")
            try:
                print("Press 1 to return to main menu,"),
                print("or any other key to exit.")
                again = raw_input("What do you want to do?: ")
                if int(again) == 1:
                    return True
                else:
                    return False
            except ValueError:
                return False
        else: raise GameNotOver("Game isn't over.")
        
                    
    def take_row_col(self, row_or_col, max_row_or_col):
        """Takes string 'row' or 'col' and max number of rows or columns. Takes
        user input for row or column respectively. Returns int with row or
        column number based on user input. If user inputs q, return False.

        Throws exception if input is not 'row' or 'col' (case-insensitive)

        """
        user_input = True
        user_selection = 0
        row_col = row_or_col.lower()
        pretty_output = row_col.title()

        if row_col != "row" and row_col != "col":
            raise Exception("Method takes row or col as string.")
        
        while user_input:
            try:
                user_selection = raw_input(pretty_output + ": ")
                if user_selection == "q": 
                    return False
                elif int(user_selection) < 1 or int(user_selection) > max_row_or_col:
                    print("Invalid row. Try again.")
                else:
                    user_input = False
            except:
                print("Invalid input, try again.")

        return user_selection
                    
def main():
    run = True

    while run: # Lets the player restart game if he or she wishes to
        interface = GameInterface()
        run = interface.run_game()

if __name__ == "__main__":
    main()
                





