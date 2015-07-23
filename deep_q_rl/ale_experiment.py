"""The ALEExperiment class handles the logic for training a deep
Q-learning agent in the Arcade Learning Environment.

Author: Nathan Sprague

"""
import logging
import numpy as np
import cv2

# Number of rows to crop off the bottom of the (downsampled) screen.
# This is appropriate for breakout, but it may need to be modified
# for other games.
CROP_OFFSET = 8




logger = logging.getLogger("ale_experiment")


class ALEExperiment(object):
    def __init__(self, ale, agent, resized_width, resized_height,
                 resize_method, num_epochs, epoch_length, test_length,
                 death_ends_episode):
        self.ale = ale
        self.agent = agent
        self.num_epochs = num_epochs
        self.epoch_length = epoch_length
        self.test_length = test_length
        self.death_ends_episode = death_ends_episode
        self.min_action_set = ale.getMinimalActionSet() # ale safe
        self.resized_width = resized_width
        self.resized_height = resized_height
        self.resize_method = resize_method
        self.width, self.height = ale.getScreenDims() # ale safe
        self.screenRGB = np.empty((self.height, self.width, 3), dtype=np.uint8)
        self.terminal_lol = False # Most recent episode ended on a loss of life

        # pydevd.settrace('127.0.0.1', port=12344, stdoutToServer=True, stderrToServer=True)

    def run(self):
        """
        Run the desired number of training epochs, a testing epoch
        is conducted after each training epoch.
        """
        for epoch in range(1, self.num_epochs + 1):
            # first train net
            if self.epoch_length > 0:
                self.run_epoch(epoch, self.epoch_length)
                self.agent.finish_epoch(epoch)
            else:
                logging.warning('training skipped')

            # then test it
            if self.test_length > 0:
                self.agent.start_testing()
                self.run_epoch(epoch, self.test_length, True)
                self.agent.finish_testing(epoch)
            else:
                logging.warning('testing skipped')

    def run_epoch(self, epoch, num_steps, testing=False):
        """ Run one 'epoch' of training or testing, where an epoch is defined
        by the number of steps executed.  Prints a progress report after
        every trial

        Arguments:
        epoch - the current epoch number
        num_steps - steps per epoch
        testing - True if this Epoch is used for testing and not training

        """
        steps_left = num_steps
        epiNumber = 0
        while steps_left > 0:
            epiNumber = epiNumber+1
            prefix = "testing" if testing else "training"
            logging.info(prefix +
                         " epoch: " + str(epoch) +
                         " episode: " + str(epiNumber) +
                         " steps_left: " + str(steps_left) +
                         " of " + str(num_steps))
            _, steps_done = self.run_episode(steps_left, testing)

            steps_left -= steps_done


    def run_episode(self, max_steps, testing):
        """Run a single training episode.

        The boolean terminal value returned indicates whether the
        episode ended because the game ended or the agent died (True)
        or because the maximum number of steps was reached (False).
        Currently this value will be ignored.

        Return: (terminal, num_steps)

        """
        self.ale.reset_game() # ale safe

        action = self.agent.start_episode(self.get_image())
        num_steps = 1
        reward = 0
        total_reward = 0
        terminal = False
        while not terminal and num_steps < max_steps:
            reward = self.ale.act(self.min_action_set[action])

            # if reward<0:
            #     reward = reward*100

            total_reward = total_reward + reward
            action = self.agent.step(reward, self.get_image())
            terminal = self.ale.game_over()
            num_steps += 1

        self.agent.end_episode(reward)
        return terminal, num_steps

    def get_image(self):
        return self.ale.get_image()