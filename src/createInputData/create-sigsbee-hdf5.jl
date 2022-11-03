using JUDI, JLD, HDF5

dataFolder = "../../data/"
modelName = "sigsbee2A"

# Load Sigsbee model
if !isfile("sigsbee2A_model.jld")
    run(`wget ftp://slim.gatech.edu/data/SoftwareRelease/Imaging.jl/CompressiveLSRTM/sigsbee2A_model.jld`)
end
M = load("sigsbee2A_model.jld")

# Save the velocity model image
h5open(dataFolder*"vel_$(modelName).h5", "w") do file
    write(file, "m0", M["m0"])
    write(file, "dm", M["dm"])
    write(file, "n", collect(M["n"]))
    write(file, "d", collect(M["d"]))
    write(file, "o", collect(M["o"]))
end
