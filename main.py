from tqdm import tqdm
from vec3 import *
from ray import *
import numpy as np
from hittable import *
from sphere import *


def color_string(color):
    ir = 255.999 * color.x()
    ig = 255.999 * color.y()
    ib = 255.999 * color.z()
    #ir,ig,ib = tuple((color*255.999).d())#nicer, but way slower
    out_str = str(ir) + ' ' + str(ig) + ' ' + str(ib) + '\n'
    return out_str


def write_image(filename,w,h,pixels):

    with open(filename,'w') as F:
        header = 'P3\n' + str(w) + ' ' + str(h) + '\n255\n'
        F.write(header)

        idx = 0
        for i in tqdm(range(h)):
            for j in range(w):
                #r = i/(h-1)
                #g = j/(w-1)
                #b = 0.25

                #color = vec3(r,g,b)
                color = pixels[idx]
                idx += 1

                out_str = color_string(color)
                F.write(out_str)




def hit_sphere(center,radius,r):
    oc = r.origin - center
    a = r.dir.length_squared()
    half_b = dot(oc,r.dir)
    c = oc.length_squared() - radius*radius
    discriminant = half_b*half_b - a*c

    if discriminant < 0:
        return -1
    else:
        return (-half_b - np.sqrt(discriminant)) / a

def ray_color(r):
    #t = hit_sphere(vec3(0,0,-1),0.5,r)

    s = sphere(vec3(0,0,-1),0.5)
    record = hit_record(None,None,None)
    hit,record = s.hit(r,float('-inf'),float('inf'),record)


    if hit and record.t>0:
        N = (r.at(record.t) - vec3(0,0,-1)).unit_vector()
        return (N+1)*0.5

    unit_dir = r.dir.unit_vector()
    t = 0.5*(unit_dir.y() + 1)
    return vec3(1,1,1)*(1-t) + vec3(.5,.7,1)*t




def main():

    aspect_ratio = 16/9
    img_width = 350
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

