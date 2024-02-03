import copy
import random
import sys

def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''

    if loc == '':
        raise ValueError
    
    if loc.isnumeric():
        raise ValueError

    if loc.isalpha():
        raise ValueError

    digits = '' # creating digits part of the location, since there could be more that one digit
    for element in loc:
        if element.isalpha(): # check if it is letter part of the location
            x = ord(element.lower()) - 96 #find number of digit in alphabet using ord function
        else:
            #digits do not require convertion, added as is
            digits += element 

    y = int(digits)

    return (x,y)
	
def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    
    # check correctness of incoming data
    if x < 1 or x > 26 or x == '':
        raise ValueError
    if y < 1 or y > 26 or y == '':
        raise ValueError
    
    # select char based on first parameter of index
    return(chr(x+96)+str(y))

class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.side = side_

    def _set_coordinates(self, x: int, y: int) -> None:
        '''setter functions which changes pos_X and pos_Y for the Piece'''

        self.pos_X = x
        self.pos_Y = y
    
    def can_reach(self, pos_X : int, pos_Y : int, B) -> bool:
        pass
    
    def can_move_to(self, pos_X : int, pos_Y : int, B) -> bool:
        pass
    
    def move_to(self, pos_X : int, pos_Y : int, B):
        pass

Board = tuple[int, list[Piece]]

def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B'''
    for figure in B[1]:
        if (figure.pos_X, figure.pos_Y) == (pos_X,pos_Y):
            return True
    return False
	
def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
    for figure in B[1]:
        if (figure.pos_X, figure.pos_Y) == (pos_X,pos_Y):
            return figure

    raise IOError    

class Knight(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)

    def __eq__(self, other):
        '''check if it is the same piece'''

        if other.pos_X == self.pos_X and other.pos_Y == self.pos_Y and other.side == self.side and type(other) == type(self):
            return True
        else:
            return False

    def _set_coordinates(self, x: int, y: int) -> None:
        '''setter functions which changes pos_X and pos_Y for the Knight'''

        self.pos_X = x
        self.pos_Y = y

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        '''
        
        # check if there is piece of the same side at target location
        if is_piece_at(pos_X, pos_Y, B):
            figure = piece_at(pos_X, pos_Y, B)
            if figure.side == self.side:
                return False
        
        #check if destination is within the board
        if pos_X > B[0] or pos_Y > B[0] or pos_X < 1 or pos_Y < 1:
            return False

        # calculate technical possibility to reach the target location
        if abs(self.pos_X - pos_X) == 2 and abs(self.pos_Y - pos_Y) == 1:
            return True
        elif abs(self.pos_X - pos_X) == 1 and abs(self.pos_Y - pos_Y) == 2:
            return True
        
        return False

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        '''

        # firstly, check [Rule1] and [Rule3] using can_reach
        if not self.can_reach(pos_X, pos_Y, B):
            return False

        # construct new board resulting from move
        new_board = self.move_to(pos_X, pos_Y, B)

        # to check [Rule4], use is_check on new board
        if is_check(self.side, new_board):
            return False
        else:
            return True
     
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this piece to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''

        # deep copy the given board
        new_board = copy.deepcopy(B)

        # identify if there is a piece on target location and remove it from the board
        if is_piece_at(pos_X, pos_Y, B):
            figure = piece_at(pos_X, pos_Y, B)
            new_board[1].remove(figure)

        # set new coordinates for the piece
        for figure in new_board[1]:
            if figure == self:
                figure._set_coordinates(pos_X, pos_Y)

        return new_board

class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)

    def __eq__(self, other):
        '''check if it is the same piece'''

        if other.pos_X == self.pos_X and other.pos_Y == self.pos_Y and other.side == self.side and type(other) == type(self):
            return True
        else:
            return False

    def _set_coordinates(self, x: int, y: int) -> None:
        '''setter functions which changes pos_X and pos_Y for the King'''

        self.pos_X = x
        self.pos_Y = y

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''

        # check if there is piece of the same side at target location
        if is_piece_at(pos_X, pos_Y, B):
            figure = piece_at(pos_X, pos_Y, B)
            if figure.side == self.side:
                return False

        #check if destination is within the board
        if pos_X > B[0] or pos_Y > B[0] or pos_X < 1 or pos_Y < 1:
            return False

        # calculate technical possibility to reach the target location
        if abs(self.pos_X - pos_X) == 1 and abs(self.pos_Y - pos_Y) == 0:
            return True
        elif abs(self.pos_X - pos_X) == 0 and abs(self.pos_Y - pos_Y) == 1:
            return True
        elif abs(self.pos_X - pos_X) == 1 and abs(self.pos_Y - pos_Y) == 1:
            return True
        else:
            return False
        
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''

        # firstly, check [Rule1] and [Rule3] using can_reach
        if not self.can_reach(pos_X, pos_Y, B):
            return False

        # construct new board resulting from move
        new_board = self.move_to(pos_X, pos_Y, B)

        # to check [Rule4], use is_check on new board
        if is_check(self.side, new_board):
            return False
        else:
            return True

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''

        # deep copy the given board
        new_board = copy.deepcopy(B)

        # identify if there is a piece on target location and remove it from the board
        if is_piece_at(pos_X, pos_Y, B):
            figure = piece_at(pos_X, pos_Y, B)
            new_board[1].remove(figure)

        # set new coordinates for the piece
        for figure in new_board[1]:
            if figure == self:
                figure._set_coordinates(pos_X, pos_Y)

        return new_board

def get_king(side: bool, B: Board) -> King:
    '''returns King object for a given side on a given board'''
    for figure in B[1]:
        if isinstance(figure, King) and figure.side == side:
            return figure

    raise IOError


def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    # get king to check if it is under threat
    king = get_king(side, B)
    
    # for each figure in the board if it is other side we check whether this figure can reach king
    for figure in B[1]:
        if figure.side != side and figure.can_reach(king.pos_X, king.pos_Y, B):
            return True
    
    return False

def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_reach 
    '''
    #first, check if there is check currently
    if not is_check(side, B):
        return False

    else:
        # find king for the side
        king = get_king(side, B)

        # try to find whether there is position where king can move without causing an another check
        for i in range(1, B[0]+1):
            for j in range(1, B[0]+1):
                if king.can_move_to(i,j, B):
                    return False

                #check if the situation can be eliminated by any other piece of the side
                for figure in B[1]:
                    if figure.side == side and figure.can_move_to(i,j, B):
                        return False

        # if there is a check and no other move - there is a checkmate
        return True

