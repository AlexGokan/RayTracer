import numpy as np


class ray:
    def __init__(self,origin,dir):
        self.origin = origin
        self.dir = dir

    def origin(self):
        return self.origin

    def dir(self):
        return self.dir

    def at(self,t):
        return self.origin + self.dir*t


