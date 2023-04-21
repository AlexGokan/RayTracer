
import numpy as np
from vector_operations import *
from ray import *

class material:
    def __init__(self):
        raise NotImplementedError()

    def scatter(self,r_in,hit_record):
        raise NotImplementedError();

class lambertian(material):#diffuse
    def __init__(self,color):
        self.albedo = color

    def scatter(self,r_in,hit_record):
        scatter_dir = hit_record.normal + unit_vector(random_vec3())

        if near_zero(scatter_dir):
            scatter_dir = hit_record.normal

        scattered = ray(hit_record.p,scatter_dir)
        attenuation = self.albedo

        return True,scattered,attenuation

class metal(material):
    def __init__(self,color):
        self.albedo = color

    def scatter(self,r_in,hit_record):
        reflected = reflect(unit_vector(r_in.dir),hit_record.normal)
        scattered = ray(hit_record.p,reflected)
        attenuation = self.albedo

        b = np.dot(scattered.dir,hit_record.normal) > 0
        return b,scattered,attenuation