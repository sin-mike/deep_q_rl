"""The ALEExperiment class handles the logic for training a deep
Q-learning agent in the Arcade Learning Environment.

Author: Nathan Sprague

"""
import logging
import numpy as np
import cv2
import time
import pipe_ale_interface

# Number of rows to crop off the bottom of the (downsampled) screen.
# This is appropriate for breakout, but it may need to be modified
# for other games.
CROP_OFFSET = 8


class Game(object):
    def __init__(self, agent, rom):
        self.agent = agent
        self.rom = rom
        # pydevd.settrace('127.0.0.1', port=12344, stdoutToServer=True, stderrToServer=True)

    def run(self):
        """
        Let our networky win!
        """
        for game in xrange(3):
            logging.info("yet another game")
            self.run_game()

    def run_game(self):
        ale = pipe_ale_interface.ALEInterface(rom=self.rom)
        self.agent.step_counter = 0

        if ale.game_over():
            ale.reset_game()
        else:
            ale.act(0)  # Take a single null action # ale safe

        action = self.agent.start_episode(ale.get_image())


        num_steps = 1
        reward = 0
        terminal = False
        max_steps = 1000
        total_reward = 0
        while not terminal and num_steps < max_steps:
            reward = ale.act(action)
            action = self.agent.step(reward, ale.get_image())

            terminal = ale.game_over()

            num_steps += 1
            total_reward += reward

        logging.info('total_reward: {0}'.format(total_reward))

        del ale.sl
        ale.s.close()


        # necessary because of connection refuse :) seems server does not close connection in time
        time.sleep(1)

