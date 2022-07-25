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
mkShell {
  buildInputs = [
    python-with-my-packages
    jupyter
  ];

  shellHooks = ''
    export DEVITO_LOGGING=DEBUG
    export DEVITO_ARCH="gcc"
    export DEVITO_LANGUAGE="openmp"
  '';
}
