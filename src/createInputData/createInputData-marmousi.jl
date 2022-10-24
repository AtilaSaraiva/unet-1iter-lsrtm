using JUDI, SegyIO, HDF5, PyPlot, Random

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

seed!(1234)

#' set up number of iterations
niter = parse(Int, get(ENV, "NITER", "10"))
# Default to 64, 5 for CI only with NITER=1
nsrc = 5 * parse(Int, get(ENV, "NITER", "$(q.nsrc ÷ 5)"))
indsrc = randperm(q.nsrc)[1:nsrc]
lsqr_sol = zeros(Float32, prod(n))

# LSQR
dinv = d_lin[indsrc]
Jinv = J[indsrc]

Ml = judiMarineTopmute2D(30, dinv.geometry)

# print(d_lin.data[1])

rtm = adjoint(Ml*Jinv*Mr)*dinv
d_calc = Ml*Jinv*Mr*rtm
rtm_remig = adjoint(Ml*Jinv*Mr)*d_calc

rtm = reshape(rtm, (n[1], n[2]))
rtm_remig = reshape(rtm_remig, (n[1], n[2]))

# Save migrated image
h5open(dataFolder*"rtm_$(modelName).h5", "w") do file
    write(file, "m", rtm)
    write(file, "d", collect(d))
end

# Save remigrated image
h5open(dataFolder*"rtm_remig_$(modelName).h5", "w") do file
    write(file, "m", rtm_remig)
    write(file, "d", collect(d))
end

#' And the RTM image
fig = figure()
imshow(rtm', cmap="Greys", extent=[0, (n[1]-1)*d[1], (n[2]-1)*d[2], 0 ], aspect="auto")
imshow(rtm_remig', cmap="Greys", extent=[0, (n[1]-1)*d[1], (n[2]-1)*d[2], 0 ], aspect="auto")
xlabel("Lateral position(m)")
ylabel("Depth (m)")
title("RTM image")
savefig("rtm.png", dpi=300)
display(fig)
