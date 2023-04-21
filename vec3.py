import numpy as np

class vec3:
    def __init__(self,x,y,z):
        self.e1 = x
        self.e2 = y
        self.e3 = z
        self.data = np.array([x,y,z])

    def x(self):
        return self.e1

    def y(self):
        return self.e2

    def z(self):
        return self.e3

    def d(self):
        return self.data

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self,key,item):
        assert(key<=2)
        self.data[key] = item

    def __add__(self,c):
        if isinstance(c,vec3):
            data = c.d()
        else:
            data = c
        return vec3(*tuple(self.d() + data))

    def __sub__(self,c):
        if isinstance(c,vec3):
            data = c.d()
        else:
            data = c
        return vec3(*tuple(self.d() - data))

    def __mul__(self,c):
        if isinstance(c,vec3):
            data = c.d()
        else:
            data = c
        return vec3(*tuple(self.d() * data))

    def __truediv__(self,c):
        if isinstance(c,vec3):
            data = c.d()
        else:
            data = c
        return vec3(*tuple(self.d() / data))

    def __floordiv__(self, c):
        if isinstance(c,vec3):
            data = c.d()
        else:
            data = c
        return vec3(*tuple(np.floor(self.d() / data)))

    def length_squared(self):
        return np.sum(np.power(self.d(),2))

    def length(self):
        return np.sqrt(self.length_squared())

    def dot(self,other):
        return np.dot(self.d(),other.d())

    def cross(self,other):
        return vec3(*tuple(np.cross(self.d(),other.d())))

    def unit_vector(self):
        return vec3(*tuple(self.d()/self.length()))

    def __str__(self):
        return 'vec3: ' + str(self.d())

    def __repr__(self):
        return self.__str__()


def dot(a,b):
    return np.dot(a.d(),b.d())

def cross(a, b):
    return vec3(*tuple(np.cross(a.d(), b.d())))

