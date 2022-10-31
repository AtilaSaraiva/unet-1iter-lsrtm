import numpy as np
from tile_dataset import *
import h5py
from unet import UNet
import torch
import torch.nn.functional as F
import pytorch_lightning as pl
from sklearn.preprocessing import RobustScaler, MaxAbsScaler
import os
import json
from pytorch_lightning.loggers import CSVLogger
from plot import plotloss

scaler = RobustScaler()

class TrainSetup(pl.LightningModule):

    def __init__(self,
                 model: torch.nn.Module,
                 train_loader: torch.utils.data.DataLoader,
                 test_loader: torch.utils.data.DataLoader = None,
                 val_loader: torch.utils.data.DataLoader = None,
                 learning_rate: float = 0.005,
                 weight_decay: float = 0.5,
                 lagrange_multiplier: float = 0.2):
        super().__init__()
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader or self.train_loader
        self.val_loader = val_loader or self.test_loader
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.multiplier = lagrange_multiplier

    def train_dataloader(self):
        return self.train_loader

    def val_dataloader(self):
        return self.val_loader

    def test_dataloader(self):
        return self.test_loader

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate, weight_decay=self.weight_decay)
        return optimizer

    def training_step(self, batch, batch_idx):
        X, Y = batch
        Y_pred = self.model(X)
        loss =  F.mse_loss(Y, Y_pred)
        return loss

    def validation_step(self, batch, batch_idx):
        loss = self.training_step(batch, batch_idx)
        metrics = {"loss": loss}
        # metrics = {f"val_{k}": v for k, v in metrics.items()}
        self.log_dict(metrics)  #, sync_dist=True))


def main(param):
    dataFolder = os.environ["DATADIR"]
    rtm_file = h5py.File(dataFolder + f"rtm_{param['model']}.h5")
    rtm_dset = rtm_file["m"]

    rtmRemig_file = h5py.File(dataFolder + f"rtm_remig_{param['model']}.h5")
    rtmRemig_dset = rtmRemig_file["m"]

    X, Y = extract_patches(rtmRemig_dset, rtm_dset, patch_num=param["patch_num"], patch_size=param["patch_size"])

    cutoff = int(0.8*param["patch_num"])
    X_train, X_test = X[:cutoff,:,:,:], X[cutoff:,:,:,:]
    Y_train, Y_test = Y[:cutoff,:,:,:], Y[cutoff:,:,:,:]

    train_dataset = torch.utils.data.TensorDataset(X_train, Y_train)
    test_dataset = torch.utils.data.TensorDataset(X_test, Y_test)

    print(param)

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=5, num_workers=20)  #, prefetch_factor=3, num_workers=3)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=5, num_workers=20)  #, prefetch_factor=3, num_workers=3)

    model = UNet(ndim=2, in_channels=1, out_channels=1, patch_size=param["patch_size"], norm=False)

    train_setup = TrainSetup(
        model,
        train_loader=train_loader,
        test_loader=test_loader,
        learning_rate=param["lr"],
        weight_decay=param["weight_decay"]
    )

    logger = CSVLogger("logs", name=f"space_domain_{param['model']}")
    trainer = pl.Trainer(
        max_epochs=param["epochs"],
        limit_train_batches=50,
        logger=logger
    )
    trainer.fit(train_setup)

    # plotloss(param, domain = "space")

    modeldir = os.environ['MODELDIR']
    torch.save(model.state_dict(), modeldir + f"spaceUnet-{param['model']}.pt")

if __name__ == "__main__":
    with open("dataconf/spaceDomain/marmousi.json", "r") as arq:
        marmousi = json.load(arq)
    main(marmousi)
