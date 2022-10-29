using JUDI, SegyIO, HDF5, PyPlot, Random, IterativeSolvers

modelName = "marmousi"
dataFolder = "../../data/"
mkpath(dataFolder)

# Load migration velocity model
if ~isfile("$(JUDI.JUDI_DATA)/marmousi_model.h5")
    ftp_data("ftp://slim.gatech.edu/data/SoftwareRelease/Imaging.jl/2DLSRTM/marmousi_model.h5")
end
n, d, o, m0 = read(h5open("$(JUDI.JUDI_DATA)/marmousi_model.h5", "r"), "n", "d", "o", "m0")
print(n)

# Set up model structure
model0 = Model((n[1], n[2]), (d[1], d[2]), (o[1], o[2]), m0)

# Load data
if ~isfile("$(JUDI.JUDI_DATA)/marmousi_2D.segy")
    ftp_data("ftp://slim.gatech.edu/data/SoftwareRelease/Imaging.jl/2DLSRTM/marmousi_2D.segy")
end
block = segy_scan(JUDI.JUDI_DATA, "marmousi_2D.segy", ["GroupX","GroupY","RecGroupElevation","SourceSurfaceElevation","dt"])
d_lin = judiVector(block)   # linearized observed data

# Set up wavelet
src_geometry = Geometry(block; key = "source", segy_depth_key = "SourceDepth")
wavelet = ricker_wavelet(src_geometry.t[1], src_geometry.dt[1], 0.03)    # 30 Hz wavelet
q = judiVector(src_geometry, wavelet)

###################################################################################################
# Infer subsampling based on free memory
mem = Sys.free_memory()/(1024^3)
t_sub = max(1, ceil(Int, 40/mem))
# Setup operators
opt = Options(subsampling_factor=t_sub, isic=true)  # ~40 GB of memory per source without subsampling
M = judiModeling(model0, q.geometry, d_lin.geometry; options=opt)
J = judiJacobian(M, q)

# Right-hand preconditioners (model topmute)
Mr = judiTopmute(model0.n, 52, 10)


#' set up number of iterations
nsrc = 5 * parse(Int, get(ENV, "NITER", "$(q.nsrc ÷ 5)"))
indsrc = randperm(q.nsrc)[1:nsrc]
lsqr_sol = zeros(Float32, prod(n))

# LSQR
dinv = d_lin[indsrc]
Jinv = J[indsrc]

Ml = judiMarineTopmute2D(30, dinv.geometry)

# print(d_lin.data[1])

lsqr_sol = zeros(Float32, prod(model0.n))
lsqr!(lsqr_sol, Ml*Jinv*Mr, Ml*dinv; maxiter=10)

# Save migrated image
h5open(dataFolder*"lsrtm_$(modelName).h5", "w") do file
    write(file, "m", reshape(lsqr_sol, model0.n))
    write(file, "d", collect((d[1], d[2])))
end

# Save remigrated image
h5open(dataFolder*"rtm_remig_$(modelName).h5", "w") do file
    write(file, "m", rtm_remig)
    write(file, "d", collect(d))
end
