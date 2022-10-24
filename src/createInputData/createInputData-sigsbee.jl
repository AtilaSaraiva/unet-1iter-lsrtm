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

using JUDI, PyPlot, JLD, SegyIO

# Load Sigsbee model
if !isfile("sigsbee2A_model.jld")
    run(`wget ftp://slim.gatech.edu/data/SoftwareRelease/Imaging.jl/CompressiveLSRTM/sigsbee2A_model.jld`)
end
M = load("sigsbee2A_model.jld")

# Setup model structure
model0 = Model(M["n"], M["d"], M["o"], M["m0"])
dm = vec(M["dm"])

# Load data
container = segy_scan(dataFolder, data_name, ["GroupX","GroupY","RecGroupElevation","SourceSurfaceElevation","dt"])
d_lin = judiVector(container)

# Set up source
src_geometry = Geometry(container; key="source")
wavelet = ricker_wavelet(src_geometry.t[1], src_geometry.dt[1], 0.015)  # 15 Hz peak frequency
q = judiVector(src_geometry, wavelet)

#################################################################################################

opt = Options(isic=true, optimal_checkpointing=true)

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

rtm = adjoint(J*Mr)*d_lin
rtm_remig = adjoint(J*Mr)*J*Mr*rtm

rtm = reshape(rtm, M["n"])
rtm_remig = reshape(rtm_remig, M["n"])

# Save migrated image
h5open(dataFolder*"rtm_$(modelName).h5", "w") do file
    write(file, "m", rtm)
    write(file, "d", collect(M["d"]))
end

# Save remigrated image
h5open(dataFolder*"rtm_remig_$(modelName).h5", "w") do file
    write(file, "m", rtm_remig)
    write(file, "d", collect(M["d"]))
end
