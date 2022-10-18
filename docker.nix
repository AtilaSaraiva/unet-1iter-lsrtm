{ sources ? import ./nix/sources.nix }:
with import sources.nixpkgs {
  config.allowUnfree = true;
  overlays = [
    (import sources.myNixPythonPackages)
  ];
};

let
  my-python-packages = python-packages: with python-packages; [
    matplotlib
    devito
    curvelops
    pytorch
    pytorch-lightning
    h5py
    tiler
    scikit-learn
    # other python packages you want
  ];
  python-with-my-packages = python3.withPackages my-python-packages;
in
  dockerTools.streamLayeredImage {
    name = "unetenv";
    tag = "latest";
    contents = [
      python-with-my-packages
      jupyter
      julia-bin
      gcc
      bash
      coreutils
    ];
    maxLayers=128;
    enableFakechroot = true;
    config = {
      Cmd = [
        "${bash}/bin/bash"
      ];
      Env = [
        "DEVITO_LOGGING=DEBUG"
        "DEVITO_ARCH=gcc"
        "DEVITO_LANGUAGE=openmp"
      ];
      WorkingDir = "/data";
      Volumes = {
        "/data" = {};
      };
    };
  }
