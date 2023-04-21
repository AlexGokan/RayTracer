from tqdm import tqdm
import numpy as np
from header import clamp

def color_string(color):
    ir = int(256 * clamp(color.x(),0,0.99999))
    ig = int(256 * clamp(color.y(),0,0.99999))
    ib = int(256 * clamp(color.z(),0,0.99999))
    #ir,ig,ib = tuple((color*255.999).d())#nicer, but way slower
    out_str = str(ir) + ' ' + str(ig) + ' ' + str(ib) + '\n'
    return out_str


def write_image(filename,w,h,pixels,gamma_correct='sqrt'):

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
                if gamma_correct == 'sqrt':
                    color.e1 = np.sqrt(color.x())
                    color.e2 = np.sqrt(color.y())
                    color.e3 = np.sqrt(color.z())

                idx += 1

                out_str = color_string(color)
                F.write(out_str)