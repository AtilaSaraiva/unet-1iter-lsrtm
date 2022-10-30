import os
import h5py
import torch
from tiler import Tiler, Merger
from sklearn.preprocessing import RobustScaler, MaxAbsScaler
from unet import UNet
from matplotlib import pyplot as plt
import json
from plot import plotimage


def main(param):
    scaler = RobustScaler()

    dataFolder = os.environ["DATADIR"]
    rtm_file = h5py.File(dataFolder + f"rtm_{param['model']}.h5")
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
    model = UNet(ndim=2, in_channels=1, out_channels=1, norm=False)
    model.load_state_dict(torch.load(modeldir + f"spaceUnet-{param['model']}.pt"))

    with torch.no_grad():
        filtered_tiles = model(tiles)

        merger = Merger(tiler)
        merger.add_batch(0, filtered_tiles.shape[0], filtered_tiles.numpy())

        normalized_filtered_image = merger.merge(unpad=True).reshape(original_shape)

    filtered_image = scaler_mig.inverse_transform(normalized_filtered_image)

    # plotimage(
        # param,
        # rtm_file["d"],
        # rtm_dset,
        # name="rtm",
        # domain="space",
        # xlim=param["blocks"]["xlimList"],
        # ylim=param["blocks"]["ylimList"],
        # xline=param["xline"]
    # )

    # plotimage(param,
        # rtm_file["d"],
        # filtered_image,
        # name="filtered",
        # domain="space",
        # xlim=param["blocks"]["xlimList"],
        # ylim=param["blocks"]["ylimList"],
        # xline=param["xline"]
    # )

    fig, ax = plt.subplots(2)
    ax[0].imshow(rtm_dset, cmap="seismic")
    ax[1].imshow(filtered_image, cmap="seismic")
    plt.show()


    with h5py.File(dataFolder + f"filtered_space_domain_image-{param['model']}.h5", "w") as f:
        f.create_dataset('m', data=filtered_image)

if __name__ == "__main__":
    with open("dataconf/spaceDomain/marmousi.json", "r") as arq:
        marmousi = json.load(arq)
    main(marmousi)
