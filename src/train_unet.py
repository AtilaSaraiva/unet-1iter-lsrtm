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
    return 


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


if __name__ == "__main__":
    nbscales = 7
    nbangles_coarse = 4

    patch_num = 1000
    patch_size = 50
    stride_z = 20
    stride_x = 20
    val_split = 0.2
    lr = 0.01


    X = torch.empty((200, 200))
    Y = torch.empty((200, 200))
    shape = X.shape

    DCT = FDCT2D(shape, nbscales=nbscales, nbangles_coarse=nbangles_coarse)

    c_X = DCT * X.ravel()
    cr_X = DCT.struct(c_X)

    # unsqueeze to 4D
    X = X[None, None, :, :]
    Y = X[None, None, :, :]

    contador = 0
    shapes = []
    for s in range(len(cr_X)):
        for w in range(len(cr_X[s])):
            shapes.append((1, *cr_X[s][w].shape))

    main_input = [torch.empty((1, *shape), dtype=torch.float32) for shape in shapes]
    main_output = [torch.empty((1, *shape), dtype=torch.float32) for shape in shapes]

    contador = 0
    curvAux = DCT * X[0,0].ravel()
    exit()
    curvAux = DCT.struct(curvAux)
    for s in range(len(curvAux)):
        for w in range(len(curvAux[s])):
            t = threshold(np.abs(curvAux[s][w]), 1e-6)
            print(t)
            #main_input[contador][0,:,:] = threshold(np.abs(curvAux[s][w]), 1e-6)
            #contador += 1

    exit()
    contador = 0
    curvAux = DCT * Y.ravel()
    curvAux = DCT.struct(curvAux)
    for s in range(len(curvAux)):
        for w in range(len(curvAux[s])):
            print(main_output[contador])
            # main_output[contador][0,:,:] = threshold(np.abs(curvAux[s][w]),1e-6)
            # contador += 1


    scaleThat(main_input)
    scaleThat(main_output)

    model =  CurveletFilter(shapes)
    print(model(main_input))
    exit()
    #history = model.fit(main_input, main_output,
    #                    epochs=10,
    #                    callbacks=ClearMemory(),
    #                    batch_size=1)
    #                    # validation_split=0.2)


