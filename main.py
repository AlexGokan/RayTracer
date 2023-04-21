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

def ray_color(r,world,depth):
    #t = hit_sphere(vec3(0,0,-1),0.5,r)
    if depth <= 0:
        return np.array([0,0,0])


    hit,record = world.hit(r,0.001,float('inf'))

    if hit:
        target = record.p + record.normal + random_vec3_in_sphere()
        return ray_color(ray(record.p,target-record.p),world,depth-1) * 0.5


    unit_dir = unit_vector(r.dir)
    t = 0.5*(unit_dir[1] + 1)
    return np.array([1,1,1])*(1-t) + np.array([.5,.7,1])*t




def main():

    samples_per_pixel = 2
    max_depth = 20


    s1 = sphere(np.array([0, 0, -1]), 0.5)
    s2 = sphere(np.array([0,-100.5,-1]), 100)
    s3 = sphere(np.array([.7, .2, -1]), 0.2)
    world = hittable_list([[s1,s2],[s3]])

    aspect_ratio = 16/9
    img_width = 300
    img_height = int(img_width/aspect_ratio)

    viewport_height = 2
    viewport_width = aspect_ratio * viewport_height
    focal_len = 1.0

    origin = np.array([0,0,0])
    horizontal = np.array([viewport_width,0,0])
    vertical = np.array([0,viewport_height,0])
    lower_left_corner = origin - horizontal/2 - vertical/2 - np.array([0,0,focal_len])

    colors = []

    cam = camera(aspect_ratio=aspect_ratio,viewport_height=viewport_height,focal_length=focal_len)

    for j in tqdm(range(img_height)):
        for i in range(img_width):
            pixel_color = np.array([0,0,0])
            for s in range(samples_per_pixel):
                u = (i+np.random.uniform(-.5,.5))/(img_width-1)
                v = (img_height-j+np.random.uniform(-.5,.5))/(img_height-1)#to make up for the backwards range used in the book

                r = cam.get_ray(u,v)
                pixel_color = pixel_color + ray_color(r,world,max_depth)
                #r = ray(origin,lower_left_corner + horizontal*u + vertical*v - origin)
                #pixel_color = ray_color(r,world)
            pixel_color = pixel_color/samples_per_pixel
            colors.append(pixel_color)



    write_image('sample.ppm',img_width,img_height,colors)



if __name__ == "__main__":
    main()

