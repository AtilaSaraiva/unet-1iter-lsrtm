import os
import h5py
import torch
from tiler import Tiler, Merger
from sklearn.preprocessing import RobustScaler, MaxAbsScaler
from unet import UNet
from matplotlib import pyplot as plt
import json
from plot import plotimage
import numpy as np


def main(param):
    scaler = RobustScaler()

    dataFolder = os.environ["DATADIR"]
    rtm_file = h5py.File(dataFolder + f"rtm_{param['model']}.h5", "r")
    rtm_dset = rtm_file["m"]
    scaler_mig = scaler.fit(rtm_dset)
    rtm_norm = scaler_mig.transform(rtm_dset)
    original_shape = rtm_norm.shape
    rtm_norm = rtm_norm.reshape((1,*original_shape))

    tileShape = (1, param["patch_size"], param["patch_size"])
    tiler = Tiler(data_shape=rtm_norm.shape,
          tile_shape=tileShape,
          overlap=(0,param["overlap"],param["overlap"]),
          channel_dimension=0)

    tiles = tiler.get_all_tiles(rtm_norm)
    tiles = torch.from_numpy(tiles)

    modeldir = os.environ['MODELDIR']
    model = UNet(
        ndim=2,
        in_channels=1,
        out_channels=1,
        patch_size=param["patch_size"],
        base_channels=param["base_channels"],
        norm=False
    )
    model.load_state_dict(torch.load(modeldir + f"spaceUnet-{param['model']}.pt"))

    with torch.no_grad():
        filtered_tiles = model(tiles)

        merger = Merger(tiler)
        merger.add_batch(0, filtered_tiles.shape[0], filtered_tiles.numpy())

        normalized_filtered_image = merger.merge(unpad=True).reshape(original_shape)

    filtered_image = scaler_mig.inverse_transform(normalized_filtered_image)

    if param["lsrtm"]:
        lsrtm_file = h5py.File(dataFolder + f"lsrtm_{param['model']}.h5", "r")
        percentiles = np.percentile(lsrtm_file["m"], [98, 2])
        vmin = np.min(percentiles)
        vmax = np.max(percentiles)
        fig, ax = plt.subplots(3)
        ax[2].imshow(lsrtm_file["m"], cmap="gray", aspect=True, vmin=vmin, vmax=vmax)
    else:
        fig, ax = plt.subplots(2)

    percentiles = np.percentile(rtm_dset, [98, 2])
    vmin = np.min(percentiles)
    vmax = np.max(percentiles)
    ax[0].imshow(rtm_dset, cmap="gray", aspect=True, vmin=vmin, vmax=vmax)
    percentiles = np.percentile(filtered_image, [98, 2])
    vmin = np.min(percentiles)
    vmax = np.max(percentiles)
    print(vmin, vmax)
    ax[1].imshow(filtered_image, cmap="gray", aspect=True, vmin=vmin, vmax=vmax)
    plt.show()

    plotimage(
        param,
        rtm_file["d"],
        rtm_dset,
        name="rtm",
        domain="space",
        xlim=param["blocks"]["xlimList"],
        ylim=param["blocks"]["ylimList"],
        xline=param["xline"]
    )

    plotimage(param,
        rtm_file["d"],
        filtered_image,
        name="filtered",
        domain="space",
        xlim=param["blocks"]["xlimList"],
        ylim=param["blocks"]["ylimList"],
        xline=param["xline"]
    )

    if param["lsrtm"]:
        plotimage(param,
            lsrtm_file["d"],
            lsrtm_file["m"],
            name="lsrtm",
            domain="space",
            xlim=param["blocks"]["xlimList"],
            ylim=param["blocks"]["ylimList"],
            xline=param["xline"]
        )


    with h5py.File(dataFolder + f"filtered_space_domain_image-{param['model']}.h5", "w") as f:
        f.create_dataset('m', data=filtered_image)

if __name__ == "__main__":
    with open("dataconf/spaceDomain/marmousi.json", "r") as arq:
        marmousi = json.load(arq)
    main(marmousi)

    # with open("dataconf/spaceDomain/sigsbee.json", "r") as arq:
        # sigsbee = json.load(arq)
    # main(sigsbee)
