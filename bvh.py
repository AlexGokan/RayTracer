
from hittable import *
import numpy as np
from vector_operations import *
from functools import cmp_to_key

class BVH_node(hittable):
    def __init__(self,list_of_hittables,t0,t1,start=None,end=None):
        def generic_box_compare(a,b,axis):
            box_a = a.bounding_box(0,0)
            box_b = b.bounding_box(0,0)
            if box_a is None or box_b is None:
                raise ValueError('no bounding box in bvh_node constructor')

            return box_a.min()[axis] < box_b.min()[axis]


        def box_x_compare(a,b):
            return generic_box_compare(a,b,0)
        def box_y_compare(a,b):
            return generic_box_compare(a,b,1)
        def box_z_compare(a,b):
            return generic_box_compare(a,b,2)

        compare_funcs = [box_x_compare,box_y_compare,box_z_compare]

        self.objects = list_of_hittables
        self.t0 = t0
        self.t1 = t1

        if start is None:
            self.start = 0
        else:
            self.start = start

        if end is None:
            self.end = len(list_of_hittables.objects)
        else:
            self.end = end

        #private attributes
        self.box = None
        self.left = None
        self.right = None


        axis = int(np.random.randint(0,2))
        comparator = compare_funcs[axis]

        object_span = self.end - self.start
        if object_span == 1:
            self.left = self.objects.objects[self.start]
            self.right = self.objects.objects[self.start]
        elif object_span == 2:
            if comparator(self.objects.objects[self.start],self.objects.objects[self.start+1]):
                self.left = self.objects.objects[self.start+1]
                self.right = self.objects.objects[self.start]
        else:
            self.objects.objects.sort(key=cmp_to_key(comparator))
            mid = self.start + object_span//2
            self.left = BVH_node(self.objects,t0,t1,self.start,mid)
            self.right = BVH_node(self.objects,t0,t1,mid,self.end)


    def bounding_box(self,t0,t1):
        return self.box

    def hit(self,r,t_min,t_max):
        if not self.box.hit(r,t_min,t_max):
            return False

        hit_left,hit_record = self.left.hit(r,t_min,t_max)
        hit_right,hit_record = self.right.hit(r,t_min,hit_record.t if hit_left else t_max)

        return hit_left or hit_right,hit_record