#!/usr/bin/env python
# -*-coding: utf-8-*-

import sys


class Point(object):
    def __init__(self, x, y, z):
        super(Point, self).__init__()
        self.x = x
        self.y = y
        self.z = z

    def write_data(self, fp):
        self.x = float(self.x)
        self.y = float(self.y)
        self.z = float(self.z)
        fp.write("%15.7E %15.7E %15.7E\n" % (self.x, self.y, self.z))


class ModeShape(Point):

    def __init__(self, x, y, z):
        super(ModeShape, self).__init__(x, y, z)


if __name__ == "__main__":
#     point = Point(1.0, 2.0, 3.0)
#     point.write_data()
    print(sys.platform)
