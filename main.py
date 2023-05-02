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
import multiprocessing as mp
import time
from scene_desc import *
import queue
import os
import matplotlib.pyplot as plt

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

def render_single_pixel(coord):
    i,j = coord

    u = (i + np.random.uniform(-.5, .5)) / (img_width - 1)
    v = (img_height - j + np.random.uniform(-.5, .5)) / (img_height - 1)

    r = SCENE_CAMERA.get_ray(u,v)
    color = r.get_color(WORLD,max_depth)

    return (i,j,color)


def render_with_pool():
    stime = time.time()

    j_s = [i for i in range(img_height)]
    i_s = [i for i in range(img_width)]

    pixel_colors = np.zeros((img_height, img_width, 3))


    iv,jv = np.meshgrid(i_s,j_s)
    iv,jv = iv.flatten(),jv.flatten()
    coords = list(zip(iv,jv))

    pool = mp.Pool(processes=num_processes)
    results = pool.map(render_single_pixel,coords)

    for c in results:
        i,j,color = c
        pixel_colors[j,i,:] = color

    etime = time.time()
    print('Render time: ',etime-stime)

    return pixel_colors


def render_single_process():
    pixel_colors = np.zeros((img_height, img_width, 3))
    for s in tqdm(range(samples_per_pixel), desc='Rendering: '):
        for j in tqdm(range(img_height), desc='Col: '):
            for i in range(img_width):
                #we offset u and v by a small random amount to fix jaggies
                #   I believe the book offsets by a random amount in (-1,1) but it makes more sense to do it in (-.5,.5) to me, idk
                #v uses height-j to effectively do the count backwards

                u = (i + np.random.uniform(-.5, .5)) / (img_width - 1)
                v = (img_height - j + np.random.uniform(-.5, .5)) / (img_height - 1)

                r = SCENE_CAMERA.get_ray(u, v)
                pixel_colors[j,i,:] = pixel_colors[j,i,:] + r.get_color(WORLD, max_depth)
                #take the average over a set of samples - add up here, divide out by sample_per_pixel at the end

    return pixel_colors


def render_10_processes():
    pipes = []
    for pid in range(10):
        pipes.append(Pipe())  # parent_conn,child_conn

    pixel_colors = np.zeros((img_height, img_width, 3))
    for s in tqdm(range(samples_per_pixel), desc='Rendering: '):
        for j in tqdm(range(img_height), desc='Col: '):
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
                p = Process(target=render_block, args=(j, pid * 120, (pid + 1) * 120, pipes[pid][1]))
                processes.append(p)

            for p in processes:
                p.start()

            for pid in range(10):
                pixel_colors[j, pid * 120:(pid + 1) * 120, :] = pipes[pid][0].recv()

            for pid in range(10):
                processes[pid].join()

    return pixel_colors

def norm(x):
    x = np.copy(x)
    x -= x.min()
    x /= x.max()
    return x

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

    image = np.zeros((img_height,img_width,3))

    for s in tqdm(range(samples_per_pixel)):
        #pixel_colors = render_single_process()
        pixel_colors = render_with_pool()

        #plt.imshow(norm(pixel_colors))
        #plt.show()

        print(np.shape(pixel_colors),np.shape(image))
        #pixel_colors /= samples_per_pixel
        image = image + pixel_colors/samples_per_pixel

    write_image(filename,img_width,img_height,image)



if __name__ == "__main__":
    main()

