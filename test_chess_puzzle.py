import pytest
from chess_puzzle import *


def test_locatio2index1():
    assert location2index("e2") == (5,2) # basic scenario

def test_locatio2index2():
    assert location2index("a1") == (1,1) # first element

def test_locatio2index3():
    assert location2index("z26") == (26,26) # last element

def test_locatio2index4():
    with pytest.raises(ValueError):
        assert location2index("")  # empty request

def test_locatio2index5():
    with pytest.raises(ValueError):
        assert location2index('11')  # incorrect request

def test_index2location1():
    assert index2location(5,2) == "e2" # basic scenario

def test_index2location2():
    assert index2location(1,1) == "a1" # first element

def test_index2location3():
    assert index2location(26,26) == "z26" # last element

def test_index2location4():
    with pytest.raises(ValueError):
        assert index2location(0,0)   # incorrect request

def test_index2location5():
    with pytest.raises(ValueError):
        assert index2location(27,27)   # incorrect request

wn1 = Knight(1,2,True)
wn2 = Knight(5,2,True)
wn3 = Knight(5,4, True)
wk1 = King(3,5, True)

bn1 = Knight(1,1,False)
bk1 = King(2,3, False)
bn2 = Knight(2,4, False)

B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
'''
  ♔  
 ♞  ♘
 ♚   
♘   ♘
♞    
'''

def test_is_piece_at1():
    assert is_piece_at(2,2, B1) == False

def test_is_piece_at2():
    assert is_piece_at(1,2, B1) == True

def test_is_piece_at3():
    assert is_piece_at(5,4, B1) == True

def test_is_piece_at4():
    assert is_piece_at(4,3, B1) == False

def test_is_piece_at5():
    assert is_piece_at(1,1, B1) == True

def test_piece_at1():
    assert piece_at(1,1, B1) == bn1

def test_piece_at2():
    assert piece_at(1,2, B1) == wn1

def test_piece_at3():
    assert piece_at(5,2, B1) == wn2

def test_piece_at4():
    assert piece_at(5,4, B1) == wn3

def test_piece_at5():
    assert piece_at(3,5, B1) == wk1

def test_piece_at6():
    assert piece_at(2,3, B1) == bk1

def test_piece_at7():
    assert piece_at(2,4, B1) == bn2

def test_can_reach_knight1():
    assert bn1.can_reach(2,2, B1) == False

def test_can_reach_knight2():
    assert wn1.can_reach(2,4, B1) == True

def test_can_reach_knight3():
    assert wn1.can_reach(3,1, B1) == True

def test_can_reach_knight4():
    assert bn1.can_reach(2,3, B1) == False

def test_can_reach_knight5():
    assert bn1.can_reach(3,2, B1) == True

def test_can_reach_king1():
    assert wk1.can_reach(2,2, B1) == False   

def test_can_reach_king2(): #try to move outside of the board
    assert wk1.can_reach(4,6, B1) == False   

def test_can_reach_king3():
    assert wk1.can_reach(4,4, B1) == True   

def test_can_reach_king4():
    assert bk1.can_reach(1,2, B1) == True  

def test_can_reach_king5():
    assert bk1.can_reach(3,3, B1) == True  

def test_can_reach_king6():
    assert bk1.can_reach(2,4, B1) == False

def test_can_reach_king7():
    assert bk1.can_reach(2,5, B1) == False

def test_can_move_to1():
    assert wk1.can_move_to(4,5, B1) == False #check appears after this move

def test_can_move_to2():
    assert wn2.can_move_to(3,1, B1) == True

def test_can_move_to3():
    assert wn1.can_move_to(3,1, B1) == True

def test_can_move_to4():
    assert wn3.can_move_to(3,4, B1) == False #cell is occupied by same side piece

def test_can_move_to5():
    assert bk1.can_move_to(2,2, B1) == True #normal move, black king takes white Knight

