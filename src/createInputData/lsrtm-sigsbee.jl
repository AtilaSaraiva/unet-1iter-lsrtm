# Generate observed linearized data for the Sigsbee2A velocity model
# Author: Philipp Witte, pwitte.slim@gmail.com
# Date: May 2018
#

# TO DO:
# Replace w/ full path the directory where the observed data will be stored
dataFolder = "../../data/"
modelName = "sigsbee2A"
mkpath(dataFolder)
data_name="sigsbee2A_marine"

using JUDI, PyPlot, JLD, SegyIO, HDF5, Random, IterativeSolvers

# Load Sigsbee model
if !isfile("$(dataFolder)vel_$(modelName)-down.h5")
    run(`wget ftp://slim.gatech.edu/data/SoftwareRelease/Imaging.jl/CompressiveLSRTM/sigsbee2A_model.jld`)
    include("create-sigsbee-hdf5.jl")
    run(`python downscale.py infile="$(dataFolder)vel_sigsbee2A.h5" fx=0.5 fy=1.`)
end
n, d, o, m0, dm = read(h5open("$(dataFolder)vel_$(modelName)-down.h5", "r"), "n", "d", "o", "m0", "dm")

# Setup model structure
model0 = Model((n[1], n[2]), (d[1], d[2]), (o[1], o[2]), m0)
dm = vec(dm)

# Load data
container = segy_scan(dataFolder, data_name, ["GroupX","GroupY","RecGroupElevation","SourceSurfaceElevation","dt"])
d_lin = judiVector(container)

# Set up source
src_geometry = Geometry(container; key="source")
wavelet = ricker_wavelet(src_geometry.t[1], src_geometry.dt[1], 0.015)  # 15 Hz peak frequency
q = judiVector(src_geometry, wavelet)

#################################################################################################
# Infer subsampling based on free memory
mem = Sys.free_memory()/(1024^3)
t_sub = max(1, ceil(Int, 40/mem))
# Setup operators
opt = Options(subsampling_factor=t_sub, isic=true)  # ~40 GB of memory per source without subsampling

# Setup operators
Pr = judiProjection(d_lin.geometry)
F0 = judiModeling(model0; options=opt)
Ps = judiProjection(src_geometry)
J = judiJacobian(Pr*F0*Ps', q)

# Right-hand preconditioners (model topmute)
idx_wb = find_water_bottom(reshape(dm, model0.n))
Tm = judiTopmute(model0.n, idx_wb, 10)  # Mute water column
S = judiDepthScaling(model0)
Mr = S*Tm

lsqr_sol = zeros(Float32, prod(model0.n))

niter=10
fval = zeros(Float32, niter)
# Main loop

z = zeros(Float32, prod(model0.n))
batchsize = 100
niter = 20
fval = zeros(Float32, niter)
t = 2f-5

for j=1:niter
    println("Iteration: ", j)

    # Compute residual and gradient
    i = randperm(d_lin.nsrc)[1:batchsize]
    d_sub = get_data(d_lin[i])    # load shots into memory

    # Compute residual and gradient
    r = J[i]*Mr*lsqr_sol - d_sub
    g = Mr'*J[i]'*r

    # Step size and update variable
    fval[j] = norm(r)^2
    isempty(t) && (global t = norm(r)^2/norm(g)^2)

    # Update variables and save snapshot
    global lsqr_sol -= t*g
end

print(fval)

# Save migrated image
h5open(dataFolder*"lsrtm_$(modelName).h5", "w") do file
    write(file, "m", reshape(lsqr_sol, model0.n))
    write(file, "d", collect((d[1], d[2])))
end
