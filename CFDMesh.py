#!/usr/bin/env python
# -*-coding: utf-8-*-

import subprocess
import Point
import re


class CFDMesh(object):

    def __init__(self, filename=""):

        self.filename = filename
        self.listpoint = []

    def run(self):
        raise Exception("Abstract method.")


class Plot3dMesh(CFDMesh):

    def __init__(self, filename=""):
        super(Plot3dMesh, self).__init__(filename)
        self.block_dim = []
        self.filehead = []

    def check(self, line):
        if len(line) != 3:
            return False
        for ic in line:
            try:
                float(ic)
            except:
                return False
        return True

    def get_filehead(self, line):
        m = re.search("ZONETYPE", line)
        if m is not None:
            listhead = re.findall("\d+", line)
            self.filehead.append(listhead)

    def get_block_info(self):
        cmd = "cat cfl3d.inp | grep '1005\|2004' | sort -n > wallinfo.dat"
        subprocess.call(cmd, shell=True)
        # p.wait()
        self.get_block_dim()
        # cmd = "rm wallinfo.dat"
        # subprocess.call(cmd, shell=True)
        # p.wait()

    def add_point(self, line):
        point = Point.ModeShape(line[0], line[1], line[2])
        self.listpoint.append(point)

    def get_point_list(self):
        with open("wall.dat", "r") as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                # line = line.strip("\n")
                # line = line.strip(" ")
                self.get_filehead(line)
                line = line.split()
                if self.check(line):
                    self.add_point(line)

    def get_block_dim(self):
        with open("wallinfo.dat", "r") as fp:
            lastnum = -1
            while True:
                line = fp.readline()

                if not line:
                    break
                line = line.split()
                dim = (int(line[4]) - int(line[3]) + 1) * (int(line[6]) - int(line[5]) + 1)
                if self.block_dim == [] or line[0] != lastnum:
                    self.block_dim.append(dim)
                else:
                    self.block_dim[-1] += dim
                lastnum = line[0]

    def run(self):
        # self.get_block_info()
        self.get_block_dim()
        self.get_point_list()

        with open("biaotou.dat", "w") as fp:
            fp.write("%d\n" % (len(self.filehead)))
            for bdim in self.filehead:
                fp.write("%d %d %d\n" %(int(bdim[0]), int(bdim[1]), int(bdim[2])))

        with open("wg.dat", "w") as fp:
            fp.write("%d 0\n" % len(self.listpoint))
            for point in self.listpoint:
                point.write_data(fp)

        with open("dim.dat", "w") as fp:
            print(len(self.block_dim))
            for dim in self.block_dim:
                fp.write("%d\n" % (dim))


class FluentMesh(CFDMesh):
    pass


if __name__ == "__main__":
    cfl3dmesh = Plot3dMesh()
    cfl3dmesh.run()
    # with open("dim.dat", "w") as fp:
    #     print(len(cfl3dmesh.block_dim))
    #     for dim in cfl3dmesh.block_dim:
    #         fp.write(str(dim) + "\n")

