

inf = float('inf')
neginf = float('-inf')
pi = 3.1415926535897932385

def deg_to_rad(d):
    return d*pi/180
def rad_to_deg(r):
    return r*180/pi

def clamp(x,low,high):
    if x<low:
        return low
    if x>high:
        return high

    return x