{ sources ? import ./nix/sources.nix }:
with import sources.nixpkgs {
  overlays = [
    (import (builtins.fetchTarball https://github.com/AtilaSaraiva/myNixPythonPackages/archive/main.tar.gz))
  ];
};

let
  my-python-packages = python-packages: with python-packages; [
    matplotlib
    devito
    curvelops
    pytorch
    pytorch-lightning
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
