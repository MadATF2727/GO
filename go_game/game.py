import argparse
import logging
import os


import matplotlib.pyplot as plt
import numpy as np

THIS_DIR = os.path.dirname(__file__)



def check_size(size):
    size_valid = size in (9, 13, 19)
    if not size_valid:
        logging.error("Invalid board size chosen, please choose from 9, 13 or 19 boxes square")
    return size_valid


def setup_logging():
    LOG_DIR = os.path.join(THIS_DIR, 'logs')
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    logfile_name = os.path.join(LOG_DIR, 'go_game_latest.log')
    logfile_error_name = os.path.join(LOG_DIR, 'go_game_error.log')
    logging.basicConfig(filename=logfile_name, level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    file_handler_error = logging.FileHandler(logfile_error_name, mode='w')
    log_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler_error)

class CrossHair(object):
    def __init__(self, color, x, y, neighbors):
        self.color = color
        self.x = x
        self.y = y
        self.neighbors = neighbors


class Player(object):
    def __init__(self, color=None, name=None):
        self.color = color
        self.name = name
        self.captured = []


class GoGame(object):
    def __init__(self, args):
        self.black = Player(color='black', name=args.black_player_name)
        self.white = Player(color='white', name=args.white_player_name)
        self.board = Board(args.board_size, self.black, self.white)
        # self.board.render()
        # x, y = self.board.get_desired_move(self.black)
        self.board.make_move(3, 3, color='black')
        # just for FB post add a white
        self.board.make_move(7, 2, 'white')
        self.board.render()



