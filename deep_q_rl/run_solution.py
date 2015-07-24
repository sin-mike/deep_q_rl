__author__ = 'm12sl'

"""
DeepHack.Game Solution program
run:
python run_solution.py --nn-file path/to/nn_file.pkl --rom rom_name
"""

import launcher
import sys

class Defaults:
    # ----------------------
    # Experiment Parameters
    # ----------------------
    STEPS_PER_EPOCH = 0
    EPOCHS = 1
    STEPS_PER_TEST = 540100 # set 0 for no testing

    # ----------------------
    # ALE Parameters
    # ----------------------
    BASE_ROM_PATH = "../roms/"
    ROM = 'breakout.bin'
    FRAME_SKIP = 1

    # ----------------------
    # Agent/Network parameters:
    # ----------------------
    NN_FILE = None # starting network
    UPDATE_RULE = 'deepmind_rmsprop'
    BATCH_ACCUMULATOR = 'sum'
    LEARNING_RATE = .00025
    DISCOUNT = .99
    RMS_DECAY = .95 # (Rho)
    RMS_EPSILON = .01
    MOMENTUM = 0 # Note that the "momentum" value mentioned in the Nature
                 # paper is not used in the same way as a traditional momentum
                 # term.  It is used to track gradient for the purpose of
                 # estimating the standard deviation. This package uses
                 # rho/RMS_DECAY to track both the history of the gradient
                 # and the squared gradient.
    EPSILON_START = 1.0
    EPSILON_MIN = .1
    EPSILON_DECAY = 1000000
    PHI_LENGTH = 4
    UPDATE_FREQUENCY = 4
    REPLAY_MEMORY_SIZE = 1000000
    BATCH_SIZE = 32
    NETWORK_TYPE = "nature_dnn"
    FREEZE_INTERVAL = 10000
    REPLAY_START_SIZE = 50000
    RESIZE_METHOD = 'scale'
    RESIZED_WIDTH = 84
    RESIZED_HEIGHT = 84
    DEATH_ENDS_EPISODE = 'true'

if __name__ == "__main__":
    launcher.launch_games(sys.argv[1:], Defaults, __doc__)

