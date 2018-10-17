# -*- coding:utf-8 -*-

import CFDMesh
import InterWorker
import Get3DModeShape

if __name__ == "__main__":
    cfl3dmesh = CFDMesh.Plot3dMesh()
    cfl3dmesh.run()
    rbfworker = InterWorker.MockRBFMethod()
    n_mode = int(rbfworker.run())
    get3d = Get3DModeShape.Get3DModeShape(n_mode)
    get3d.run()
