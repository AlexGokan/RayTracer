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

from multiprocessing import Process, Pipe


def render_block(j,i_low,i_high,connection):
    pixel_colors = np.zeros((1,i_high-i_low,3))
    for i in range(i_low,i_high):
        u = (i + np.random.uniform(-.5, .5)) / (img_width - 1)
        v = (img_height - j + np.random.uniform(-.5, .5)) / (img_height - 1)

        relative_i_index = i - i_low
        r = SCENE_CAMERA.get_ray(u, v)
        pixel_colors[0, relative_i_index, :] = pixel_colors[0, relative_i_index, :] + r.get_color(WORLD, max_depth)

    connection.send(pixel_colors)
    connection.close()

def main():


    if len(sys.argv) < 2:
        filename = None
    else:
        filename = sys.argv[1]
    if filename is None or filename == '':
        filename = 'sample.ppm'

    #img_width = 60

    print('Resolution: ' + str(img_width) +  ' x ' + str(img_height))
    print('Filename: ' + filename)

    pipes = []
    for pid in range(10):
        pipes.append(Pipe())#parent_conn,child_conn



    pixel_colors = np.zeros((img_height,img_width,3))
    for s in tqdm(range(samples_per_pixel),desc='Rendering: '):
        for j in tqdm(range(img_height),desc='Col: '):
            """
            for i in range(img_width):
                #we offset u and v by a small random amount to fix jaggies
                #   I believe the book offsets by a random amount in (-1,1) but it makes more sense to do it in (-.5,.5) to me, idk
                #v uses height-j to effectively do the count backwards

                u = (i + np.random.uniform(-.5, .5)) / (img_width - 1)
                v = (img_height - j + np.random.uniform(-.5, .5)) / (img_height - 1)

                r = SCENE_CAMERA.get_ray(u, v)
                pixel_colors[j,i,:] = pixel_colors[j,i,:] + r.get_color(WORLD, max_depth)
                #take the average over a set of samples - add up here, divide out by sample_per_pixel at the end
            """
            processes = []
            for pid in range(10):
                p = Process(target=render_block,args=(j,pid*120,(pid+1)*120,pipes[pid][1]))
                processes.append(p)

            for p in processes:
                p.start()
            #p1 = Process(target=render_block,args=(j,0,20,child1_conn,))
            #p2 = Process(target=render_block,args=(j,20,40,child2_conn,))
            #p3 = Process(target=render_block,args=(j,40,60,child3_conn,))

            #p1.start()
            #p2.start()
            #p3.start()

            for pid in range(10):
                pixel_colors[j,pid*120:(pid+1)*120,:] = pipes[pid][0].recv()

            #pixel_colors[j, 0:20, :] = parent1_conn.recv()
            #pixel_colors[j, 20:40, :] = parent2_conn.recv()
            #pixel_colors[j, 40:60, :] = parent3_conn.recv()


            for pid in range(10):
                processes[pid].join()
            #p1.join()
            #p2.join()
            #p3.join()


            #-------------------------------------
            #pixel_colors[j,0:20,:] = render_block(j,0,20)
            #pixel_colors[j,20:40,:] = render_block(j,20,40)
            #pixel_colors[j,40:60,:] = render_block(j,40,60)

        write_image(filename+str(s),img_width,img_height,pixel_colors)#save intermediate images in case something happens

    pixel_colors /= samples_per_pixel


    write_image(filename,img_width,img_height,pixel_colors)



if __name__ == "__main__":
    main()

