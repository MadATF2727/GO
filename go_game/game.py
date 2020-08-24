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

class Liberty(object):
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
        self.board = Board(args.board_size)
        self.black = Player(color='black', name=args.black_player_name)
        self.white = Player(color='white', name=args.white_player_name)
        self.board.render()
        prompt= ("{} please enter the x, y location you'd like to play at ").format(self.black.name)
        xy_str = input(prompt)
        x = int(xy_str.split(',')[0])
        y = int(xy_str.split(',')[1])
        self.board.make_move(x, y, color='black')
        self.board.render()



class Board(object):
    def __init__(self, size=None):
        if size is None:
            self.size = 13
        elif check_size(size):
            self.size = size
        self.grid = self._initialize_liberties_grid()
        self.stones = []

    def _check_for_corner(self, x, y):
        return ((x == 0 and y == 0) or (x == 0 and y == self.size - 1)
                or (x == self.size - 1 and y == self.size - 1) or (x == self.size - 1 and y == 0))

    def _get_neighbors(self, x, y):
        # return neighbors in clockwise order starting from the left
        return [self.grid[x - 1, y], self.grid[y + 1, y], self.grid[x + 1, y],
                self.grid[y - 1, x]]

    def validate_move(self, liberty, color):
        # make sure no self-capture and no piece already there
        neighbor_color_match =np.array([n.color!=color for n in liberty.neighbors])
        if neighbor_color_match.all():
            pass


    def _get_board_state_at_liberty(self, liberty):
        return self.grid[liberty.x, liberty.y]


    def _check_for_capture(self, neighbors):
        # neighbors all full with the same color (opposite to the piece in question)
        # the piece is captured
        pass


    def make_move(self, x, y, color):
        # make sure there is no piece there and it isn't a corner
        this_liberty = self.grid[x, y]
        if this_liberty.color is None and not self._check_for_corner(x, y):
            this_liberty.neighbors = self._get_neighbors(x, y)
            # see if all are occupied
            this_liberty.color = color


    def _initialize_liberties_grid(self):
        self.grid = np.empty((self.size, self.size)).astype(object)
        for x in range(self.size):
            for y in range(self.size):
                if not self._check_for_corner(x, y):
                    # until a stone is played on a spot neighbors are None and color is None
                    self.grid[x, y] = Liberty(x=x, y=y, neighbors=None, color=None)
                else:
                    self.grid[x, y] = None
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
