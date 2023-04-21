
from hittable import *
#from vec3 import *
from vector_operations import *
import numpy as np

class sphere(hittable):
    def __init__(self,center,radius,material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self,r,t_min,t_max):
        oc = r.origin - self.center
        a = length_squared(r.dir)
        half_b = np.dot(oc,r.dir)
        c = length_squared(oc) - self.radius*self.radius

        disc = half_b*half_b - a*c
        if disc<0:
            return False,None
        sqrtd = np.sqrt(disc)

        root = (-half_b - sqrtd) / a
        if root<t_min or t_max<root:
            root = (-half_b+sqrtd)/a
            if root<t_min or t_max<root:
                return False,None

        rec = hit_record(None,None,None)
        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p-self.center)/self.radius
        rec.set_face_normal(r,outward_normal)
        rec.material = self.material

        return True,rec
