"""The SimpleExperiment class handles the logic for evaluation in DeepHackathone.

Author: m12sl

"""
import logging
import numpy as np
import cv2

# Number of rows to crop off the bottom of the (downsampled) screen.
# This is appropriate for breakout, but it may need to be modified
# for other games.
CROP_OFFSET = 8


class SimpleExperiment(object):
    def __init__(self, ale, agent):
        self.ale = ale
        self.agent = agent

    def run(self):
        """
        Run the desired number of training epochs, a testing epoch
        is conducted after each training epoch.
        """
        print 'JUST RUN'

        screen = self.ale.act(0)
        action = self.agent.start_episode(screen)
        print action

        # num_steps = 1
        # reward = 0
        # terminal = False
        # while not terminal and num_steps < max_steps:
        #     reward = self.ale.act(self.min_action_set[action])
        #     action = self.agent.step(reward, self.get_image())
        #     self.terminal_lol = (self.death_ends_episode and not testing and
        #                          self.ale.lives() < start_lives)
        #     terminal = self.ale.game_over() or self.terminal_lol
        #     num_steps += 1
        #
        # self.agent.end_episode(reward)
        # return terminal, num_steps

    #
    # def run_epoch(self, epoch, num_steps, testing=True):
    #     """ Run evaluation epoch.
    #
    #     Arguments:
    #     epoch - the current epoch number
    #     num_steps - steps per epoch
    #     testing - True if this Epoch is used for testing and not training
    #     """
    #     self.terminal_lol = False # Make sure each epoch starts with a reset.
    #     steps_left = num_steps
    #     while steps_left > 0:
    #         prefix = "evaluation"
    #         logging.info(prefix + " epoch: " + str(epoch) + " steps_left: " +
    #                      str(steps_left))
    #         _, num_steps = self.run_episode(steps_left, testing)
    #
    #         steps_left -= num_steps
    #
    #
    # def run_episode(self, max_steps, testing):
    #     """Run a single evaluation.
    #
    #     The boolean terminal value returned indicates whether the
    #     episode ended because the game ended or the agent died (True)
    #     or because the maximum number of steps was reached (False).
    #     Currently this value will be ignored.
    #
    #     Return: (terminal, num_steps)
    #
    #     """
    #
    #     action = self.agent.start_episode(self.get_image())
    #     num_steps = 1
    #     reward = 0
    #     terminal = False
    #     while not terminal and num_steps < max_steps:
    #         reward = self.ale.act(self.min_action_set[action])
    #         action = self.agent.step(reward, self.get_image())
    #         self.terminal_lol = (self.death_ends_episode and not testing and
    #                              self.ale.lives() < start_lives)
    #         terminal = self.ale.game_over() or self.terminal_lol
    #         num_steps += 1
    #
    #     self.agent.end_episode(reward)
    #     return terminal, num_steps
    #
    #
    # def get_image(self):
    #     """ Get a screen image from ale and rescale appropriately. """
    #
    #     # convert to greyscale
    #     self.ale.getScreenRGB(self.screenRGB)
    #
    #     greyscaled = cv2.cvtColor(self.screenRGB, cv2.COLOR_RGB2GRAY)
    #
    #     if self.resize_method == 'crop':
    #         # resize keeping aspect ratio
    #         resize_height = int(round(
    #             float(self.height) * self.resized_width / self.width))
    #
    #         resized = cv2.resize(greyscaled,
    #                              (self.resized_width, resize_height),
    #                              interpolation=cv2.INTER_LINEAR)
    #
    #         # Crop the part we want
    #         crop_y_cutoff = resize_height - CROP_OFFSET - self.resized_height
    #         cropped = resized[crop_y_cutoff:
    #                           crop_y_cutoff + self.resized_height, :]
    #
    #         return cropped
    #     elif self.resize_method == 'scale':
    #         return cv2.resize(greyscaled,
    #                           (self.resized_width, self.resized_height),
    #                           interpolation=cv2.INTER_LINEAR)
    #     else:
    #         raise ValueError('Unrecognized image resize method.')