def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints: 
    - use is_check
    - use can_move_to 
    '''

    #first, check if there is check currently
    if is_check(side, B):
        return False

    else:

        for i in range(1, B[0]+1):
            for j in range(1, B[0]+1):
                for figure in B[1]:
                    if figure.side == side and figure.can_move_to(i,j, B): #if any figure can move to any positions - there is no stalemate
                        return False

        return True

def create_piece(abbreviature: str, side: bool) -> Piece:
    '''creates piece using string abbreviature contains in file'''

    index = location2index(abbreviature[1:])
    if abbreviature[0].upper() == 'N': #create kinght
        return Knight(index[0], index[1], side)
    elif abbreviature[0].upper() == 'K': #create king
        return King(index[0], index[1], side) #return piece
    else:
        raise IOError

def piece2str(figure: Piece) -> str:
    '''transforms Piece to string'''

    name = ''
    if isinstance(figure, King):
        name += 'K'
    else:
        name += 'N'
    name += index2location(figure.pos_X, figure.pos_Y)

    return name

def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''

    all_figures = []  # create empty list of figures

    try:
        board = open(filename)

        board_size = int(board.readline())  # read first line of file: it is size of a board

        if board_size < 3 or board_size > 26:
            raise IOError

        white_figures = board.readline().split(",")  # read second line of file: it contains list of white figures

        # create white pieces using special method create_piece
        for figure in white_figures:
            figure = figure.strip()

            # ensure there are no empty figures
            if figure == '':
                continue

            new_fig = create_piece(figure, True)
            all_figures.append(new_fig)

        black_figures = board.readline().split(",")  # read third line of file: it contains list of white figures

        # create black pieces using special method create_piece
        for figure in black_figures:
            figure = figure.strip()

            # ensure there are no empty figures
            if figure == '':
                continue

            new_fig = create_piece(figure, False)
            all_figures.append(new_fig)

        # check validity of the board
        num_of_w_kings = 0
        num_of_b_kings = 0
        for el in all_figures:
            if type(el) == King and el.side == True:
                num_of_w_kings += 1
            elif type(el) == King and el.side == False:
                num_of_b_kings += 1

            # check that all pieces are within the board
            if el.pos_X > board_size or el.pos_Y > board_size or el.pos_X < 1 or el.pos_Y < 1:
                raise IOError

        if num_of_w_kings != 1 or num_of_b_kings != 1:
            raise IOError

        # check for presence of two figure on same location
        for i in range(0, len(all_figures)):
            for j in range(i+1, len(all_figures)):
                if all_figures[i].pos_X == all_figures[j].pos_X and all_figures[i].pos_Y == all_figures[j].pos_Y:
                    raise IOError

        B = (board_size, all_figures)

    except:
        raise IOError

    return B

def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    
    # open file to save the configuration
    target_file = open(filename, 'w')

    # write first line
    target_file.write(str(B[0]) + '\n')

    white_figures = []
    black_figures = []

    # separate white figures from black ones
    for figure in B[1]:
        if figure.side == True:
            white_figures.append(piece2str(figure))
        else:
            black_figures.append(piece2str(figure))

    # write info to the file
    print(*white_figures, sep=", ", file=target_file)
    print(*black_figures, sep=", ", file=target_file)

    #close the file
    target_file.close()


def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''

    possible_moves = []

    for i in range(1, B[0]+1):
        for j in range(1, B[0]+1):
            for figure in B[1]:

                if figure.side == False and figure.can_move_to(i,j, B):
                    
                    # identify all possible moves for black
                    possible_moves.append((figure, i , j))

    # randomly select one of the moves
    move = random.choice(possible_moves)

    return move       

def conf2unicode(B: Board) -> str:
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''

    board = '' #initialise empty board

    for i in range(B[0], 0, -1): #go through rows
        line = '' #initialise empty line

        for j in range(1, B[0]+1): #go through columns
                found = False

                for figure in B[1]:

                    if figure.pos_X == j and figure.pos_Y == i:
                        if figure.side == True and type(figure) == King: #white king
                            line += '\u2654'
                            found = True
                        elif figure.side == True and type(figure) == Knight: #white Knight
                            line += '\u2658'
                            found = True
                        elif figure.side == False and type(figure) == King: #black king
                            line += '\u265A'
                            found = True
                        else:                                               #black Knight
                            line += '\u265E'
                            found = True
                if not found:
                    line += '\u2001'

        board += line + '\n' #drop line into the board

    return board

def white_move(request: str, B: Board) -> Board:
    '''makes move based on user request'''

    def get_piece_based_on_input(request: str, B: Board) -> tuple[Piece, int, int]:
        '''based on user input identify a piece and coordinates where it should move. Raises IOError if no such piece or it is black's piece'''

        # some checks on input quality
        if len(request) < 4 or len(request) > 6:
            raise IOError
        elif request[0].isdigit() or request[-1].isalpha():
            raise IOError
        elif ' ' in request:
            raise IOError

        # split user input in two parts: from and to
        for i in range(len(request)):
            if request[i].isdigit() and request[i+1].isalpha:
                from_ = request[:i+1]
                to = request[i+1:]
                break
        
        # another check on input quality
        for i in range(len(from_)):
            if from_[i].isalpha() and from_[i+1].isalpha():
                raise IOError
        for i in range(len(to)):
            if to[i].isalpha() and to[i+1].isalpha():
                raise IOError

        # tranforming from and to into coordinates
        from_index = location2index(from_)
        to_index = location2index(to)

        # return requested figure and to_coordinates as integers
        for figure in B[1]:
            if figure.pos_X == from_index[0] and figure.pos_Y == from_index[1] and figure.side == True:
                return(figure, to_index[0], to_index[1])
        
        #raise error if not possible to find
        raise IOError

    try:
        move_attempt = get_piece_based_on_input(request, B)
    except:
        raise IOError

    # try to make a move for white. If not possible - raise error.
    if move_attempt[0].can_move_to(move_attempt[1], move_attempt[2], B):
        return(move_attempt[0].move_to(move_attempt[1], move_attempt[2], B))
    else:
        raise IOError

