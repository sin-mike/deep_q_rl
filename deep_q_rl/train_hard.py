#! /usr/bin/env python
"""
Execute a training run of deep-Q-Leaning with parameters that
are consistent with:

Human-level control through deep reinforcement learning.
Nature, 518(7540):529-533, February 2015

"""

import logging
import os
import sys

import custom_ale_interface
import pipe_ale_interface
import q_network
import cPickle

import ale_experiment
import ale_agent
from launcher import process_args


class Defaults:
    STEPS_PER_EPOCH = 11000  # set 0 for no training
    EPOCHS = 20
    STEPS_PER_TEST = 1100  # set 0 for no testing

    BASE_ROM_PATH = "../roms/"
    ROM = 'breakout.bin'
    FRAME_SKIP = 4

    UPDATE_RULE = 'deepmind_rmsprop'
    BATCH_ACCUMULATOR = 'sum'
    LEARNING_RATE = .00025
    DISCOUNT = .99
    RMS_DECAY = .95  # (Rho)
    RMS_EPSILON = .01
    MOMENTUM = 0
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

    INTERFACE = 'custom'


def launch_train(args, defaults, description):
    experiment_dir = 'experiments'

    logging.basicConfig(level=logging.INFO)
    parameters = process_args(args, defaults, description)

    if parameters.rom.endswith('.bin'):
        rom = parameters.rom
    else:
        rom = "%s.bin" % parameters.rom
    full_rom_path = os.path.abspath(os.path.join(defaults.BASE_ROM_PATH, rom))

    num_actions = 18

    if parameters.nn_file is None:
        logging.info('generating network from scratch')
        network = q_network.DeepQLearner(defaults.RESIZED_WIDTH,
                                         defaults.RESIZED_HEIGHT,
                                         num_actions,
                                         parameters.phi_length,
                                         parameters.discount,
                                         parameters.learning_rate,
                                         parameters.rms_decay,
                                         parameters.rms_epsilon,
                                         parameters.momentum,
                                         parameters.freeze_interval,
                                         parameters.batch_size,
                                         parameters.network_type,
                                         parameters.update_rule,
                                         parameters.batch_accumulator)
    else:
        nn_file = os.path.abspath(parameters.nn_file)
        logging.info('loading network from ' + nn_file)
        with open(nn_file, 'r') as handle:
            network = cPickle.load(handle)
            logging.info('network loaded')
            # nasty bug with discount parameter, sometimes it is not saved
            if not network.__dict__.get('discount', None):
                network.discount = parameters.discount

    if parameters.pipe_interface:
        logging.info('Use pipe_interface')
        ale = pipe_ale_interface.PipeALEInterface(rom=parameters.rom)
    else:
        logging.info('Use custom interface')
        ale = custom_ale_interface.CustomALEInterface(rom=parameters.rom,
                                                      display_screen=parameters.display_screen)





        agent = ale_agent.NeuralAgent(network,
                                      parameters.epsilon_start,
                                      parameters.epsilon_min,
                                      parameters.epsilon_decay,
                                      parameters.replay_memory_size,
                                      parameters.experiment_prefix,
                                      parameters.replay_start_size,
                                      parameters.update_frequency,
                                      experiment_dir)

        experiment = ale_experiment.ALEExperiment(ale, agent,
                                                  defaults.RESIZED_WIDTH,
                                                  defaults.RESIZED_HEIGHT,
                                                  parameters.resize_method,
                                                  parameters.epochs,
                                                  parameters.steps_per_epoch,
                                                  parameters.steps_per_test,
                                                  parameters.death_ends_episode)

        experiment.run()


if __name__ == "__main__":
    launch_train(sys.argv[1:], Defaults, __doc__)
