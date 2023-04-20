from tqdm import tqdm
from vec3 import *
from ray import *
import numpy as np

print('hello world')




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

        for i in tqdm(range(h)):
            for j in range(w):
                r = i/(h-1)
                g = j/(w-1)
                b = 0.25

                color = vec3(r,g,b)

                out_str = color_string(color)
                F.write(out_str)

write_image('sample.ppm',256,256,None)

v1 = vec3(0,1,2)
v2 = vec3(0,2,3)
v3 = v1+v2
v4 = v1/2
v5 = v1 * v2
v6 = v1 - 4
v7 = v1 / v2
print(v7)

print(v2.unit_vector())

print(v4.d())
print(v4.length())


r = ray(v1,v2)
print(r.at(0.5))


print('done')


