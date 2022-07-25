import torch
import torch.nn.functional as F
import pytorch_lightning as pl
from unet import UNet


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


if __name__ == "__main__":
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