def test_move_to1():
    Actual_B = wn1.move_to(2,4, B1)
    wn1a = Knight(2,4,True)
    Expected_B = (5, [wn1a, bn1, wn2, wn3, wk1, bk1]) 
    '''
      ♔   
     ♘  ♘
     ♚   
        ♘
    ♞    
    '''

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to2():
    Actual_B = wn2.move_to(3,1, B1)
    wn2a = Knight(3,1,True)
    Expected_B = (5, [wn1, bn1, wn2a, bn2, wn3, wk1, bk1])

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to3():
    Actual_B = bk1.move_to(1,2, B1)
    bk1a = King(1,2,False)
    Expected_B = (5, [bn1, wn2, bn2, wn3, wk1, bk1a])

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to4():
    Actual_B = wk1.move_to(2,4, B1)
    wk1a = King(2,4,True)
    Expected_B = (5, [wn1, bn1, wn2, wn3, wk1a, bk1])

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to5():
    Actual_B = bn2.move_to(1,2, B1)
    bn2a = Knight(1,2,False)
    Expected_B = (5, [bn1, wn2, bn2a, wn3, wk1, bk1])

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_get_king1():
    assert get_king(True, B1) == wk1

def test_get_king2():
    assert get_king(False, B1) == bk1

def test_get_king3():
    assert get_king(False, B1) != bn1

def test_get_king4():
    assert get_king(False, B1) != bn2

def test_get_king5():
    assert get_king(True, B1) != wn2

def test_is_check1():
    wk1a = King(4,5,True)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1a, bk1])
    '''
       ♔  
     ♞  ♘
     ♚   
    ♘   ♘
    ♞    
    '''
    
    assert is_check(True, B2) == True

def test_is_check2():
    wk1a = King(4,5,True)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1a, bk1])
    assert is_check(False, B2) == False
    
def test_is_check3():
    wk1a = King(3,3,True)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1a, bk1])
    assert is_check(True, B2) == True

def test_is_check4():
    wk1a = King(3,3,True)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1a, bk1])
    assert is_check(False, B2) == True

def test_is_check5():
    wk1a = King(3,2,True)
    B2 = (5, [wn1, bn1, wn2, bn2, wn3, wk1a, bk1])
    assert is_check(False, B2) == True

def test_is_checkmate1():
    wk1a = King(1,5,True)
    bn2a = Knight(3,4, False)
    bn3 = Knight(4,4,False)
    B2 = (5, [wn1, wn2, wn3, wk1a, bn1, bk1, bn2a, bn3])
  
    '''
    ♔    
      ♞♞♘
     ♚   
    ♘   ♘
    ♞    
    '''
    assert is_checkmate(True, B2) == True

def test_is_checkmate2():
    wk1a = King(2,5,True)
    bn2a = Knight(3,4, False)
    bn3 = Knight(4,4,False)
    B2 = (5, [wn1, wn2, wn3, wk1a, bn1, bk1, bn2a, bn3])

    assert is_checkmate(True, B2) == False

