FROM nixos/nix

COPY *.toml /app/
COPY *.nix /app/
COPY nix /app/nix

WORKDIR /app

RUN nix-env -f shell.nix -i -A buildInputs

ENV DEVITO_LOGGING=DEBUG
ENV DEVITO_ARCH="gcc"
ENV DEVITO_LANGUAGE="openmp"
ENV JULIA_DEPOT_PATH="/julia"
ENV MODELDIR=$PWD/models/
ENV DATADIR=$PWD/data/

RUN julia -e 'using Pkg; Pkg.activate("."); Pkg.instantiate()'
