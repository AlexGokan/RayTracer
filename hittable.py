

class hit_record:
    def __init__(self,p,normal,t):
        self.p = p
        self.normal = normal
        self.t = t

class hittable:
    def __init__(self):
        raise NotImplementedError()#need to be implemented by the subclass

    def hit(self,r,t_min,t_max,rec):
        raise NotImplementedError()#need to be implemented by the subclass