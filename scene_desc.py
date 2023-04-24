from numpy import *
from camera import *

from hittable import *
from sphere import *

from material import *



#---------------World description------------------------------------------
blue_lambert = lambertian(np.array([.8,.8,1]))
ground_mat = lambertian(np.array([.8,1,.7]))
metal_shader = metal(np.array([1,1,1]),roughness=0.2)
glass_shader = dielectric(1.5)

s_ground = sphere(np.array([0,-100.5,-1]),100,ground_mat)
s1 = sphere(np.array([0,0,-1]),0.5,blue_lambert)
s2 = sphere(np.array([-1,0,-1]),0.5,glass_shader)
s22 = sphere(np.array([-1,0,-1]),-0.45,glass_shader)
s3 = sphere(np.array([1,0,-1]),0.5,metal_shader)
WORLD = hittable_list([s1,s2,s22,s3,s_ground])


#---------------Camera description------------------------------------------
aspect_ratio = 16/9
vert_fov = 20#degrees
lookfrom = np.array([3,3,2])
lookat = np.array([0,0,-1])
v_up = np.array([0,1,0])
aperture = 2.0
focal_point = lookat


img_width = 150
img_height = int(img_width/aspect_ratio)

viewport_height = 2
viewport_width = aspect_ratio * viewport_height

SCENE_CAMERA = camera(aspect_ratio=aspect_ratio,vert_fov=vert_fov,lookfrom=lookfrom,lookat=lookat,v_up=v_up,aperture=aperture,focal_point=focal_point)

#---------------Rendering settings------------------------------------------
samples_per_pixel = 3
max_depth = 2
