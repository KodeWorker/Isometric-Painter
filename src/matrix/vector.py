import numpy as np

class Vector2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return '{}({}, {})'.format('Vector2D', self.x, self.y)
    # addition
    def __add__(self, other):
        if isinstance(other, self.__class__):        
            return Vector2D(self.x+other.x, self.y+other.y)
        else:
            raise TypeError(('unsupported operand type(s) for +: {} and {}')\
                            .format(self.__class__, type(other)))
    # subtraction
    def __sub__(self, other):
        if isinstance(other, self.__class__):        
            return Vector2D(self.x-other.x, self.y-other.y)
        else:
            raise TypeError(('unsupported operand type(s) for +: {} and {}')\
                            .format(self.__class__, type(other)))
    # multiplication/dot-product
    def __mul__(self, other):
        if isinstance(other, self.__class__):        
            return Vector2D(self.x*other.x, self.y*other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x*other, self.y*other)
        else:
            raise TypeError(('unsupported operand type(s) for +: {} and {}')\
                            .format(self.__class__, type(other)))
    # length/norm
    def norm(self):
        return np.sqrt(self.x**2 + self.y**2)
    
    # get numpy array
    def toArray(self):
        return np.array([self.x, self.y])
    
    # rotate
    def rotate(self, degree):
        x, y = \
        self.x*np.cos(np.pi*degree/180)-self.y*np.sin(np.pi*degree/180),\
        self.x*np.sin(np.pi*degree/180)+self.y*np.cos(np.pi*degree/180)
        return Vector2D(x, y)
      
class Vector3D():
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return '{}({}, {}, {})'.format('Vector3D', self.x, self.y, self.z)
    # addition
    def __add__(self, other):
        if isinstance(other, self.__class__):        
            return Vector3D(self.x+other.x, self.y+other.y, self.z+other.z)
        else:
            raise TypeError(('unsupported operand type(s) for +: {} and {}')\
                            .format(self.__class__, type(other)))
    # subtraction
    def __sub__(self, other):
        if isinstance(other, self.__class__):        
            return Vector3D(self.x-other.x, self.y-other.y, self.z-other.z)
        else:
            raise TypeError(('unsupported operand type(s) for +: {} and {}')\
                            .format(self.__class__, type(other)))
    # multiplication/dot-product
    def __mul__(self, other):
        if isinstance(other, self.__class__):        
            return Vector3D(self.x*other.x, self.y*other.y, self.z*other.z)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector3D(self.x*other, self.y*other, self.z*other)
        else:
            raise TypeError(('unsupported operand type(s) for +: {} and {}')\
                            .format(self.__class__, type(other)))
    # length/norm
    def norm(self):
        return np.sqrt(self.x**2 + self.y**2 + self.z **2)
    
    # get numpy array
    def toArray(self):
        return np.array([self.x, self.y, self.z])
    
    # 3d perspective projection by rotation matrix R and displacement v0
    def project(self, R, v0):
        (x, y, z) = np.dot(R, (self-v0).toArray())
        return Vector2D(x, y)

def PerspectiveProjection(gamma, beta, alpha):
    R = np.array([[np.cos(beta)*np.cos(gamma), np.cos(beta)*np.sin(gamma), -np.sin(beta)],
                  [np.sin(alpha)*np.sin(beta)*np.cos(gamma)-np.cos(alpha)*np.sin(gamma), np.sin(alpha)*np.sin(beta)*np.sin(gamma)+np.cos(alpha)*np.cos(gamma), np.sin(alpha)*np.cos(beta)],
                  [np.cos(alpha)*np.sin(beta)*np.cos(gamma)+np.sin(alpha)*np.sin(gamma), np.cos(alpha)*np.sin(beta)*np.sin(gamma)-np.sin(alpha)*np.cos(gamma), np.cos(alpha)*np.cos(beta)]])
    return R