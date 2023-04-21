from tqdm import tqdm

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