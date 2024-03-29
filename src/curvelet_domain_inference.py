import os
import h5py
import torch
import numpy as np
from tiler import Tiler, Merger
from sklearn.preprocessing import RobustScaler, MaxAbsScaler
from unet import UNet
from matplotlib import pyplot as plt
from trainUnetClass import CurveletFilter, make_curv_transform, scaleThat, unscaleThat

scaler = RobustScaler()

dataFolder = os.environ["DATADIR"]
rtm_file = h5py.File(dataFolder + "rtm.h5")
rtm_dset = rtm_file["m"]
original_shape = rtm_dset.shape
rtm_dset = np.array(rtm_dset).reshape((1,*original_shape))

tiler = Tiler(data_shape=rtm_dset.shape,
      tile_shape=(1, 32, 32),
      overlap=(0,20,20),
      channel_dimension=0)


modeldir = os.environ['MODELDIR']

curv_fwd, curv_inv, curv_shapes = make_curv_transform(tiler.get_tile(rtm_dset, 0), with_phase=True)
model =  CurveletFilter(curv_shapes)
model.load_state_dict(torch.load(modeldir + "curveletUnet.pt"))

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

fig, ax = plt.subplots(2)
ax[0].imshow(rtm_dset[0], cmap="seismic")
ax[1].imshow(filtered_image[0], cmap="seismic")
plt.show()

with h5py.File(dataFolder + "filtered_curvelet_domain_image.h5", "w") as f:
    f.create_dataset('m', data=filtered_image)
