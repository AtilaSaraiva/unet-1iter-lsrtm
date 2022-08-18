import os
import h5py
import torch
from tiler import Tiler, Merger
from sklearn.preprocessing import RobustScaler, MaxAbsScaler
from unet import UNet
from matplotlib import pyplot as plt

scaler = RobustScaler()

dataFolder = os.environ["DATADIR"]
rtm_file = h5py.File(dataFolder + "rtm.h5")
rtm_dset = rtm_file["m"]
scaler_mig = scaler.fit(rtm_dset)
rtm_norm = scaler_mig.transform(rtm_dset)
original_shape = rtm_norm.shape
rtm_norm = rtm_norm.reshape((1,*original_shape))

tiler = Tiler(data_shape=rtm_norm.shape,
      tile_shape=(1, 32, 32),
      overlap=(0,20,20),
      channel_dimension=0)

tiles = tiler.get_all_tiles(rtm_norm)
tiles = torch.from_numpy(tiles)

modeldir = os.environ['MODELDIR']
model = UNet(ndim=2, in_channels=1, out_channels=1, norm=False)
model.load_state_dict(torch.load(modeldir + "spaceUnet.pt"))

with torch.no_grad():
    filtered_tiles = model(tiles)

    merger = Merger(tiler)
    merger.add_batch(0, filtered_tiles.shape[0], filtered_tiles.numpy())

    normalized_filtered_image = merger.merge(unpad=True).reshape(original_shape)

filtered_image = scaler_mig.inverse_transform(normalized_filtered_image)

fig, ax = plt.subplots(2)
ax[0].imshow(rtm_dset, cmap="seismic")
ax[1].imshow(filtered_image, cmap="seismic")
plt.show()

with h5py.File(dataFolder + "filtered_space_domain_image.h5", "w") as f:
    f.create_dataset('m', data=filtered_image)
