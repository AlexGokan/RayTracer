


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


def random_vec3_in_unit_sphere():
    while True:
        p = random_vec3(-1,1)
        if length_squared(p) <= 1:
            return p

def random_vec3_in_hemisphere(normal):
    v = random_vec3_in_unit_sphere()
    if np.dot(v,normal) > 0.0:
        return v
    else:
        return -1 * v

def random_vec2_in_unit_disk():
    while True:
        p = np.array([np.random.uniform(-1,1),np.random.uniform(-1,1)])
        if length_squared(p) < 1:
            return p

def near_zero(x):
    s = 1e-8
    if np.max(np.abs(x)) < s:
        return True
    return False

def reflect(v,n):
    return v - 2*np.dot(v,n)*n

def refract(uv,n,etai_over_etat):
    cos_theta = min(np.dot(-uv,n),1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta*n)
    r_out_parallel = -np.sqrt(abs(1-length_squared(r_out_perp))) * n

    return r_out_perp + r_out_parallel