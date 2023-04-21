from tqdm import tqdm
from vec3 import *
from ray import *
import numpy as np
from hittable import *
from sphere import *
from fileio import *

def ray_color(r):
    #t = hit_sphere(vec3(0,0,-1),0.5,r)

    s1 = sphere(vec3(0,0,-1),0.5)
    s2 = sphere(vec3(.7,.7,-1),0.4)
    s3 = sphere(vec3(.7,.2,-1),0.2)
    slist = hittable_list([[s1,s2],[s3]])

    hit,record = slist.hit(r,float('-inf'),float('inf'))


    if hit and record.t>0:
        N = (r.at(record.t) - vec3(0,0,-1)).unit_vector()
        return (N+1)*0.5

    unit_dir = r.dir.unit_vector()
    t = 0.5*(unit_dir.y() + 1)
    return vec3(1,1,1)*(1-t) + vec3(.5,.7,1)*t




def main():

    aspect_ratio = 16/9
    img_width = 150
    img_height = int(img_width/aspect_ratio)

    viewport_height = 2
    viewport_width = aspect_ratio * viewport_height
    focal_len = 1.0

    origin = vec3(0,0,0)
    horizontal = vec3(viewport_width,0,0)
    vertical = vec3(0,viewport_height,0)
    lower_left_corner = origin - horizontal/2 - vertical/2 - vec3(0,0,focal_len)

    colors = []

    for j in tqdm(range(img_height)):
        for i in range(img_width):
            u = i/(img_width-1)

            v = (img_height-j)/(img_height-1)#to make up for the backwards range used in the book

            r = ray(origin,lower_left_corner + horizontal*u + vertical*v - origin)
            pixel_color = ray_color(r)

            colors.append(pixel_color)



    write_image('sample.ppm',img_width,img_height,colors)



if __name__ == "__main__":
    main()

