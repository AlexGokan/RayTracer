


import numpy as np

def length_squared(x):
    return np.sum(np.power(x,2))
def length(x):
    return np.sqrt(length_squared(x))

def unit_vector(x):
    return x/length(x)

def random_vec3(low=None,high=None):
    if low is None or high is None:
        return np.random.uniform(size=3)
    return np.random.uniform(low,high,size=3)


def random_vec3_in_sphere():
    while True:
        p = random_vec3(-1,1)
        if length_squared(p) <= 1:
            return p