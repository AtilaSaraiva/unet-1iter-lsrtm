import numpy as np
from dataclasses import dataclass
import torch
import torch.nn.functional as F
import pytorch_lightning as pl
from unet import UNet
from curvelops import FDCT2D
from curvelet_filter import CurveletFilter
import pylops
import json
# import m8r
from sklearn.preprocessing import StandardScaler, RobustScaler, MaxAbsScaler

scaler = RobustScaler

def scaleThat(main_input):
    scales = []
    for i in range(len(main_input)):
        scales.append(RobustScaler())
        main_input[i] = scales[i].fit_transform(main_input[i].reshape(-1,main_input[i].shape[-1])).reshape(main_input[i].shape)

    return scales


def unscaleThat(main_input,scales):
    for i in range(len(main_input)):
        aux = main_input[i].numpy()

        main_input[i] = scales[i].inverse_transform(aux.reshape(-1,aux.shape[-1])).reshape(aux.shape)


def threshold(arr,thresh):
    arr[arr < thresh] = 0
    return arr


class RandomDataset(torch.utils.data.Dataset):

    def __init__(self, input_shape=(), output_shape=(), size=1):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.size = int(size)
        self.distribution = torch.distributions.uniform.Uniform(-1, 1)

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        x = self.distribution.sample(self.input_shape)
        y = self.distribution.sample(self.output_shape)
        return x, y

def example_training():
    train_dataset = RandomDataset((2, 16, 16), (2, 16, 16), 1000)
    test_dataset = RandomDataset((2, 16, 16), (2, 16, 16), 100)

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=5)  #, prefetch_factor=3, num_workers=3)
    test_loader = torch.utils.data.DataLoader(train_dataset, batch_size=5)  #, prefetch_factor=3, num_workers=3)

    model = UNet(ndim=2, in_channels=2, out_channels=2, norm=False)

    train_setup = TrainSetup(
        model,
        train_loader=train_loader,
        test_loader=test_loader,
        learning_rate=0.005,
    )

    trainer = pl.Trainer(max_epochs=2000, limit_train_batches=100)
    trainer.fit(train_setup)


def make_curv_transform(x, nbscales=2, nbangles=8, with_phase=False):
    shape = x.shape

    dct = FDCT2D(shape, nbscales=nbscales, nbangles_coarse=nbangles)

    xc = dct.struct(dct * x.ravel())

    curv_shapes = [(1, *xc[s][w].shape)
                    for s, _ in enumerate(xc)
                    for w, _ in enumerate(xc[s])]

    def curv_fwd(x):
        out_data = [np.empty((1, *shape), dtype=np.float32)
                    for shape in curv_shapes]

        xc = dct.struct(dct * x.ravel())

        i = 0
        for s, _ in enumerate(xc):
            for w, _ in enumerate(xc[s]):
                out_data[i][0,:,:] = threshold(np.abs(xc[s][w]), 1e-6)
                i += 1

        scaleThat(out_data)
        return out_data

    def curv_fwd_with_phase(x):
        out_data = [np.empty((1, *shape), dtype=np.float32)
                    for shape in curv_shapes]

        phase_data = [np.empty((1, *shape), dtype=np.float32)
                    for shape in curv_shapes]

        xc = dct.struct(dct * x.ravel())

        i = 0
        for s, _ in enumerate(xc):
            for w, _ in enumerate(xc[s]):
                out_data[i][0,:,:] = threshold(np.abs(xc[s][w]), 1e-6)
                phase_data[i][0,:,:] = np.angle(xc[s][w])
                i += 1

        return out_data, phase_data

    def curv_inv(tile_amplitude, tile_phase):
        curvArray = []
        contador = 0
        for s, _ in enumerate(xc):
            wedges = []
            for w, _ in enumerate(xc[s]):
                wedges.append(tile_amplitude[contador][0,0,:,:] * np.exp(np.cfloat(1j) * tile_phase[contador][0,0,:,:]))
                contador+=1

            curvArray.append(wedges)

        curvArray = dct.vect(curvArray)
        spaceDomainArray = dct.H * curvArray
        spaceDomainArray = spaceDomainArray.reshape(*shape)
        spaceDomainArray = np.real(spaceDomainArray)

        return spaceDomainArray

    # TODO remove if not useful
    #curv_shape_by_feature = {
    #    s: {w: xc_sw.shape for w, xc_sw in enumerate(xc_s)}
    #    for s, xc_s in enumerate(xc)
    #}

    if with_phase:
        return curv_fwd_with_phase, curv_inv, curv_shapes
    return curv_fwd, curv_inv, curv_shapes


if __name__ == "__main__":
    nbscales = 7
    nbangles_coarse = 4

    patch_num = 1000
    patch_size = 50
    stride_z = 20
    stride_x = 20
    val_split = 0.2
    lr = 0.01

    x = np.random.rand(5, 5)
    y = np.random.rand(5, 5)
    # x = np.ones((5, 5))
    # y = np.ones((5, 5))

    curv_fwd, curv_inv, curv_shapes = make_curv_transform(x)

    xc = curv_fwd(x)
    yc = curv_fwd(y)

    scaleThat(xc)
    scaleThat(yc)

    model =  CurveletFilter(curv_shapes)

    main_input = [torch.from_numpy(i) for i in xc]
    main_output = [torch.from_numpy(i) for i in yc]

    for i in main_input:
        # i.requires_grad_ = True
        # i.require_grad_ = True
        i.requires_grad_(True)

    yc_pred = model(main_input)
    print(yc_pred)
