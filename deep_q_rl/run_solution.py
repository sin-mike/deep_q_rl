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
    STEPS_PER_TEST = 1000 # set 0 for no testing

    # ----------------------
    # ALE Parameters
    # ----------------------
    BASE_ROM_PATH = "../roms/"
    ROM = ''
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


def launch_games(args, defaults, description):
    import os
    import pipe_ale_interface
    import logging
    logging.basicConfig(level=logging.INFO)
    import time


    """
    Sequential game starter
    """

    games = [
             ('tutankham', 'experiments/tutankham_07-24-00-58_0p00025_0p99/')
             ,('seaquest', 'experiments/seaquest_07-24-01-05_0p00025_0p99/')
             ,('gopher', 'experiments/gopher_07-24-00-59_0p00025_0p99/')
             ]

    for (rom, folder) in games:
        try: # if one game stops accidentially, it doesn't affect other games

            logging.info('looking for the last network_file_*** in ' + folder)
            lst = os.listdir(folder)
            lst = [f for f in lst if f.startswith('network_file')]
            lstcouples = [f.split('_')[-1] for f in lst]
            numbers = [int(f.split('.')[0]) for f in lstcouples]
            maxnum = max(numbers)
            nn_file = os.path.join(folder,'network_file_'+str(maxnum)+'.pkl')
            logging.info('nn_file '+nn_file)

            # create pipe ALE, which by default is headless
            ale = pipe_ale_interface.PipeALEInterface(rom=rom)

            # specify network file
            defaults.NN_FILE = nn_file
            defaults.ROM = rom

            # launch experiment
            launcher.launch(args, defaults, description, ale)

            # some kind of miss-architecture in ale-socket place
            del ale.sl
            ale.s.close()

            # necessary because of connection refuse :) seems server does not close connection in time
            time.sleep(1)
        except Exception, e:
            logging.error(str(e))


if __name__ == "__main__":
    launch_games(sys.argv[1:], Defaults, __doc__)

