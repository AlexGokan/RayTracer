
from hittable import *
from vec3 import *

class sphere(hittable):
    def __init__(self,center,radius):
        self.center = center
        self.radius = radius

    def hit(self,r,t_min,t_max,rec):
        oc = r.origin - self.center
        a = r.dir.length_squared()
        half_b = dot(oc,r.dir)
        c = oc.length_squared() - self.radius*self.radius

        disc = half_b*half_b - a*c
        if disc<0:
            return False,rec
        sqrtd = np.sqrt(disc)

        root = (-half_b - sqrtd) / a
        if root<t_min or t_max<root:
            root = (-half_b+sqrtd)/a
            if root<t_min or t_max<root:
                return False,rec

        rec.t = root
        rec.p = r.at(rec.t)
        rec.normal = (rec.p-self.center)/self.radius

        return True,rec
