
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
    def __init__(self,color,roughness=0):
        self.albedo = color
        self.roughness = roughness

    def scatter(self,r_in,hit_record):
        reflected = reflect(unit_vector(r_in.dir),hit_record.normal)
        scattered = ray(hit_record.p,reflected + self.roughness*random_vec3_in_unit_sphere())
        attenuation = self.albedo

        b = np.dot(scattered.dir,hit_record.normal) > 0
        return b,scattered,attenuation

class dielectric(material):#refract
    def __init__(self,ior):
        self.ior = ior


    def reflectance(self,cosine,ref_idx):#schlick approximation
        r0 = (1-ref_idx) / (1+ref_idx)
        r0 = r0*r0
        return r0 + (1-r0)*np.power((1-cosine),5)

    def scatter(self,r_in,hit_record):
        attenuation = np.array([1,1,1])
        refraction_ratio = 1.0/self.ior if hit_record.front_face else self.ior

        unit_dir = unit_vector(r_in.dir)
        cos_theta = min(np.dot(-unit_dir,hit_record.normal),1.0)
        sin_theta = np.sqrt(1-cos_theta*cos_theta)

        cant_refract = refraction_ratio * sin_theta > 1.0

        if cant_refract or self.reflectance(cos_theta,refraction_ratio) > np.random.uniform():
            direction = reflect(unit_dir,hit_record.normal)
        else:
            direction = refract(unit_dir,hit_record.normal,refraction_ratio)


        scattered = ray(hit_record.p,direction)

        return True,scattered,attenuation