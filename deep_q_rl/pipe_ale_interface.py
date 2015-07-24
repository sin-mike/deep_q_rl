__author__ = 'm12sl'
# ale_python_interface.py
# Author: Ben Goodrich
# This directly implements a python version of the arcade learning
# environment interface.

import numpy as np
import os
import sys
import socket
import logging
import re
import codecs
import cv2

CROP_OFFSET = 8

logger = logging.getLogger('pipe_ale_interface')


class SockLines(object):
    def __init__(self, s, ssz):
        self.s = s
        self.buff = ''
        self.ssz = ssz

    def get_line(self):
        pos = self.buff.find('\n')
        while pos == -1:
            data = self.s.recv(self.ssz * 2 + 10)
            pos = data.find('\n')
            if pos != -1:
                pos += len(self.buff)
            self.buff = self.buff + data
        out = self.buff[:pos + 1]
        self.buff = self.buff[pos + 1:]
        return out


class PipeALEInterface(object):
    def __init__(self,
                 # host='localhost',
                 # port=1567,
                 # login='test',
                 # pwd='test12',
                 host='52.8.225.234',
                 port=17006,
                 login='team_6',
                 pwd='Ly2vyA',
                 rom=None):

        if rom is None:
            raise Exception('rom must be specified')

        self.resize_method = 'crop'
        self.resized_width = 84
        self.resized_height = 84

        self._isdie = False
        self._isterminate = False

        HOST = host
        PORT = port

        logging.warning('connecting to socket')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST, PORT))
            logging.warning('connected!')
        except Exception, err:
            print err
            raise Exception('SOCKET ERROR')

        self.s = s

        self.auth(login, pwd, rom)

        self.handshake()

        # self.reset_game()

    def auth(self, login, pwd, rom):
        # send auth
        self.s.send("%s,%s,%s\n" % (login, pwd, rom))

    def handshake(self):
        head = self.s.recv(1024)
        m = re.match(r'(\d{3})\-(\d{3})', head)
        if not m:
            sys.stderr.write("bad FIFO header: [%s]" % head)
            sys.exit(1)

        width = int(m.group(1))
        height = int(m.group(2))
        ssz = width * height

        self.width = width
        self.height = height
        self.ssz = ssz

        logging.info('handshake: ' + str(head))
        self.s.send("1,0,0,1\n")

        sl = SockLines(self.s, ssz)

        self.sl = sl

    def _unhex(self, data):
        byte_str = codecs.decode(data, 'hex_codec')
        return np.frombuffer(byte_str, dtype='uint8').reshape((self.height, self.width))

    def _resized(self, data):
        greyscaled = data
        if self.resize_method == 'crop':
            # resize keeping aspect ratio
            resize_height = int(round(
                float(self.height) * self.resized_width / self.width))

            resized = cv2.resize(greyscaled,
                                 (self.resized_width, resize_height),
                                 interpolation=cv2.INTER_LINEAR)

            # Crop the part we want
            crop_y_cutoff = resize_height - CROP_OFFSET - self.resized_height
            cropped = resized[crop_y_cutoff:
                              crop_y_cutoff + self.resized_height, :]

            return cropped
        elif self.resize_method == 'scale':
            return cv2.resize(greyscaled,
                              (self.resized_width, self.resized_height),
                              interpolation=cv2.INTER_LINEAR)
        else:
            raise ValueError('Unrecognized image resize method.')

    def act(self, action):
        self.s.send("%d,18\n" % action)
        data = self.sl.get_line()

        if len(data) < 10:
            if data.startswith('DIE'):
                self._isdie = True
            logging.warning(data)
            return -1
        else:
            (screen_str, episode_str, delme) = data.split(":", 2)

            temp = episode_str.split(',')
            terminate = int(temp[0])

            reward = int(temp[1])

            if terminate:
                logging.warning('terminate')
                # self.s.send("45,18\n")
                # todo: refactor this strange thing. DIE and termination may have difference
                self._isterminate = True
                self._isdie = True

            self._img, self._reward = self._resized(self._unhex(screen_str)), reward
            return reward

    def get_image(self):
        return self._img

    def game_over(self):
        return self._isdie

    def reset_game(self):
        self._isdie = False
        self._isterminate = False
        self.s.send("45,18\n")
        data = self.sl.get_line()
        (screen_str, episode_str, delme) = data.split(":", 2)

        temp = episode_str.split(',')
        terminate = int(temp[0])

        reward = int(temp[1])
        self._img, self._reward = self._resized(self._unhex(screen_str)), reward

    def getLegalActionSet(self):
        return np.arange(18, dtype='int32')

    def getMinimalActionSet(self):
        return self.getLegalActionSet()

    def getFrameNumber(self):
        return 'get frame number'

    def lives(self):
        # todo: must read from rom start lives
        logging.error('LIVES not available in FIFO')
        return 0

    def getScreenDims(self):
        """returns a tuple that contains (screen_width, screen_height)
        """
        return (self.width, self.height)
        #
        #
        # def getScreen(self, screen_data=None):
        #     """This function fills screen_data with the RAW Pixel data
        #     screen_data MUST be a numpy array of uint8/int8. This could be initialized like so:
        #     screen_data = np.empty(w*h, dtype=np.uint8)
        #     Notice,  it must be width*height in size also
        #     If it is None,  then this function will initialize it
        #     Note: This is the raw pixel values from the atari,  before any RGB palette transformation takes place
        #     """
        #     if(screen_data is None):
        #         width = ale_lib.getScreenWidth(self.obj)
        #         height = ale_lib.getScreenHeight(self.obj)
        #         screen_data = np.zeros(width*height, dtype=np.uint8)
        #     ale_lib.getScreen(self.obj, as_ctypes(screen_data))
        #     return screen_data
        #
        # def getScreenRGB(self, screen_data=None):
        #     """This function fills screen_data with the data
        #     screen_data MUST be a numpy array of uint8. This can be initialized like so:
        #     screen_data = np.empty((height,width,3), dtype=np.uint8)
        #     If it is None,  then this function will initialize it.
        #     """
        #     if(screen_data is None):
        #         width = ale_lib.getScreenWidth(self.obj)
        #         height = ale_lib.getScreenHeight(self.obj)
        #         screen_data = np.empty((height, width,3), dtype=np.uint8)
        #     ale_lib.getScreenRGB(self.obj, as_ctypes(screen_data[:]))
        #     return screen_data
