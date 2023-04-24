from vector_operations import *
from ray import *
from header import *
import numpy as np

class camera:
    def __init__(self,aspect_ratio=16/9,
                 vert_fov=90,
                 lookfrom=np.array([-1,0,0]),
                 lookat=np.array([0,0,0]),
                 v_up=np.array([0,1,0]),#v_up describes what direction is "up" for the camera - so you can "tilt your head"
                 aperture=1.0,
                 focal_point=np.array([0,0,0])):

        focus_distance = length(lookfrom-focal_point)

        w = unit_vector(lookfrom-lookat)
        u = unit_vector(np.cross(v_up,w))
        v = unit_vector(np.cross(w,u))




        theta = deg_to_rad(vert_fov)
        h = np.tan(theta/2)

        self.aspect_ratio = aspect_ratio
        self.viewport_height = 2*h

        self.viewport_width = aspect_ratio * self.viewport_height

        self.origin = lookfrom
        self.horizontal = focus_distance *self.viewport_width * u
        self.vertical = focus_distance * self.viewport_height * v
        self.lower_left = self.origin - self.horizontal/2 - self.vertical/2 - focus_distance*w

        self.lens_radius = aperture/2


    def get_ray(self,s,t):
        rd = self.lens_radius * random_vec2_in_unit_disk()
        offset = s*rd[0] + t*rd[1]

        return ray(self.origin + offset,self.lower_left + self.horizontal*s + self.vertical*t - self.origin)