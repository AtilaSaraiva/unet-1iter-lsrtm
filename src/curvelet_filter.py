from typing import Any, Sequence
from dataclasses import dataclass
import torch
from unet import UNet
import numpy as np


@dataclass
class CurveletFilter(torch.nn.Module):
    shapes: Sequence[int]

    def __post_init__(self, base_channels=16):
        super().__init__()

        self.models = torch.nn.ModuleList()
        self._models = []

        for shape in self.shapes:
            min_dim = min(*shape[1:3])
            nscales = min(int(np.log2(min_dim) - 1), 3)

            if nscales >= 1:
                unet = UNet(
                    ndim=2,
                    in_channels=1,
                    out_channels=1,
                    nscales=nscales,
                    base_channels=base_channels,
                    activation=torch.nn.Tanh,
                    first_activation=torch.nn.Tanh,
                    last_activation=torch.nn.Tanh,
                )
                self.models.append(unet)
                self._models.append(unet)
            else:
                self._models.append((lambda x: x))

    def forward(self, xs):
        ys = []
        for model, x in zip(self._models, xs):
            y = model(x)
            ys.append(y)
        return ys

if __name__ == '__main__':
    pass
