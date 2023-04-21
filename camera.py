#from vec3 import *
from ray import *
from header import *
import numpy as np

class camera:
    def __init__(self,aspect_ratio=16/9,
                 viewport_height=2.0,
                 focal_length=1.0):

        self.aspect_ratio = aspect_ratio
        self.viewport_height = viewport_height
        self.focal_length = focal_length

        self.viewport_width = int(aspect_ratio * viewport_height)
        self.origin = np.array([0,0,0])
        self.horizontal = np.array([self.viewport_width,0,0])
        self.vertical = np.array([0,viewport_height,0])
        self.lower_left = self.origin - self.horizontal/2 - self.vertical/2 - np.array([0,0,self.focal_length])

    def get_ray(self,u,v):
        return ray(self.origin,self.lower_left + self.horizontal*u + self.vertical*v - self.origin)