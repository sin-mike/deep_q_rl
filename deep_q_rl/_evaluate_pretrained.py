__author__ = 'm12sl'
import sys
import os
import logging
import launcher
import run_nips
import cPickle

import simple_experiment
import pipe_ale_interface
import ale_agent

import ale_experiment



def launch_local_nips(args, defaults, description):
    """
    run the evaluation
    """
    logging.basicConfig(level=logging.INFO)
    parameters = launcher.process_args(args, defaults, description)

    if parameters.rom.endswith('.bin'):
        rom = parameters.rom
    else:
        rom = "%s.bin" % parameters.rom
    full_rom_path = os.path.join(defaults.BASE_ROM_PATH, rom)

    ale = pipe_ale_interface.ALEInterface()

    assert parameters.nn_file is not None, "No NN file in input"


    # we should unpickle params for continue learning
    handle = open(parameters.nn_file, 'r')
    network = cPickle.load(handle)
    print 'pre trainted nn'

    agent = ale_agent.NeuralAgent(network,
                                  parameters.epsilon_start,
                                  parameters.epsilon_min,
                                  parameters.epsilon_decay,
                                  parameters.replay_memory_size,
                                  parameters.experiment_prefix,
                                  parameters.replay_start_size,
                                  parameters.update_frequency)

    experiment = simple_experiment.SimpleExperiment(ale, agent)

    experiment.run()

if __name__ == "__main__":
    launch_local_nips(sys.argv[1:], run_nips.Defaults, __doc__)



