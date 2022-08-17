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


def scaleThat(main_input):
    scales = []
    for i in range(len(main_input)):
        scales.append(RobustScaler())
        main_input[i] = scales[i].fit_transform(main_input[i].reshape(-1,main_input[i].shape[-1])).reshape(main_input[i].shape)
    return scales


def unscaleThat(main_input,scales):
    for i in range(len(main_input)):
        main_input[i] = scales[i].inverse_transform(main_input[i].reshape(-1,main_input[i].shape[-1])).reshape(main_input[i].shape)


def threshold(arr,thresh):
    arr[arr < thresh] = 0
    return arr


class TrainSetup(pl.LightningModule):

    def __init__(self,
                 model: torch.nn.Module,
                 train_loader: torch.utils.data.DataLoader,
                 test_loader: torch.utils.data.DataLoader = None,
                 val_loader: torch.utils.data.DataLoader = None,
                 learning_rate: float = 0.005):
        super().__init__()
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader or self.train_loader
        self.val_loader = val_loader or self.test_loader
        self.learning_rate = learning_rate
 
    def train_dataloader(self):
        return self.train_loader

    def val_dataloader(self):
        return self.val_loader
 
    def test_dataloader(self):
        return self.test_loader
 
    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer
 
    def training_step(self, batch, batch_idx):
        X, Y = batch
        Y_pred = self.model(X)
        loss =  F.mse_loss(Y, Y_pred)
        return loss
 
    def validation_step(self, batch, batch_idx):
        loss = self.training_step(batch, batch_idx)
        metrics = {"loss": loss}
        metrics = {f"val_{k}": v for k, v in metrics.items()}
        self.log_dict(metrics)  #, sync_dist=True))


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


def make_curv_transform(x, nbscales=7, nbangles=4):
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
        return out_data

    def curv_inv(x):
        # TODO make it work
        pass

    # TODO remove if not useful
    #curv_shape_by_feature = {
    #    s: {w: xc_sw.shape for w, xc_sw in enumerate(xc_s)}
    #    for s, xc_s in enumerate(xc)
    #}

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
