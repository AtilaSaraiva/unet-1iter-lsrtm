import numpy as np
from tile_dataset import *
import h5py
from matplotlib import pyplot as plt
from unet import UNet
import torch
import torch.nn.functional as F
import pytorch_lightning as pl
from sklearn.preprocessing import RobustScaler, MaxAbsScaler
from typing import Callable
from trainUnetClass import CurveletFilter, make_curv_transform
import os


class TrainSetup(pl.LightningModule):

    def __init__(self,
                 model: torch.nn.Module,
                 transform: Callable,
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
        self.transform = transform


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
        residue = torch.tensor(0, dtype=torch.float32)
        for x, y in zip(X, Y):
            xc = tuple([torch.from_numpy(i) for i in self.transform(x[0])])
            yc = tuple([torch.from_numpy(i) for i in self.transform(y[0])])
            yc_pred = self.model(xc)
            for i in range(len(yc_pred)):
                residue += F.mse_loss(yc[i], yc_pred[i])
        loss = residue / len(X)
        return loss

    def validation_step(self, batch, batch_idx):
        X, Y = batch
        residue = torch.tensor(0, dtype=torch.float32)
        for x, y in zip(X, Y):
            xc = tuple([torch.from_numpy(i) for i in self.transform(x[0])])
            yc = tuple([torch.from_numpy(i) for i in self.transform(y[0])])
            yc_pred = self.model(xc)
            for i in range(len(yc_pred)):
                residue += F.mse_loss(yc[i], yc_pred[i])
        loss = residue / len(X)
        metrics = {"loss": loss}
        metrics = {f"val_{k}": v for k, v in metrics.items()}
        self.log_dict(metrics)  #, sync_dist=True))

scaler = RobustScaler()

dataFolder = os.environ["DATADIR"]
rtm_file = h5py.File(dataFolder + "rtm_marmousi.h5")
rtm_dset = rtm_file["m"]
scaler_mig = scaler.fit(rtm_dset)
rtm_norm = scaler_mig.transform(rtm_dset)

rtmRemig_file = h5py.File(dataFolder + "rtm_remig_marmousi.h5")
rtmRemig_dset = rtmRemig_file["m"]
scaler_remig = scaler.fit(rtmRemig_dset)
rtmRemig_norm = scaler_remig.transform(rtmRemig_dset)

X, Y = extract_patches(rtmRemig_norm, rtm_norm, patch_num=600, patch_size=32)

X_train, X_test = X[:500,:,:,:], X[500:,:,:,:]
Y_train, Y_test = Y[:500,:,:,:], Y[500:,:,:,:]

curv_fwd, curv_inv, curv_shapes = make_curv_transform(X[0,0])

train_dataset = torch.utils.data.TensorDataset(X_train, Y_train)
test_dataset = torch.utils.data.TensorDataset(X_test, Y_test)

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=5, num_workers=20)  #, prefetch_factor=3, num_workers=3)
test_loader = torch.utils.data.DataLoader(train_dataset, batch_size=5, num_workers=20)  #, prefetch_factor=3, num_workers=3)

#model = UNet(ndim=2, in_channels=1, out_channels=1, norm=False)
model =  CurveletFilter(curv_shapes)

train_setup = TrainSetup(
    model,
    transform=curv_fwd,
    train_loader=train_loader,
    test_loader=test_loader,
    learning_rate=0.005,
)

trainer = pl.Trainer(max_epochs=50, limit_train_batches=50)
trainer.fit(train_setup)

modeldir = os.environ['MODELDIR']
torch.save(model.state_dict(), modeldir + "curveletUnet.pt")
