#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 python3Packages.h5py python3Packages.numpy python3Packages.matplotlib

import h5py
import numpy as np
import matplotlib.pyplot as plt

def checkFile(filename):
    f = h5py.File(filename, "r")
    print(list(f.keys()))
    vel = f["m"]
    d = f["d"]

    print(vel.shape)
    print(vel[:])
    print(d[:])
    plt.imshow(vel)
    plt.show()

print("Velocity field")
checkFile("../../data/vel.h5")
print("RTM image")
checkFile("../../data/rtm.h5")
print("RTM remigrated image")
checkFile("../../data/rtm_remig.h5")

