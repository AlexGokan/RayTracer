import copy

import numpy as np
from axis_aligned_bb import *
#from vec3 import *
from copy import *

class hit_record:
    def __init__(self,p,normal,t):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = None
        self.material = None

    def set_face_normal(self,r,outward_normal):
        self.front_face = np.dot(r.dir,outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = outward_normal * -1

class hittable:
    def __init__(self):
        raise NotImplementedError()#need to be implemented by the subclass

    def hit(self,r,t_min,t_max):
        raise NotImplementedError()#need to be implemented by the subclass

    def bounding_box(self,t0,t1):
        raise NotImplementedError()#need to be implemented by the subclass

class hittable_list(hittable):
    def __init__(self,objects):
        self.objects = objects

    def hit(self,r,t_min,t_max):
        hit_anything = False
        closest_so_far = t_max
        rec = hit_record(None,None,None)
        for h in self.objects:
            if isinstance(h,list):
                h = hittable_list(h)
            hit,temp_rec = h.hit(r,t_min,closest_so_far)
            if hit:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec
        return hit_anything,rec

    def bounding_box(self,t0,t1):
        if len(self.objects) == 0:
            return False,None

        temp_box = AABB()
        output_box = AABB()
        first_box = True

        for object in self.objects:
            bb_bool,temp_box = object.bounding_box(t0,t1)
            if not bb_bool:
                return False,None
            output_box = temp_box if first_box else surrounding_box(output_box,temp_box)

        return True,output_box


class BVH_node(hittable):

    def __init__(self,src_objects,t0,t1):
        self.src_objects = src_objects
        self.start = 0
        self.end = len(src_objects)
        self.t0 = t0
        self.t1 = t1

    def hit(self,r,t_min,t_max):
        pass

    def bounding_box(self,t0,t1):
        pass

