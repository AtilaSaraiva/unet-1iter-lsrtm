import os
import h5py
import torch
import numpy as np
from tiler import Tiler, Merger
from sklearn.preprocessing import RobustScaler, MaxAbsScaler
from unet import UNet
from matplotlib import pyplot as plt
from trainUnetClass import CurveletFilter, make_curv_transform, scaleThat, unscaleThat
import json
from plot import plotimage

def main(param):
    scaler = RobustScaler()

    dataFolder = os.environ["DATADIR"]
    rtm_file = h5py.File(dataFolder + f"rtm_{param['model']}.h5")
    rtm_dset = rtm_file["m"]
    original_shape = rtm_dset.shape
    rtm_dset = np.array(rtm_dset).reshape((1,*original_shape))

    tileShape = (1, param["patch_size"], param["patch_size"])
    tiler = Tiler(data_shape=rtm_dset.shape,
          tile_shape=tileShape,
          overlap=(0,param["overlap"],param["overlap"]),
          channel_dimension=0)


    modeldir = os.environ['MODELDIR']

    curv_fwd, curv_inv, curv_shapes = make_curv_transform(tiler.get_tile(rtm_dset, 0), with_phase=True)
    model =  CurveletFilter(curv_shapes, base_channels=param["base_channels"])
    model.load_state_dict(torch.load(modeldir + f"curveletUnet-{param['model']}.pt"))

    merger = Merger(tiler)

    with torch.no_grad():

        for tile_id, tile in tiler(rtm_dset):

            tile_amplitude, tile_phase = curv_fwd(tile)

            scales = scaleThat(tile_amplitude)

            tile_amplitude = tuple([torch.from_numpy(i) for i in tile_amplitude])

            filtered_tile_curvDomain = model(tile_amplitude)

            unscaleThat(filtered_tile_curvDomain, scales)

            filtered_tile = curv_inv(filtered_tile_curvDomain, tile_phase)

            merger.add(tile_id, filtered_tile)

    filtered_image = merger.merge(unpad=True)

    if param["lsrtm"]:
        lsrtm_file = h5py.File(dataFolder + f"lsrtm_{param['model']}.h5", "r")
        fig, ax = plt.subplots(3)
        percentiles = np.percentile(lsrtm_file["m"], [98, 2])
        vmin = np.min(percentiles)
        vmax = np.max(percentiles)
        ax[2].imshow(lsrtm_file["m"], cmap="gray", aspect=True, vmin=vmin, vmax=vmax)
    else:
        fig, ax = plt.subplots(2)

    percentiles = np.percentile(rtm_file["m"], [98, 2])
    vmin = np.min(percentiles)
    vmax = np.max(percentiles)
    ax[0].imshow(rtm_file["m"], cmap="gray", aspect=True, vmin=vmin, vmax=vmax)
    percentiles = np.percentile(filtered_image[0,:,:], [98, 2])
    vmin = np.min(percentiles)
    vmax = np.max(percentiles)
    ax[1].imshow(filtered_image[0,:,:], cmap="gray", aspect=True, vmin=vmin, vmax=vmax)
    plt.show()

    plotimage(
        param,
        rtm_file["d"],
        rtm_file["m"],
        name="rtm",
        domain="curvelet",
        xlim=param["blocks"]["xlimList"],
        ylim=param["blocks"]["ylimList"],
        xline=param["xline"]
    )

    plotimage(param,
        rtm_file["d"],
        filtered_image[0,:,:],
        name="filtered",
        domain="curvelet",
        xlim=param["blocks"]["xlimList"],
        ylim=param["blocks"]["ylimList"],
        xline=param["xline"]
    )

    if param["lsrtm"]:
        plotimage(param,
            lsrtm_file["d"],
            lsrtm_file["m"],
            name="lsrtm",
            domain="curvelet",
            xlim=param["blocks"]["xlimList"],
            ylim=param["blocks"]["ylimList"],
            xline=param["xline"]
        )

    with h5py.File(dataFolder + f"filtered_curvelet_domain_image-{param['model']}.h5", "w") as f:
        f.create_dataset('m', data=filtered_image[0,:,:])

if __name__ == "__main__":
    with open("dataconf/curveletDomain/marmousi.json", "r") as arq:
        marmousi = json.load(arq)
    main(marmousi)

    with open("dataconf/spaceDomain/sigsbee.json", "r") as arq:
        sigsbee = json.load(arq)
    main(sigsbee)
