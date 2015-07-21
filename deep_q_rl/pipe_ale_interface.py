__author__ = 'm12sl'
# ale_python_interface.py
# Author: Ben Goodrich
# This directly implements a python version of the arcade learning
# environment interface.

import numpy as np
import os
import sys
import socket

import re

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
            if pos != -1 :
                pos += len(self.buff)
            self.buff = self.buff + data
        out = self.buff[:pos+1]
        self.buff = self.buff[pos+1:]
        return out


class PipeInterface(object):
    def __init__(self):
        HOST = 'localhost'
        PORT = 1567
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        login = 'test'
        pwd = 'test12'
        rom = 'gopher'

        # send auth
        s.send("%s,%s,%s\n"%(login, pwd, rom))


        head = s.recv(1024)
        m = re.match(r'(\d{3})\-(\d{3})', head)
        if not m:
          sys.stderr.write("bad FIFO header: [%s]"%head)
          sys.exit(1)

        width = int(m.group(1))
        height = int(m.group(2))
        ssz = width*height

        self.width = width
        self.height = height
        self.ssz = ssz


        print "IN:", head
        s.send("1,0,0,1\n")

        sl = SockLines(s, ssz)

        self.s = s
        self.sl = sl

    def act(self, action):
        self.s.send("%d,18\n" % action)
        data = self.sl.get_line()
        (screen_str, episode_str, delme) = data.split(":", 2)
        print screen_str, episode_str
        return screen_str

    def game_over(self):
        return "is the game over ? oo"

    def reset_game(self):
        print "try to reset game"

    def getLegalActionSet(self):
        return 'get legal actions'

    def getMinimalActionSet(self):
        return 'get minimal actions'

    def getFrameNumber(self):
        return 'get frame number'

    def lives(self):
        return 'lives'

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

