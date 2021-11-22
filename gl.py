#lab 1 fillpolygon Andres Paiz 191142
import struct

def char(c):
  """
  Input: requires a size 1 string
  Output: 1 byte of the ascii encoded char 
  """
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  """
  Input: requires a numberber such that (-0x7fff - 1) <= numberber <= 0x7fff
         ie. (-32768, 32767)
  Output: 2 bytes
  Example:  
  >>> struct.pack('=h', 1)
  b'\x01\x00'
  """
  return struct.pack('=h', w)

def dword(d):
  """
  Input: requires a numberber such that -2147483648 <= numberber <= 2147483647
  Output: 4 bytes
  Example:
  >>> struct.pack('=l', 1)
  b'\x01\x00\x00\x00'
  """
  return struct.pack('=l', d)

def switch(cl):
    color_sw = cl * 255
    return int(color_sw)

def color(r, g, b):
  """
  Input: each parameter must be a numberber such that 0 <= numberber <= 255
         each numberber represents a color in rgb 
  Output: 3 bytes
  Example:
  >>> bytes([0, 0, 255])
  b'\x00\x00\xff'
  """
  return bytes([b, g, r])

GREEN = color(0,200,0)
BLACK = color(0,0,0)
WHITE = color(255,255,255)

class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color_usado = GREEN
        self.clear()

    def glViewPort(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_width = width
        self.viewport_height = height

    def clear(self):
        self.pixels = [
            [WHITE for x in range(self.width)]
            for y in range(self.height)
        ]
 
    def glvertex(self, x, y):
        self.pixels[y][x] = self.color_usado


    def set_color(self, color):
        self.color_usado = color

    def  line( self , x1 , y1 , x2 , y2 ):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        offset = 0
        threshold = 0.5

        try:
            m = dy/dx
            y = y1

            for x in range(x1, x2 + 1):
                if steep:
                    self.glvertex(y, x)
                else:
                    self.glvertex(x, y)

                offset += m
                if offset >= threshold:
                    y += 1 if y1 < y2 else -1
                    threshold += 1
        except ZeroDivisionError:
            pass

    def polifill(self, vertexs):
        self.vertexs = vertexs
        self.size = len(self.vertexs)
        for vertex in range(self.size):
            x1 = self.vertexs[vertex][0]
            y1 = self.vertexs[vertex][1]

            if vertex + 1 < self.size:
                x2 = self.vertexs[vertex + 1][0]
            else:
                self.vertexs[0][0]

            if vertex + 1 < self.size:
                y2 = self.vertexs[vertex + 1][1] 
            else:
                self.vertexs[0][1]

            self.line(x1, y1, x2, y2)
            for x in range(self.width):
                for y in range(self.height):
                    if self.parimpar(x, y) == True:
                        self.glvertex(x, y)

    
    def parimpar(self, x, y):
        number = self.size
        i = 0
        j = number - 1
        c = False
        for i in range(number):
            if ((self.vertexs[i][1] > y) != (self.vertexs[j][1] > y)) and \
                    (x < self.vertexs[i][0] + (self.vertexs[j][0] - self.vertexs[i][0]) * (y - self.vertexs[i][1]) /
                                    (self.vertexs[j][1] - self.vertexs[i][1])):
                c = not c
            j = i
        return c

    
    def write(self, name):
        f = open(name, 'bw')
        f.write(bytes('B'.encode('ascii')))
        f.write(bytes('M'.encode('ascii')))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])

        f.close()