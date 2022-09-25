using JUDI, PyPlot, LinearAlgebra, HDF5

# Load marmousi model
if ~isfile("$(JUDI.JUDI_DATA)/marmousi_model.h5")
    ftp_data("ftp://slim.gatech.edu/data/SoftwareRelease/Imaging.jl/2DLSRTM/marmousi_model.h5")
end

# Load overthrust model
if ~isfile("$(JUDI.JUDI_DATA)/overthrust_model_2D.h5")
    ftp_data("ftp://slim.gatech.edu/data/SoftwareRelease/WaveformInversion.jl/2DFWI/overthrust_model_2D.h5")
end
