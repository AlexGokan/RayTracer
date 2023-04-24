from header import *

from tqdm import tqdm
#from vec3 import *
from ray import *
import numpy as np
from vector_operations import *
from hittable import *
from sphere import *
from fileio import *
from camera import *
from material import *

import sys

def ray_color(r,world,depth):
    #t = hit_sphere(vec3(0,0,-1),0.5,r)
    if depth <= 0:
        return np.array([0,0,0])


    hit,record = world.hit(r,0.001,float('inf'))

    if hit:

        mat_scat_bool,scattered,attenuation = record.material.scatter(r,record)
        if mat_scat_bool:
            return attenuation * ray_color(scattered,world,depth-1)

        #target = record.p + random_vec3_in_hemisphere(record.normal)
        #return ray_color(ray(record.p,target-record.p),world,depth-1) * 0.5


    unit_dir = unit_vector(r.dir)
    t = 0.5*(unit_dir[1] + 1)
    return np.array([1,1,1])*(1-t) + np.array([.5,.7,1])*t#sky shader




def main():

    samples_per_pixel = 3
    max_depth = 2

    blue_lambert = lambertian(np.array([.8,.8,1]))
    ground_mat = lambertian(np.array([.8,1,.7]))
    metal_shader = metal(np.array([1,1,1]),roughness=0.2)
    glass_shader = dielectric(1.5)

    s_ground = sphere(np.array([0,-100.5,-1]),100,ground_mat)
    s1 = sphere(np.array([0,0,-1]),0.5,blue_lambert)
    s2 = sphere(np.array([-1,0,-1]),0.5,glass_shader)
    s22 = sphere(np.array([-1,0,-1]),-0.45,glass_shader)
    s3 = sphere(np.array([1,0,-1]),0.5,metal_shader)
    world = hittable_list([s1,s2,s22,s3,s_ground])

    aspect_ratio = 16/9
    img_width = 150
    img_height = int(img_width/aspect_ratio)

    viewport_height = 2
    viewport_width = aspect_ratio * viewport_height
    focal_len = 1.0

    origin = np.array([0,0,0])
    horizontal = np.array([viewport_width,0,0])
    vertical = np.array([0,viewport_height,0])
    lower_left_corner = origin - horizontal/2 - vertical/2 - np.array([0,0,focal_len])

    #cam = camera(aspect_ratio=aspect_ratio,focal_length=focal_len,vert_fov=45)
    cam = camera(aspect_ratio=aspect_ratio,focal_length=1,vert_fov=90,lookfrom=np.array([-2,2,1]),lookat=np.array([0,0,-1]))
    print(str(img_width) +  ' x ' + str(img_height))


    colors = []
    for j in tqdm(range(img_height),desc='Rendering:'):
        for i in range(img_width):
            pixel_color = np.array([0,0,0])
            for s in range(samples_per_pixel):
                u = (i+np.random.uniform(-.5,.5))/(img_width-1)
                v = (img_height-j+np.random.uniform(-.5,.5))/(img_height-1)#to make up for the backwards range used in the book

                r = cam.get_ray(u,v)
                pixel_color = pixel_color + ray_color(r,world,max_depth)

            pixel_color = pixel_color/samples_per_pixel
            colors.append(pixel_color)

    if len(sys.argv) < 2:
        filename = None
    else:
        filename = sys.argv[1]
    if filename is None or filename == '':
        filename = 'sample.ppm'
    write_image(filename,img_width,img_height,colors)



if __name__ == "__main__":
    main()

