import numpy as np
import torch


conv_for_dim = {
    1: torch.nn.Conv1d,
    2: torch.nn.Conv2d,
    3: torch.nn.Conv3d,
}

pool_for_dim = {
    1: torch.nn.AvgPool1d,
    2: torch.nn.AvgPool2d,
    3: torch.nn.AvgPool3d,
}

norm_for_dim = {
    1: torch.nn.BatchNorm1d,
    2: torch.nn.BatchNorm2d,
    3: torch.nn.BatchNorm3d,
}

drop_for_dim = {
    1: torch.nn.Dropout,
    2: torch.nn.Dropout2d,
    3: torch.nn.Dropout3d,
}


class Encoder(torch.nn.Module):

    def __init__(
        self,
        ndim=1,
        in_channels=1,
        out_channels=1,
        nconvs=3,
        kernel_size=3,
        activation=None,
        norm=False,
    ):
        super().__init__()

        self.norms = torch.nn.ModuleList() if norm else None
        self.convs = torch.nn.ModuleList()

        for step in range(nconvs):
            if step == 0:
                _in_channels = in_channels
            else:
                _in_channels = out_channels

            if norm:
                self.norms.append(norm_for_dim[ndim](_in_channels))

            self.convs.append(conv_for_dim[ndim](
                _in_channels,
                out_channels,
                kernel_size,
                stride=1,
                padding='same',
            ))

        if activation:
            self.activation = activation()
        else:
            self.activation = lambda x: x

    def forward(self, x, norm=None):
        norm = norm or True

        for step in range(len(self.convs)):
            if self.norms and norm:
                x = self.norms[step](x)
            x = self.convs[step](x)
            x = self.activation(x)

        return x

class Decoder(torch.nn.Module):

    def __init__(
        self,
        ndim=1,
        in_channels=1,
        out_channels=1,
        nconvs=2,
        kernel_size=3,
        activation=None,
        norm=False,
    ):
        super().__init__()

        self.norms = torch.nn.ModuleList() if norm else None
        self.convs = torch.nn.ModuleList()

        for step in range(nconvs):
            if step == 0:
                _in_channels = in_channels + out_channels
            else:
                _in_channels = out_channels

            if norm:
                self.norms.append(norm_for_dim[ndim](_in_channels))

            self.convs.append(conv_for_dim[ndim](
                _in_channels,
                out_channels,
                kernel_size,
                stride=1,
                padding='same',
            ))

        if activation:
            self.activation = activation()
        else:
            self.activation = lambda x: x

    def forward(self, x, x_old, norm=None):
        norm = norm or True

        x = torch.nn.functional.interpolate(x, x_old.shape[2:], mode="nearest-exact")
        x = torch.concat([x_old, x], dim=1)

        for step in range(len(self.convs)):
            if self.norms and norm:
                x = self.norms[step](x)
            x = self.convs[step](x)
            x = self.activation(x)

        return x


class MultiScaleEncoder(torch.nn.Module):

    def __init__(
        self,
        ndim=1,
        in_channels=1,
        nscales=5,
        nconvs_by_scale=2,
        kernel_size=3,
        activation=None,
        norm=False,
        dropout=False,
    ):
        super().__init__()

        self._nscales = nscales

        self.encoders = torch.nn.ModuleList()

        _in_channels = in_channels
        for scale in range(self._nscales):
            _out_channels = in_channels * 2 ** (scale)
            encoder = Encoder(
                ndim=ndim,
                in_channels=_in_channels,
                out_channels=_out_channels,
                nconvs=nconvs_by_scale,
                kernel_size=kernel_size,
                activation=activation,
                norm=norm)
            self.encoders.append(encoder)

            _in_channels = _out_channels


        self.pool = pool_for_dim[ndim](kernel_size=3, stride=2, padding=1)

        if dropout:
            self.dropout = drop_for_dim[ndim](dropout)
        else:
            self.dropout = lambda x: x

    def forward(self, x, get_scale=None, train=False, return_old=False):
        old = []

        for scale in range(self._nscales):
            x = self.encoders[scale](x)

            if scale == get_scale:
                return x

            if scale < self._nscales-1:
                old.append(x)
                x = self.pool(x)

        if train:
            x = self.dropout(x)

        if return_old:
            return x, old
        else:
            return x


class MultiScaleDecoder(torch.nn.Module):

    def __init__(
        self,
        ndim=1,
        in_channels=1,
        nscales=5,
        nconvs_by_scale=2,
        kernel_size=3,
        activation=None,
        norm=False,
    ):
        super().__init__()

        self._nscales = nscales

        self.decoders = torch.nn.ModuleList()

        _in_channels = in_channels
        for scale in range(self._nscales-1):
            _out_channels = in_channels // (2 ** (scale+1))
            decoder = Decoder(
                ndim=ndim,
                in_channels=_in_channels,
                out_channels=_out_channels,
                nconvs=nconvs_by_scale,
                kernel_size=kernel_size,
                activation=activation,
                norm=norm)
            self.decoders.append(decoder)

            _in_channels = _out_channels
        self.decoders = self.decoders[::-1]

    def forward(self, x, old):
        for scale in range(self._nscales-2, -1 ,-1):
            x_old = old.pop()
            x = self.decoders[scale](x, x_old)  # CONCAT!!!, in_channels
        return x


class UNet(torch.nn.Module):

    def __init__(
        self,
        ndim=1,
        in_channels=1,
        out_channels=1,
        nscales=5,
        nconvs_by_scale=2,
        base_channels=8,
        kernel_size=3,
        activation=torch.nn.ReLU,
        first_activation=None,
        last_activation=None,
        norm=False,
        dropout=False,
        norm_at_start=False,
        nconvs_bottom=None,
        use_skip_connections=True,
        return_encoders=False,
        verbose=False,
    ):
        super().__init__()

        last_activation = last_activation or activation
        first_activation = first_activation or activation

        if first_activation:
            self.first_activation = first_activation()
        else:
            self.first_activation = lambda x: x

        if norm_at_start:
            input_norm = norm_for_dim[ndim](in_channels)

        self.to_base_channels = conv_for_dim[ndim](
                in_channels,
                base_channels,
                kernel_size,
                stride=1,
                padding='same',
        )

        self.global_encoder = MultiScaleEncoder(
            ndim=ndim,
            in_channels=base_channels,
            nscales=nscales,
            nconvs_by_scale=nconvs_by_scale,
            kernel_size=kernel_size,
            activation=activation,
            norm=norm,
            dropout=dropout,
        )

        deep_channels = base_channels * 2 ** (nscales-1)

        self.global_decoder = MultiScaleDecoder(
            ndim=ndim,
            in_channels=deep_channels,
            nscales=nscales,
            nconvs_by_scale=nconvs_by_scale,
            kernel_size=kernel_size,
            activation=activation,
            norm=norm,
        )

        self.to_out_channels = conv_for_dim[ndim](
            base_channels,
            out_channels,
            kernel_size,
            stride=1,
            padding='same',
        )

        if last_activation:
            self.last_activation = last_activation()
        else:
            self.last_activation = lambda x: x

    def forward(self, x):
        x = self.to_base_channels(x)
        x = self.first_activation(x)
        x, old = self.global_encoder(x, return_old=True)
        x = self.global_decoder(x, old)
        x = self.to_out_channels(x)
        x = self.last_activation(x)
        return x


if __name__ == "__main__":
    X = torch.rand((2, 2, 32, 32, 32))
    unet = Unet(ndim=3, in_channels=2, out_channels=2, norm=False)
    Y = unet(X)
    print(Y.shape)