def test_is_checkmate3():
    wk1a = King(5,1,True)
    wn1 = Knight(4,2, True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(4,1, True)
    bn3 = Knight(4,3, False)
    B2 = (5, [wn1, wn2, wn3, wk1a, bn1, bk1, bn3])

    assert is_checkmate(True, B2) == True

def test_is_checkmate4(): #same as previous, but there is white knight which can eliminate danger
    wk1a = King(5,1,True)
    wn1 = Knight(4,2, True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(4,1, True)
    bn3 = Knight(4,3, False)
    wn4 = Knight(3,5, True)
    B2 = (5, [wn1, wn2, wn3, wk1a, bn1, bk1, bn3, wn4])

    assert is_checkmate(True, B2) == False

def test_is_checkmate5(): #same as previous, but now two black knights attack simultaneously. So no option to eliminate the target.
    wk1a = King(5,1,True)
    wn1 = Knight(4,2, True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(4,1, True)
    bn3 = Knight(4,3, False)
    wn4 = Knight(3,5, True)
    bn4 = Knight(3,2, False)
    B2 = (5, [wn1, wn2, wn3, wk1a, bn1, bk1, bn3, wn4, bn4])

    assert is_checkmate(True, B2) == True

def test_is_stalemate1():

    wk1a = King(1,5, True)
    bn2a = Knight(1,3, False)
    B2 = (5, [wk1a, bn2a, bk1, bn1])

    assert is_stalemate(True, B2) == True

def test_is_stalemate2():

    wk1a = King(2,5, True)
    bn2a = Knight(1,3, False)
    B2 = (5, [wk1a, bn2a, bk1, bn1])

    assert is_stalemate(True, B2) == False

def test_is_stalemate3():

    wk1a = King(5,5, True)
    bn2a = Knight(4,2, False)
    bk1a = King(3,4, False)
    B2 = (5, [wk1a, bn2a, bk1a, bn1])

    assert is_stalemate(True, B2) == True

def test_is_stalemate4():

    wk1a = King(4,5, True)
    bn2a = Knight(4,2, False)
    bk1a = King(3,4, False)
    B2 = (5, [wk1a, bn2a, bk1a, bn1])

    assert is_stalemate(True, B2) == False

def test_is_stalemate5(): #checkmate situation

    wk1a = King(3,5, True)
    bn2a = Knight(4,2, False)
    bk1a = King(3,4, False)
    B2 = (5, [wk1a, bn2a, bk1a, bn1])

    assert is_stalemate(True, B2) == False

def test_create_piece1(): #base check that created piece is the same as should be
    new_piece = create_piece('Na1', True)
    test_piece = Knight(1,1, True)

    assert new_piece.pos_X == test_piece.pos_X and new_piece.pos_Y == test_piece.pos_Y and new_piece.side == test_piece.side and type(new_piece) == type(test_piece)
    
def test_create_piece2(): #change pos_X of test piece. Test will be OK if new piece is created correctly.
    new_piece = create_piece('Na1', True)
    test_piece = Knight(2,1, True)

    assert new_piece.pos_X != test_piece.pos_X and new_piece.pos_Y == test_piece.pos_Y and new_piece.side == test_piece.side and type(new_piece) == type(test_piece)

def test_create_piece3(): #change pos_Y of test piece. Test will be OK if new piece is created correctly.
    new_piece = create_piece('Na1', True)
    test_piece = Knight(1,2, True)

    assert new_piece.pos_X == test_piece.pos_X and new_piece.pos_Y != test_piece.pos_Y and new_piece.side == test_piece.side and type(new_piece) == type(test_piece)

def test_create_piece4(): #change side of test piece. Test will be OK if new piece is created correctly.
    new_piece = create_piece('Na1', True)
    test_piece = Knight(1,1, False)

    assert new_piece.pos_X == test_piece.pos_X and new_piece.pos_Y == test_piece.pos_Y and new_piece.side != test_piece.side and type(new_piece) == type(test_piece)

def test_create_piece5(): #change type of test piece. Test will be OK if new piece is created correctly.
    new_piece = create_piece('Na1', True)
    test_piece = King(1,1, True)

    assert new_piece.pos_X == test_piece.pos_X and new_piece.pos_Y == test_piece.pos_Y and new_piece.side == test_piece.side and type(new_piece) != type(test_piece)

def test_piece2str1():
    test_str = piece2str(King(1,1, True))
    assert test_str == 'Ka1'

def test_piece2str2():
    test_str = piece2str(Knight(3,3, True))
    assert test_str == 'Nc3'

def test_piece2str3():
    test_str = piece2str(Knight(3,3, True))
    assert test_str != 'Ka1'

def test_piece2str4():
    test_str = piece2str(King(1,1, True))
    assert test_str != 'Nc3'

def test_piece2str5():
    test_str = piece2str(King(6,6, False))
    assert test_str == 'Kf6'

def test_read_board1():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_read_board2(): #try to read not existing file
    with pytest.raises(IOError):
        assert read_board('not_existing_examp.txt')

def test_read_board3(): #try to read file with error in first line
    with pytest.raises(IOError):
        assert read_board('board_examp2.txt')

def test_read_board4(): #try to read file with error in second line
    with pytest.raises(IOError):
        assert read_board('board_examp3.txt')

def test_read_board5(): #try to read file with error in third line
    with pytest.raises(IOError):
        assert read_board('board_examp4.txt')

def test_read_board6(): #try to read file with 2 black kings
    with pytest.raises(IOError):
        assert read_board('board_examp5.txt')

def test_read_board7(): #try to read file with piece outside of board size
    with pytest.raises(IOError):
        assert read_board('board_examp6.txt')

def test_read_board8(): #try to read file with zero kings for white
    with pytest.raises(IOError):
        assert read_board('board_examp7.txt')

def test_read_board9(): #try to read file with two pieces on same field
    with pytest.raises(IOError):
        assert read_board('board_examp8.txt')

def test_read_board10(): #try to read file with board 2x2
    with pytest.raises(IOError):
        assert read_board('board_examp9.txt')

def test_read_board11(): #try to read file with board 27x27
    with pytest.raises(IOError):
        assert read_board('board_examp10.txt')

def test_read_board12(): #try to read file with piece outside of the board (v1)
    with pytest.raises(IOError):
        assert read_board('board_examp11.txt')

def test_read_board13(): #try to read file with piece outside of the board (v2)
    with pytest.raises(IOError):
        assert read_board('board_examp12.txt')

def test_save_board(): #here we test that what is written to file is exactly the same as what we initially read
    B = read_board("board_examp.txt")
    save_board("save_board_examp.txt", B)

    B1 = read_board("save_board_examp.txt")

    assert B[0] == B1[0]

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_X == piece1.pos_X and piece.pos_Y == piece1.pos_Y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_conf2unicode1():

    B = read_board("board_examp.txt")

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])

    board = conf2unicode(B)

    control_board = conf2unicode(B1)

    assert board == control_board

def test_conf2unicode2():

    B = read_board("board_examp.txt")

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])

    board = conf2unicode(B)

    '''
      ♔  
     ♞  ♘
     ♚   
    ♘   ♘
    ♞    
    '''

    assert board[2] == "\u2654"

