__author__ = 'm12sl'
"""
Custom ALE python interface with marked non-FIFO methods
Two purposes:
    1. Make Training as fast as with vanilla ALEInterface
    2. Refactor all processes with DATA_TRANSFER-agnostic methods

"""
import numpy as np

import logging
import cv2

CROP_OFFSET = 8
import ale_python_interface


def nonfifo(fn):
    """
    Just a dev decorator
    """
    def wrapped(*args):
        logging.warning('non-FIFO action ' + str(fn))
        return fn(args)
    return wrapped


class SemiALEInterface(ale_python_interface.ALEInterface):
    def __init__(self):
        super(SemiALEInterface, self).__init__()
        self.width, self.height = self.getScreenDims()
        self.resize_method = 'crop'
        self.resized_width = 84
        self.resized_height = 84

    @nonfifo
    def getString(self, key):
        return super(SemiALEInterface, self).getString(key)

    @nonfifo
    def getInt(self, key):
        return super(SemiALEInterface, self).getInt(key)

    @nonfifo
    def getBool(self, key):
        return super(SemiALEInterface, self).getBool(key)

    @nonfifo
    def getFloat(self, key):
        return super(SemiALEInterface, self).getFloat(key)

    @nonfifo
    def setString(self, key, value):
        super(SemiALEInterface, self).setString(key, value)

    @nonfifo
    def setInt(self, key, value):
        super(SemiALEInterface, self).setInt(key, value)

    @nonfifo
    def setBool(self, key, value):
        super(SemiALEInterface, self).setBool(key, value)

    @nonfifo
    def setFloat(self, key, value):
        super(SemiALEInterface, self).setFloat(key, value)

    @nonfifo
    def loadROM(self, rom_file):
        super(SemiALEInterface, self).loadROM(rom_file)

    def act(self, action):
        return super(SemiALEInterface, self).act(int(action))

    def game_over(self):
        return super(SemiALEInterface, self).game_over()

    def reset_game(self):
        super(SemiALEInterface, self).reset_game()

    @nonfifo
    def getLegalActionSet(self):
        return super(SemiALEInterface, self).getLegalActionSet()

    @nonfifo
    def getMinimalActionSet(self):
        return super(SemiALEInterface, self).getMinimalActionSet()

    @nonfifo
    def getFrameNumber(self):
        return super(SemiALEInterface, self).getFrameNumber()

    @nonfifo
    def lives(self):
        return super(SemiALEInterface, self).lives()

    @nonfifo
    def getEpisodeFrameNumber(self):
        return super(SemiALEInterface, self).getEpisodeFrameNumber()

    def getScreenDims(self):
        """returns a tuple that contains (screen_width, screen_height)
        """
        return super(SemiALEInterface, self).getScreenDims()

    def getScreen(self, screen_data=None):
        """This function fills screen_data with the RAW Pixel data
        screen_data MUST be a numpy array of uint8/int8. This could be initialized like so:
        screen_data = np.empty(w*h, dtype=np.uint8)
        Notice,  it must be width*height in size also
        If it is None,  then this function will initialize it
        Note: This is the raw pixel values from the atari,  before any RGB palette transformation takes place
        """
        return super(SemiALEInterface, self).getScreen()
        # if(screen_data is None):
        #     width = ale_lib.getScreenWidth(self.obj)
        #     height = ale_lib.getScreenHeight(self.obj)
        #     screen_data = np.zeros(width*height, dtype=np.uint8)
        # ale_lib.getScreen(self.obj, as_ctypes(screen_data))
        # return screen_data

    def get_image(self):
        img = self.getScreen().reshape((self.height, self.width))
        return self._resized(img)

    @nonfifo
    def getScreenRGB(self, screen_data=None):
        """This function fills screen_data with the data
        screen_data MUST be a numpy array of uint8. This can be initialized like so:
        screen_data = np.empty((height,width,3), dtype=np.uint8)
        If it is None,  then this function will initialize it.
        """
        return super(SemiALEInterface, self).getScreenRGB()

    @nonfifo
    def getRAMSize(self):
        return super(SemiALEInterface, self).getRAMSize()

    @nonfifo
    def getRAM(self, ram=None):
        """This function grabs the atari RAM.
        ram MUST be a numpy array of uint8/int8. This can be initialized like so:
        ram = np.array(ram_size, dtype=uint8)
        Notice: It must be ram_size where ram_size can be retrieved via the getRAMSize function.
        If it is None,  then this function will initialize it.
        """
        return super(SemiALEInterface, self).getRAM()

    @nonfifo
    def saveScreenPNG(self, filename):
        return super(SemiALEInterface, self).saveScreenPNG(filename)

    @nonfifo
    def saveState(self):
        return super(SemiALEInterface, self).saveState()

    @nonfifo
    def loadState(self):
        return super(SemiALEInterface, self).loadState()

    def __del__(self):
        super(SemiALEInterface, self).__del__()

    def _resized(self, data):
        greyscaled = data
        if self.resize_method == 'crop':
            # resize keeping aspect ratio
            resize_height = int(round(
                float(self.height) * self.resized_width / self.width))

            resized = cv2.resize(greyscaled,
                                 (self.resized_width, self.resized_height),
                                 interpolation=cv2.INTER_LINEAR)

            # Crop the part we want
            crop_y_cutoff = self.resized_height - CROP_OFFSET - self.resized_height
            cropped = resized[crop_y_cutoff: crop_y_cutoff + self.resized_height, :]

            return cropped
        elif self.resize_method == 'scale':
            return cv2.resize(greyscaled, (self.resized_width, self.resized_height),
                              interpolation=cv2.INTER_LINEAR)
        else:
            raise ValueError('Unrecognized image resize method.')
