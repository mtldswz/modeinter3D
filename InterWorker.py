# -*-coding: utf-8-*-

import subprocess
import os
import sys


class InterWork(object):
    def __init__(self, csdmesh, cfdmesh):
        self.csdmesh = csdmesh
        self.cfdmesh = cfdmesh
        self.list_modeshape = []

    def run(self):
        raise Exception("Abstract method.")


class MockRBFMethod(InterWork):

    def __init__(self, csdmesh="mode.dat", cfdmesh="wg.dat", inp="input.dat", filehead="biaotou.dat"):
        super(MockRBFMethod, self).__init__(csdmesh, cfdmesh)
        self.inputfile = inp
        self.filehead = filehead
        self.codef90 = "MODULM.f90 RBF_MODE.f90"
        self.worker = "RBF_MODE.o"
        self.compiler = None
        self.n_mode = None

    def check_file(self):
        if not os.path.isfile("MODULM.f90") or not os.path.isfile("RBF_MODE.f90"):
            raise Exception("file %s does't exist!" % self.codef90)
        if not os.path.isfile(self.csdmesh):
            raise Exception("file %s does't exist!" % self.csdmesh)
        if not os.path.isfile(self.cfdmesh):
            raise Exception("file %s does't exist!" % self.cfdmesh)
        if not os.path.isfile(self.inputfile):
            raise Exception("file %s does't exist!" % self.inputfile)
        if not os.path.isfile(self.filehead):
            raise Exception("file %s does't exist!" % self.filehead)
        return True

    def check_sys(self):
        if sys.platform == "win32":
            self.worker = "interplation.exe"
            return True
        else:
            cmd = "which ifort"
            rc = subprocess.call(cmd, shell=True)
            if rc == 0:
                self.compiler = "ifort"
                self.compile_f90()
                return True
            cmd = "which gfortran"
            rc = subprocess.call(cmd, shell=True)
            if rc == 0:
                self.compile_f90()
                self.compiler = "gfortran"
                return True
        # raise Exception("no Frotran compiler! Pleas install 'ifort' or 'gfortran'")

    def compile_f90(self):
        if self.compiler is None:
            raise Exception("no Frotran compiler! Pleas install 'ifort' or 'gfortran'")
        cmd = self.compiler + self.codef90 + "-o" + self.worker
        rc = subprocess.call(cmd, shell=True)
        if rc != 0:
            raise Exception("compile f90 code fail!")

    def run(self):
        self.check_sys()

        if self.check_file():
            if self.check_sys():
                subprocess.call(self.worker)
                print("done")
            else:
                cmd = os.path.join(".", self.worker)
                subprocess.call(cmd, shell=True)

        with open("MODE.dat", "r") as fp:
            line = fp.readline()
            line = line.split()
            self.n_mode = line[1]
        return self.n_mode


if __name__ == "__main__":
    nrbf = MockRBFMethod()
    nrbf.run()
