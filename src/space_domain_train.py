import numpy as np
from tile_dataset import *
import h5py
from matplotlib import pyplot as plt
from trainUnetClass import TrainSetup
from unet import UNet
import torch
import torch.nn.functional as F
import pytorch_lightning as pl
from sklearn.preprocessing import RobustScaler, MaxAbsScaler
import os

dataFolder = os.environ["DATADIR"]
rtm_file = h5py.File(dataFolder + "rtm.h5")
rtm_dset = rtm_file["m"]
scaler_mig = MaxAbsScaler().fit(rtm_dset)
rtm_norm = scaler_mig.transform(rtm_dset)

rtmRemig_file = h5py.File(dataFolder + "rtm_remig.h5")
rtmRemig_dset = rtmRemig_file["m"]
scaler_remig = MaxAbsScaler().fit(rtmRemig_dset)
rtmRemig_norm = scaler_remig.transform(rtmRemig_dset)

X, Y = extract_patches(rtmRemig_norm, rtm_norm, patch_num=600, patch_size=32)

X_train, X_test = X[:500,:,:,:], X[500:,:,:,:]
Y_train, Y_test = Y[:500,:,:,:], Y[500:,:,:,:]

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
)

trainer = pl.Trainer(max_epochs=10, limit_train_batches=50)
trainer.fit(train_setup)

modeldir = os.environ['MODELDIR']
torch.save(model.state_dict(), modeldir + "spaceUnet.pt")
