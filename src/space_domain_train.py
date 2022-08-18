import numpy as np
from tile_dataset import *
import h5py
from matplotlib import pyplot as plt
from unet import UNet
import torch
import torch.nn.functional as F
import pytorch_lightning as pl
from sklearn.preprocessing import RobustScaler, MaxAbsScaler
import os

epochs = 30
scaler = RobustScaler()

class TrainSetup(pl.LightningModule):

    def __init__(self,
                 model: torch.nn.Module,
                 train_loader: torch.utils.data.DataLoader,
                 test_loader: torch.utils.data.DataLoader = None,
                 val_loader: torch.utils.data.DataLoader = None,
                 learning_rate: float = 0.005,
                 weight_decay: float = 0.5):
        super().__init__()
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader or self.train_loader
        self.val_loader = val_loader or self.test_loader
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay

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
        metrics = {f"val_{k}": v for k, v in metrics.items()}
        self.log_dict(metrics)  #, sync_dist=True))


dataFolder = os.environ["DATADIR"]
rtm_file = h5py.File(dataFolder + "rtm.h5")
rtm_dset = rtm_file["m"]
scaler_mig = scaler.fit(rtm_dset)
rtm_norm = scaler_mig.transform(rtm_dset)

rtmRemig_file = h5py.File(dataFolder + "rtm_remig.h5")
rtmRemig_dset = rtmRemig_file["m"]
scaler_remig = scaler.fit(rtmRemig_dset)
rtmRemig_norm = scaler_remig.transform(rtmRemig_dset)

# plt.imshow(rtmRemig_norm)
# plt.savefig("rtmremig.pdf")
# plt.show()
# plt.imshow(rtm_norm)
# plt.savefig("rtm.pdf")
# plt.show()

X, Y = extract_patches(rtmRemig_norm, rtm_norm, patch_num=250, patch_size=32)

X_train, X_test = X[:200,:,:,:], X[200:,:,:,:]
Y_train, Y_test = Y[:200,:,:,:], Y[200:,:,:,:]

train_dataset = torch.utils.data.TensorDataset(X_train, Y_train)
test_dataset = torch.utils.data.TensorDataset(X_test, Y_test)

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=5, num_workers=20)  #, prefetch_factor=3, num_workers=3)
test_loader = torch.utils.data.DataLoader(train_dataset, batch_size=5, num_workers=20)  #, prefetch_factor=3, num_workers=3)

model = UNet(ndim=2, in_channels=1, out_channels=1, norm=False)

train_setup = TrainSetup(
    model,
    train_loader=train_loader,
    test_loader=test_loader,
    learning_rate=0.005,
    weight_decay=0.01
)

trainer = pl.Trainer(max_epochs=epochs, limit_train_batches=50)
trainer.fit(train_setup)

modeldir = os.environ['MODELDIR']
torch.save(model.state_dict(), modeldir + "spaceUnet.pt")
