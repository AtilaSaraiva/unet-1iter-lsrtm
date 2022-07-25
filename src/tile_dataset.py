import numpy as np
import random
import torch

def tile(data, wsize, dz, dx):

    (z_max, x_max) = data.shape

    n_patch = (z_max//dz+1)*(x_max//dx+1)
    data_patch = np.zeros((n_patch,wsize,wsize,1))

    n = 0
    for z in range(0, z_max, dz):
        for x in range(0, x_max, dx):
            if z_max - z < wsize and x_max - x < wsize:
                data_patch[n,:,:,0] = data[z_max-wsize:z_max, x_max-wsize:x_max]
            elif x_max - x < wsize:
                data_patch[n,:,:,0] = data[z:z+wsize, x_max-wsize:x_max]
            elif z_max - z < wsize:
                data_patch[n,:,:,0] = data[z_max-wsize:z_max, x:x+wsize]
            else:
                data_patch[n,:,:,0] = data[z:z+wsize,x:x+wsize]
            n = n + 1

    return data_patch


def merge(data_patch, z_max, x_max, wsize, dz, dx):

    data_new = np.zeros((z_max, x_max,1))
    count = np.zeros((z_max, x_max, 1))

    n = 0
    for z in range(0, z_max, dz):
        for x in range(0, x_max, dx):
            if z_max - z < wsize and x_max - x < wsize:
                data_new[z_max-wsize:z_max, x_max-wsize:x_max,0] += data_patch[n,:,:,0]
                count[z_max-wsize:z_max, x_max-wsize:x_max,0] += 1
            elif x_max - x < wsize:
                data_new[z:z+wsize, x_max-wsize:x_max,0] += data_patch[n,:,:,0]
                count[z:z+wsize, x_max-wsize:x_max,0] += 1
            elif z_max - z < wsize:
                data_new[z_max-wsize:z_max, x:x+wsize,0] += data_patch[n,:,:,0]
                count[z_max-wsize:z_max, x:x+wsize,0] += 1
            else:
                data_new[z:z+wsize,x:x+wsize,0] += data_patch[n,:,:,0]
                count[z:z+wsize,x:x+wsize,0] += 1
            n = n + 1

    return data_new/count

def extract_patches(data, mask, patch_num, patch_size):

    X = torch.empty((patch_num, 1, patch_size, patch_size))
    Y = torch.empty((patch_num, 1, patch_size, patch_size))

    (z_max, x_max) = data.shape

    for n in range(patch_num):

        # Select random point in data (not too close to edge)
        x_n = random.randint(patch_size // 2, x_max - patch_size // 2)
        z_n = random.randint(patch_size // 2, z_max - patch_size // 2)

        # Extract data and mask patch around point
        X[n,0,:,:] = torch.from_numpy(data[z_n-patch_size//2:z_n+patch_size//2,x_n-patch_size//2:x_n+patch_size//2])
        Y[n,0,:,:] = torch.from_numpy(mask[z_n-patch_size//2:z_n+patch_size//2,x_n-patch_size//2:x_n+patch_size//2])


    return X, Y
