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

from scene_desc import *

import sys






def main():
    if len(sys.argv) < 2:
        filename = None
    else:
        filename = sys.argv[1]
    if filename is None or filename == '':
        filename = 'sample.ppm'



    print('Resolution: ' + str(img_width) +  ' x ' + str(img_height))
    print('Filename: ' + filename)


    colors = []

    pixel_colors = np.zeros((img_height,img_width,3))
    for s in tqdm(range(samples_per_pixel),desc='Rendering: '):
        for j in tqdm(range(img_height),desc='Col: '):
            for i in range(img_width):
                u = (i + np.random.uniform(-.5, .5)) / (img_width - 1)
                v = (img_height - j + np.random.uniform(-.5, .5)) / (img_height - 1)  # to make up for the backwards range used in the book

                r = SCENE_CAMERA.get_ray(u, v)
                #print(img_height-j-1,i)
                pixel_colors[j,i,:] = pixel_colors[j,i,:] + r.get_color(WORLD, max_depth)
    pixel_colors /= samples_per_pixel


    """
    colors = []
    for j in tqdm(range(img_height),desc='Rendering:'):
        for i in range(img_width):
            pixel_color = np.array([0,0,0])
            for s in range(samples_per_pixel):
                u = (i+np.random.uniform(-.5,.5))/(img_width-1)
                v = (img_height-j+np.random.uniform(-.5,.5))/(img_height-1)#to make up for the backwards range used in the book

                r = SCENE_CAMERA.get_ray(u,v)
                pixel_color = pixel_color + r.get_color(WORLD,max_depth)

            pixel_color = pixel_color/samples_per_pixel
            colors.append(pixel_color)
    """

    write_image(filename,img_width,img_height,pixel_colors)



if __name__ == "__main__":
    main()

