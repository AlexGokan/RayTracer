from numpy import *
from numpy import array as npa
from camera import *

from hittable import *
from sphere import *

from material import *
from bvh import BVH_node


#---------------World description------------------------------------------
world_list = []

random.seed(0)

ground_mat = lambertian(npa([.5,.5,.5]))
ground_sphere = sphere(npa([0,-1000,0]),1000,ground_mat)
world_list.append(ground_sphere)


for a in range(-2,2):
    for b in range(-2,2):
        mat_choice = np.random.uniform(0,1)

        mult = 0.8

        center = npa([a + mult*np.random.uniform(-1,1),0.2,b + mult*np.random.uniform(-1,1)])
        center = center + npa([4,0,0])

        if mat_choice < 0.75:
            color = random_vec3(0,1)
            sphere_mat = lambertian(color)
        else:
            color = random_vec3(0,1)
            fuzz = np.random.uniform(0,1)
            sphere_mat = metal(color,fuzz)

        world_list.append(sphere(center,0.2,sphere_mat))

glass1 = dielectric(1.5)
lambert1 = lambertian(npa([.4,.2,.1]))
metal1 = metal(npa([.7,.6,.5]),0.0)

world_list.append(sphere(npa([0,1,0]),1.0,lambert1))
world_list.append(sphere(npa([-4,1,0]),1.0,glass1))
world_list.append(sphere(npa([4,1,0]),1.0,metal1))



WORLD = hittable_list(world_list)

print('building BVH')
BVH = BVH_node(WORLD, 0, float('inf'))
print('BVH built')

#---------------Camera description------------------------------------------
aspect_ratio = 16/9
vert_fov = 20#degrees
lookfrom = np.array([13,2,3])
lookat = np.array([0,0,0])
v_up = np.array([0,1,0])
aperture = .1
focal_point = lookat


img_width = 300
img_height = int(img_width/aspect_ratio)

SCENE_CAMERA = camera(aspect_ratio=aspect_ratio,vert_fov=vert_fov,lookfrom=lookfrom,lookat=lookat,v_up=v_up,aperture=aperture,focal_point=focal_point)

#---------------Rendering settings------------------------------------------
samples_per_pixel = 1
max_depth = 5
num_processes = 8#going any higher than 8 doesn't really give any further benefit
aa_strength = 1.0

#29.36 sec
#1 sample, 5 deep, 8 proc