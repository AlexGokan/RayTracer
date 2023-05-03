

class AABB:
    def __init__(self,a=None,b=None):
        self.minimum = a
        self.maximum = b


    def min(self):
        return self.minimum
    def max(self):
        return self.maximum

    def hit_slow(self,r,t_min,t_max):
        for a in range(3):
            t0 = min((self.minimum[a]-r.origin[a])/r.dir[a],
                     (self.maximum[a] - r.origin[a]) / r.dir[a])

            t1 = max((self.minimum[a]-r.origin[a])/r.dir[a],
                     (self.maximum[a] - r.origin[a]) / r.dir[a])

            t_min = max(t0,t_min)
            t_max = max(t1,t_max)

            if t_max <= t_min:
                return False
        return True

    def hit_fast(self,r,t_min,t_max):
        for a in range(3):
            invD = 1.0/r.dir[a]
            t0 = (self.minimum[a] - r.origin[a]) * invD
            t1 = (self.maximum[a] - r.origin[a]) * invD
            if invD < 0.0:
                t0,t1 = t1,t0

            t_min = max(t0, t_min)
            t_max = max(t1, t_max)

            if t_max <= t_min:
                return False
        return True

    def hit(self,r,t_min,t_max):
        return self.hit_fast(r,t_min,t_max)


def surrounding_box(boxa,boxb):
    small = [min(boxa.min()[0],boxb.min()[0]),
            min(boxa.min()[1],boxb.min()[1]),
            min(boxa.min()[2],boxb.min()[2])]

    big = [max(boxa.max()[0],boxb.max()[0]),
            max(boxa.max()[1],boxb.max()[1]),
            max(boxa.max()[2],boxb.max()[2])]

    return AABB(small,big)