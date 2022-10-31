using JUDI, SegyIO, HDF5, PyPlot, Random, LinearAlgebra

modelName = "marmousi"
domain = ARGS[1]
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
# Setup operators
opt = Options(isic=true)  # ~40 GB of memory per source without subsampling
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

reflectivity = read(h5open(dataFolder*"filtered_$(domain)_domain_image-$(modelName).h5", "r"), "m")

reflectivity = reshape(reflectivity, size(reflectivity)[1] * size(reflectivity)[2])

r = Jinv*Mr*reflectivity - Ml*dinv

residue = norm(r)^2

print(residue)

open("$(dataFolder)residue-$(domain)-marmousi.txt", "w") do file
    write(file, "$(residue)")
end
