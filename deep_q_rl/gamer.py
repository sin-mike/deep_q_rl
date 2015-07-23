"""The ALEExperiment class handles the logic for training a deep
Q-learning agent in the Arcade Learning Environment.

Author: Nathan Sprague

"""
import logging
import numpy as np
import cv2
import time
import pipe_ale_interface
import custom_ale_interface

# Number of rows to crop off the bottom of the (downsampled) screen.
# This is appropriate for breakout, but it may need to be modified
# for other games.
CROP_OFFSET = 8

logger = logging.getLogger("gamer")


class Game(object):
    def __init__(self, agent, rom, repeats=3):
        self.agent = agent
        self.rom = rom
        self.repeats = repeats
        # pydevd.settrace('127.0.0.1', port=12344, stdoutToServer=True, stderrToServer=True)

    def run(self):
        """
        Let our networky win!
        There will be 30 repeats as far as I know at 23 Jul 04:00
        """
        for game in xrange(self.repeats):
            logging.info("yet another game")
            try:
                self.run_game()
            except Exception, err:
                logging.error(err)

    def run_game(self):
        # You may change interface for fit usage
        ale = pipe_ale_interface.PipeALEInterface(rom=self.rom)
        # ale = custom_ale_interface.SemiALEInterface(rom=self.rom)
        self.agent.step_counter = 0

        if ale.game_over():
            ale.reset_game()
        else:
            ale.act(0)

        # todo: inspect it
        # it is necessary for correct agent initialization

        action = self.agent.start_episode(ale.get_image())



        num_steps = 1
        total_reward = 0
        while not ale.game_over():
            reward = ale.act(action)
            action = self.agent.step(reward, ale.get_image())

            num_steps += 1
            total_reward += reward

        logging.info('steps:{0:<5} total_reward: {1:<5}'.format(num_steps, total_reward))

        # some kind of miss-architecture in ale-socket place
        if isinstance(ale, pipe_ale_interface.PipeALEInterface):
            del ale.sl
            ale.s.close()

            # necessary because of connection refuse :) seems server does not close connection in time
            time.sleep(1)