def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''
    filename = input('\033[1mFile name for \033[0;0minitial configuration: ')

    # try to open board configuration
    while True:

        if filename == 'QUIT':
            sys.exit()

        try:

            B = read_board(filename)
            break

        except IOError:

            filename = input('This \033[1mis not\033[0;0m a valid file. \033[1mFile name for \033[0;0minitial configuration: ')
    
    # show initial configuration
    print('\nThe initial \033[1mconfiguration is:\033[0;0m')
    print(conf2unicode(B))

    # check if initial configuration is checkmate or stalemate
    if is_checkmate(False, B):
        print('Game \033[1mover\033[0;0m. White wins.')
        sys.exit()

    elif is_checkmate(True, B):
        print('Game \033[1mover\033[0;0m. Black wins')
        sys.exit()

    elif is_stalemate(True, B):
        print('Game \033[1mover\033[0;0m. Stalemate')
        sys.exit()

    # ask user to make first move
    next_move = input('\033[1mNext\033[0;34m move\033[0;0m of White: ')

    while True:

        # if user wants to finish the game we propose to save configuration
        if next_move == 'QUIT':
            save_to = input('\033[1mFile name to\033[0;0m store the configuration: ')
            save_board(save_to, B)
            print('The game configuration saved.')
            sys.exit()
        
        try:

            # make a move
            B = white_move(next_move, B)

            # print configuration
            print("\nThe \033[1mconfiguration after\033[0;0m White\033[0;31m's\033[0;0m move \033[1mis\033[0;0m:")
            print(conf2unicode(B))
            
            # check is game is over
            if is_checkmate(False, B):
                print('Game \033[1mover\033[0;0m. White wins.')
                sys.exit()
            elif is_stalemate(False, B):
                print('Game \033[1mover\033[0;0m. Stalemate.')
                sys.exit()

            # if not checkmate or stalemate - make black move
            else:
                black_move = find_black_move(B)

                B = black_move[0].move_to(black_move[1], black_move[2], B)

                # create str representation of black move
                black_from = index2location(black_move[0].pos_X, black_move[0].pos_Y)
                black_to = index2location(black_move[1], black_move[2])
                black_str = black_from + black_to
                
                # show result of black move
                print(f"\n\033[1mNext\033[0;0m move \033[1mof\033[0;0m Black \033[1mis\033[0;0m {black_str}. The \033[1mconfiguration after\033[0;0m Black\033[0;31m's\033[0;0m move \033[1mis\033[0;0m:")
                print(conf2unicode(B))

                # check for checkmate or stalemate for white
                if is_checkmate(True, B):
                    print('Game \033[1mover\033[0;0m. Black wins')
                    sys.exit()
                elif is_stalemate(True, B):
                    print('Game \033[1mover\033[0;0m. Stalemate')
                    sys.exit()
                else:

                    # again return to white
                    next_move = input('\033[1mNext\033[0;34m move\033[0;0m of White: ')
                    continue

        # if something goes wrong - ask to repeat input
        except IOError:

            next_move = input('This\033[1m is not\033[0;0m a valid move. \033[1mNext\033[0;0m move \033[1mof\033[0;0m White: ')

if __name__ == '__main__': #keep this in
   main()
