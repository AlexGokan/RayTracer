import copy

from vec3 import *
from copy import *

class hit_record:
    def __init__(self,p,normal,t):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = None

    def set_face_normal(self,r,outward_normal):
        self.front_face = dot(r.dir,outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = outward_normal * -1

class hittable:
    def __init__(self):
        raise NotImplementedError()#need to be implemented by the subclass

    def hit(self,r,t_min,t_max):
        raise NotImplementedError()#need to be implemented by the subclass

class hittable_list(hittable):
    def __init__(self,objects):
        self.objects = objects

    def hit(self,r,t_min,t_max):
        hit_anything = False
        closest_so_far = t_max
        for h in self.objects:
            hit,rec = h.hit(r,t_min,closest_so_far)
            if hit:
                hit_anything = True
                closest_so_far = rec.t
        return hit_anything,rec