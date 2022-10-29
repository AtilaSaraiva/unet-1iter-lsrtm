import cv2
import h5py
import numpy as np
import sys
import os

def main(infile, outfile, fx, fy):
    M = h5py.File(infile, "r")
    keys = list(M.keys())

    # n is in the order of (nx, ny) so it has to be reverted to the numpy way of writing (ny, nx)
    n = tuple(M["n"])[::-1]

    assert M["m0"].shape == n

    m0_down = cv2.resize(np.array(M["m0"]), (0,0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)

    M_down = h5py.File(outfile, "w")
    M_down.create_dataset("m0", data=m0_down)
    M_down.create_dataset("d", data=(M["d"][0]/float(fx), M["d"][1]/float(fy)))
    M_down.create_dataset("o", data=M["o"])
    M_down.create_dataset("n", data=m0_down.shape[::-1])

    if "dm" in keys:
        assert M["dm"].shape == n
        dm_down = cv2.resize(np.array(M["dm"]), (0,0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
        M_down.create_dataset("dm", data=dm_down)

    M.close()
    M_down.close()

    return

def getArg(key):
    for arg, i in zip(sys.argv, range(len(sys.argv))):
        if key in arg:
            return arg.split("=")[-1]

def testPlot(infile, outfile)
    M = h5py.File(infile, "r")
    M_down = h5py.File(outfile, "w")


if __name__ == "__main__":
    dataFolder = os.environ["DATADIR"]

    infile = getArg("infile")
    fx = float(getArg("fx"))
    fy = float(getArg("fy"))

    infile_name = infile.split("/")[-1].split(".")[0]
    outfile = dataFolder + infile_name + "-down.h5"

    main(infile, outfile, fx, fy)

    test = getArg("test
