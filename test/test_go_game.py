from go_game import game

def test_check_for_self_capture_simplest_case():
    black = game.Player(color='black', name='Arna')
    white = game.Player(color='white', name='Sean')
    board = game.Board(9, black, white)
    # put some pieces down
    board.make_move(3, 2, white.color)
    board.make_move(3, 4, white.color)
    board.make_move(2, 3, white.color)
    board.make_move(4, 3, white.color)
    # comment back in to confirm placement
    # board.render()
    # now check for self capture if you were to put a black
    # down at 3, 3 should return True
    potential_move = game.CrossHair(x=3,y=3,color='black',neighbors=board._get_neighbors(x=3,y=3))
    self_capture = board._check_for_capture(potential_move, black.color)
    assert self_capture

def test_check_for_self_capture_single_chain_self_capture_true():
    black = game.Player(color='black', name='Arna')
    white = game.Player(color='white', name='Sean')
    board = game.Board(9, black, white)
    # put some pieces down. Chain of three black set up for self capture
    board.make_move(4, 2, white.color)
    board.make_move(4, 3, white.color)
    board.make_move(4, 4, white.color)
    board.make_move(4, 5, white.color)
    board.make_move(5, 1, white.color)
    board.make_move(5, 6, white.color)
    board.make_move(6, 2, white.color)
    board.make_move(6, 3, white.color)
    board.make_move(6, 4, white.color)
    board.make_move(6, 5, white.color)
    # black pieces
    board.make_move(5, 3, black.color)
    board.make_move(5, 4, black.color)
    board.make_move(5, 5, black.color)
    # board.render()
    potential_move = game.CrossHair(x=5, y=2, color='black', neighbors=board._get_neighbors(x=5,y=2))
    self_capture = board._check_for_capture(potential_move, black.color)
    assert self_capture

def test_for_self_capture_two_chains_self_capture_true():
    black = game.Player(color='black', name='Arna')
    white = game.Player(color='white', name='Sean')
    board = game.Board(9, black, white)
    # put some pieces down. Chain of three black set up for self capture
    board.make_move(4, 2, white.color)
    board.make_move(4, 3, white.color)
    board.make_move(4, 4, white.color)
    board.make_move(4, 5, white.color)
    board.make_move(5, 1, white.color)
    board.make_move(5, 6, white.color)
    board.make_move(6, 2, white.color)
    board.make_move(6, 3, white.color)
    board.make_move(6, 5, white.color)
    board.make_move(7, 3, white.color)
    board.make_move(7, 5, white.color)
    board.make_move(8, 4, white.color)
    # black pieces
    board.make_move(5, 3, black.color)
    board.make_move(5, 4, black.color)
    board.make_move(5, 5, black.color)
    board.make_move(6, 4, black.color)
    board.make_move(7, 4, black.color)
    # board.render()
    potential_move = game.CrossHair(x=5, y=2, color='black', neighbors=board._get_neighbors(x=5,y=2))
    import pdb;pdb.set_trace()
    self_capture = board._check_for_capture(potential_move, black.color)

    assert self_capture

def test_get_opposite_color_white():
    black = game.Player(color='black', name='Arna')
    white = game.Player(color='white', name='Sean')
    board = game.Board(9, black, white)
    color = board._get_opposite_color(white.color)
    assert color == 'black'

def test_get_opposite_color_black():
    black = game.Player(color='black', name='Arna')
    white = game.Player(color='white', name='Sean')
    board = game.Board(9, black, white)
    color = board._get_opposite_color(black.color)
    assert color == 'white'

def test_get_neighbors_corner():
    black = game.Player(color='black', name='Arna')
    white = game.Player(color='white', name='Sean')
    board = game.Board(9, black, white)
    neighbors = board._get_neighbors(0,0)
    assert neighbors['left'] is None
    assert neighbors['bottom'] is None
    assert neighbors['top'] is not None
    assert neighbors['right'] is not None

def test_get_neighbors_edge():
    black = game.Player(color='black', name='Arna')
    white = game.Player(color='white', name='Sean')
    board = game.Board(9, black, white)
    neighbors = board._get_neighbors(0, 7)
    assert neighbors['left'] is None
    assert neighbors['bottom'] is not None
    assert neighbors['top'] is not None
    assert neighbors['right'] is not None

def test_get_neighbors_middle():
    black = game.Player(color='black', name='Arna')
    white = game.Player(color='white', name='Sean')
    board = game.Board(9, black, white)
    neighbors = board._get_neighbors(3, 3)
    assert neighbors['left'] is not None
    assert neighbors['bottom'] is not None
    assert neighbors['top'] is not None
    assert neighbors['right'] is not None