class Board(object):
    def __init__(self, size=None, black=None, white=None):
        if size is None:
            self.size = 13
        elif check_size(size):
            self.size = size
        self.grid = self._initialize_liberties_grid()
        self.black = black
        self.white = white
        self.stones = []

    def get_desired_move(self, player):

        prompt = ("{} please enter the x, y location you'd like to play at ").format(player.name)
        xy_str = input(prompt)
        x = int(xy_str.split(',')[0])
        y = int(xy_str.split(',')[1])
        return x, y

    def _check_for_corner(self, x, y):
        return ((x == 0 and y == 0) or (x == 0 and y == self.size - 1)
                or (x == self.size - 1 and y == self.size - 1) or (x == self.size - 1 and y == 0))

    def _check_in_bounds(self, coord):
        return coord - 1 > 0 and coord + 1 < self.size

    def _get_neighbors(self, x, y):
        if self._check_in_bounds(x) and self._check_in_bounds(y):
            return {'left':self.grid[x - 1, y],
                'right':self.grid[x + 1, y],
                'top': self.grid[x, y + 1],
                'bottom':self.grid[x, y - 1]}
        elif self._check_in_bounds(x) and not self._check_in_bounds(y):
            if y - 1 < 0:
                return {'left': self.grid[x - 1, y],
                    'right': self.grid[x + 1, y],
                    'top': self.grid[x, y + 1],
                    'bottom': None}
            elif y + 1 > self.size:
                return {'left': self.grid[x - 1, y],
                        'right': self.grid[x + 1, y],
                        'top': None,
                        'bottom': self.grid[x, y - 1]}
        elif not self._check_in_bounds(x) and self._check_in_bounds(y):
            if x - 1 < 0:
                return {'left': None,
                        'right': self.grid[x + 1, y],
                        'top': self.grid[y + 1, y],
                        'bottom': self.grid[x, y - 1]}
            elif x + 1 > self.size:
                return {'left': self.grid[x - 1, y],
                        'right': None,
                        'top': self.grid[x, y + 1],
                        'bottom': self.grid[x, y - 1]}
        elif not self._check_in_bounds(x) and not self._check_in_bounds(y):
            if x - 1 < 0 and y - 1 < 0:
                # bottom left corner
                return {'left': None,
                        'right': self.grid[x + 1, y],
                        'top': self.grid[x, y + 1],
                        'bottom': None}
            elif x - 1 < 0 and y + 1 > self.size-1:
                # top left corner
                return {'left': None,
                        'right': self.grid[x + 1, y],
                        'top': None,
                        'bottom': self.grid[x, y - 1]}
            elif x + 1 > self.size - 1 and y + 1 > self.size - 1:
                # top right corner
                return {'left': self.grid[x - 1, y],
                        'right': None,
                        'top': None,
                        'bottom': self.grid[x, y - 1]}
            elif x + 1 > self.size - 1 and y + 1 > self.size - 1:
                # bottom right corner
                return {'left': self.grid[x - 1, y],
                        'right': None,
                        'top': self.grid[x, y + 1],
                        'bottom': None}

    def validate_move(self, liberty, player):
        self_capture = self._check_for_self_capture(liberty, player)
        if self_capture:
            print("Sorry, that move is illegal because of self-capture, try again")
            liberty = self.get_desired_move(player)
            self.validate_move(liberty, player)
        pass

    def _check_for_capture(self, crosshair, color):
        capture_flag = False
        same, opposite, empty = self._get_same_opposite_empty(crosshair, color)
        if len(opposite) == 4:
            capture_flag = True
        elif len(opposite) + len(same) == 4:
            capture_list = []
            for key in same:
                self_capture, _ = self._check_chain_in_direction(crosshair, key, color)
                capture_list.append(self_capture)
            if len(capture_list) == len(same):
                capture_flag = True
            else:
                capture_flag = False
        return capture_flag

    def _check_chain_in_direction(self, crosshair, direction, color):
        chain_end = False
        self_capture = False
        crosshair = crosshair.neighbors[direction]
        key_to_expect_in_same = self._get_neighbor_to_expect_on_next(direction)
        while not chain_end:
            same, opposite, empty = self._get_same_opposite_empty(crosshair, color)
            if key_to_expect_in_same in same:
                same.remove(key_to_expect_in_same)
            if empty:
                self_capture = False
                chain_end = True
            elif len(opposite) == 3:
                self_capture = True
                chain_end = True
            else:
                crosshair = crosshair.neighbors[direction]
                self_capture, chain_end = self._check_chain_in_direction(crosshair, direction, color)

        return self_capture, chain_end

    def _get_same_opposite_empty(self, crosshair, color):
        same = self._get_surrounding_liberties_of_one_color(crosshair, color)
        empty = self._get_surrounding_empty_liberties(crosshair)
        opposite = self._get_surrounding_liberties_of_one_color(crosshair, self._get_opposite_color(color))
        return same, opposite, empty

    def _get_neighbor_to_expect_on_next(self, side):
        if side == 'left':
            return 'right'
        elif side == 'right':
            return 'left'
        elif side == 'bottom':
            return 'top'
        elif side == 'top':
            return 'bottom'

    def _get_opposite_color(self, color):
        if color == 'black':
            return 'white'
        else:
            return 'black'

    def _get_surrounding_liberties_of_one_color(self, crosshair, color):
        crosshair.neighbors = self._get_neighbors(crosshair.x, crosshair.y)
        same_color_liberties = []
        for key in crosshair.neighbors.keys():
            this_one = crosshair.neighbors[key]
            if self.grid[this_one.x, this_one.y] is not None:
                if self.grid[this_one.x, this_one.y].color == color:
                    same_color_liberties.append(key)
        return same_color_liberties

    def _get_surrounding_empty_liberties(self, crosshair):
        none_liberties = []
        for key in crosshair.neighbors.keys():
            if crosshair.neighbors[key] is None:
                none_liberties.append(key)
        return none_liberties


    def make_move(self, x, y, player):
        # # make sure there is no piece there and it isn't a corner
        this_liberty = self.grid[x, y]
        # if this_liberty.color is not None or self._check_for_capture(this_liberty, player.color):
        #     print("Illegal move please make another")
        #     x, y = self.get_desired_move(player)
        # else:
        #     capture = self._check_for_capture(this_liberty, self._get_opposite_color(player.color))
        #
        this_liberty.color = player.color
        this_liberty.neighbors = self._get_neighbors(x, y)




    def _initialize_liberties_grid(self):
        self.grid = np.empty((self.size, self.size)).astype(object)
        for x in range(self.size):
            for y in range(self.size):
                # until a stone is played on a spot neighbors are None and color is None
                self.grid[x, y] = CrossHair(x=x, y=y, neighbors=None, color=None)

        return self.grid


    def render(self):
        # 7" ny 7" board
        fig = plt.figure(figsize=[7, 7])
        # pale yellow face
        fig.patch.set_facecolor((1, 1, .8))
        ax = fig.add_subplot(111)
        # draw the grid
        ticks = [str(x) for x in range(1, self.size+1)]
        ax.set_xticks(ticks=range(self.size))
        ax.set_xticklabels(labels=ticks)
        ax.set_yticks(ticks=range(self.size))
        ax.set_yticklabels(labels=ticks)
        for x in range(self.size):
            ax.plot([x, x], [0, self.size-1], 'k')
        for y in range(self.size):
            ax.plot([0, self.size-1], [y, y], 'k')
        # scale the axis area to fill the whole figure
        ax.set_position([0, 0, 1, 1])
        # get rid of axes and everything (the figure background will show through)
        ax.set_axis_off()
        # scale the plot area conveniently (the board is in 0,0, size, size)
        ax.set_xlim(-1, self.size)
        ax.set_ylim(-1, self.size)

        import matplotlib.patches as mpatches
        for x in range(self.size):
            for y in range(self.size):
                this_liberty = self.grid[x,y]
                if this_liberty is not None:
                    if this_liberty.color is not None:
                        if this_liberty.color == 'black':
                            black_stone = mpatches.Circle((0, 0), .45, facecolor='k', edgecolor=(.8, .8, .8, 1),
                                                          linewidth=2, clip_on=False, zorder=10)
                            black_stone.center = (x, y)
                            ax.add_patch(black_stone)
                            # ax.plot(x, y, markersize=30, markeredgecolor=(0,0,0), markerfacecolor='k', markeredgewidth=2)
                        elif this_liberty.color == 'white':
                            white_stone = mpatches.Circle((0, 0), .45, facecolor='w', edgecolor=(.8, .8, .8, 1),
                                                          linewidth=2, clip_on=False, zorder=10)
                            white_stone.center = (x, y)
                            ax.add_patch(white_stone)

        plt.show()

def parse_args():
    desc = 'Go Game! Black player always goes first!'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--black-player-name', required=True, help='Player one name')
    parser.add_argument('--white-player-name', required=True, help='Player two name')
    parser.add_argument('--board-size', required=True, help='Number of squares on each side of board (9, 13 or 19)', type=int, action='store')
    return parser.parse_args()

def check_args(args):
    return args.board_size in (9, 13, 19)

def play_game(args):
    # initialize board
    game = GoGame(args)
    # get first move



if __name__ == "__main__":
    args = parse_args()
    valid_board = check_args(args)
    if valid_board:
        play_game(args)
    else:
        logging.error("Aborting, see prior error message")