def test_conf2unicode3():

    B = read_board("board_examp.txt")

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])

    board = conf2unicode(B)

    assert board[4] == "\u2001"

def test_conf2unicode4():

    B = read_board("board_examp.txt")

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])

    board = conf2unicode(B)

    assert board[7] == "\u265E"

def test_conf2unicode5():

    B = read_board("board_examp.txt")

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])

    board = conf2unicode(B)

    assert board[10] == "\u2658"

def test_white_move1():

    wn1 = Knight(1,2,True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(5,4, True)
    wn3a = Knight(4,2, True)
    wk1 = King(3,5, True)

    bn1 = Knight(1,1,False)
    bk1 = King(2,3, False)
    bn2 = Knight(2,4, False)

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Expected_B = (5, [wn1, bn1, wn2, bn2, wn3a, wk1, bk1])

    assert white_move('e4d2', B1) == Expected_B

def test_white_move2(): #try to move king under check, get IOError

    with pytest.raises(IOError):
        assert white_move('c5d5', B1)

def test_white_move3(): #try to move black piece, get IOError

    with pytest.raises(IOError):
        assert white_move('a1c2', B1)

def test_white_move4(): #try to move non-existing piece, get IOError

    with pytest.raises(IOError):
        assert white_move('a5b5', B1)

def test_white_move5(): #check that input is not case-sensitive

    wn1 = Knight(1,2,True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(5,4, True)
    wn3a = Knight(4,2, True)
    wk1 = King(3,5, True)

    bn1 = Knight(1,1,False)
    bk1 = King(2,3, False)
    bn2 = Knight(2,4, False)

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Expected_B = (5, [wn1, bn1, wn2, bn2, wn3a, wk1, bk1])

    assert white_move('E4D2', B1) == Expected_B

def test_white_move6(): #try to input non-valid move, get IOError

    with pytest.raises(IOError):
        assert white_move('abracadabra', B1)

def test_white_move7(): #try to enter incorrect value

    wn1 = Knight(1,2,True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(5,4, True)
    wn3a = Knight(4,2, True)
    wk1 = King(3,5, True)

    bn1 = Knight(1,1,False)
    bk1 = King(2,3, False)
    bn2 = Knight(2,4, False)

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Expected_B = (5, [wn1, bn1, wn2, bn2, wn3a, wk1, bk1])

    with pytest.raises(IOError):
        assert white_move(' e4d2', B1)

def test_white_move8(): #try to enter incorrect value

    wn1 = Knight(1,2,True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(5,4, True)
    wn3a = Knight(4,2, True)
    wk1 = King(3,5, True)

    bn1 = Knight(1,1,False)
    bk1 = King(2,3, False)
    bn2 = Knight(2,4, False)

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Expected_B = (5, [wn1, bn1, wn2, bn2, wn3a, wk1, bk1])

    with pytest.raises(IOError):
        assert white_move('e4 d2', B1)

def test_white_move9(): #try to enter incorrect value

    wn1 = Knight(1,2,True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(5,4, True)
    wn3a = Knight(4,2, True)
    wk1 = King(3,5, True)

    bn1 = Knight(1,1,False)
    bk1 = King(2,3, False)
    bn2 = Knight(2,4, False)

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Expected_B = (5, [wn1, bn1, wn2, bn2, wn3a, wk1, bk1])

    with pytest.raises(IOError):
        assert white_move('ee4d2', B1)

def test_white_move10(): #try to enter incorrect value

    wn1 = Knight(1,2,True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(5,4, True)
    wn3a = Knight(4,2, True)
    wk1 = King(3,5, True)

    bn1 = Knight(1,1,False)
    bk1 = King(2,3, False)
    bn2 = Knight(2,4, False)

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Expected_B = (5, [wn1, bn1, wn2, bn2, wn3a, wk1, bk1])

    with pytest.raises(IOError):
        assert white_move('e4d2 ', B1)

def test_white_move11(): #try to enter incorrect value

    wn1 = Knight(1,2,True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(5,4, True)
    wn3a = Knight(4,2, True)
    wk1 = King(3,5, True)

    bn1 = Knight(1,1,False)
    bk1 = King(2,3, False)
    bn2 = Knight(2,4, False)

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Expected_B = (5, [wn1, bn1, wn2, bn2, wn3a, wk1, bk1])

    with pytest.raises(IOError):
        assert white_move('e4dd2', B1)

def test_white_move12(): #try to enter incorrect value

    wn1 = Knight(1,2,True)
    wn2 = Knight(5,2,True)
    wn3 = Knight(5,4, True)
    wn3a = Knight(4,2, True)
    wk1 = King(3,5, True)

    bn1 = Knight(1,1,False)
    bk1 = King(2,3, False)
    bn2 = Knight(2,4, False)

    B1 = (5, [wn1, bn1, wn2, bn2, wn3, wk1, bk1])
    Expected_B = (5, [wn1, bn1, wn2, bn2, wn3a, wk1, bk1])

    with pytest.raises(IOError):
        assert white_move('e4d2d', B1)

def test_set_coordinates1():

     wn1 = Knight(1,2,True)

     wn1._set_coordinates(3,4)

     assert wn1.pos_X == 3 and wn1.pos_Y == 4

def test_set_coordinates2():

     wn1 = Knight(5,2,True)

     wn1._set_coordinates(3,4)

     assert wn1.pos_X == 3 and wn1.pos_Y == 4

def test_set_coordinates3():

     wn1 = Knight(5,2,True)

     wn1._set_coordinates(3,4)

     assert wn1.pos_X != 5 and wn1.pos_Y != 2

def test_set_coordinates4():

     bk1 = King(2,3, False)

     bk1._set_coordinates(2,4)

     assert bk1.pos_X == 2 and bk1.pos_Y == 4

def test_set_coordinates5():

     bk1 = King(2,3, False)

     bk1._set_coordinates(1,2)

     assert bk1.pos_X != 2 and bk1.pos_Y != 3