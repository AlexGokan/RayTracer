import numpy as np
from vector_operations import *

class ray:
    def __init__(self,origin,dir):
        self.origin = origin
        self.dir = dir

    def at(self,t):
        return self.origin + self.dir*t

    def get_color(self,world,bvh,depth):
        if depth <= 0:
            return np.array([0,0,0])

        hit,record = world.hit(self,0.001,float('inf'))
        bvh_hit,bvh_record = bvh.hit(self,0.001,float('inf'))


        if bvh_hit:
            mat_scat_bool,scattered_ray,attenuation = bvh_record.material.scatter(self,record)
            if mat_scat_bool:
                #any ray is color(this_surface)*incoming ray which we find the below line
                return attenuation * scattered_ray.get_color(world,bvh,depth-1)
            else:
                return np.array([0,0,0])


        unit_dir = unit_vector(self.dir)
        t = 0.5*unit_dir[1] + 1#essentially the y component of our dir vector
        #eturn np.array([1,1,1])*(1-t) + np.array([.5,.7,1])*t#default sky shader
        return np.array([0.8,0.8,0.8])


