using JUDI, PyPlot, LinearAlgebra, HDF5

close("all")

dataFolder = "../../data/"
mkpath(dataFolder)

function createData(v, v0, n, d, o, nsrc, dtD, timeD, muteRow, modelName)

    dm = vec(m0 - m)
    # Setup model structure
    # nsrc = n[1]/10	# number of sources
    # nsrc = 10	# number of sources
    model = Model(n, d, o, m)
    model0 = Model(n, d, o, m0)

    # Set up receiver geometry
    nxrec = n[1]
    xrec = range(0f0, stop=(n[1]-1)*d[1], length=nxrec)
    yrec = 0f0 # We have to set the y coordiante to zero (or any number) for 2D modeling
    zrec = range(d[1], stop=d[1], length=nxrec)

    # receiver sampling and recording time
    # timeD = 3000f0   # receiver recording time [ms]
    # dtD = 2f0        # receiver sampling interval [ms]

    # Set up receiver structure
    recGeometry = Geometry(xrec, yrec, zrec; dt=dtD, t=timeD, nsrc=nsrc)

    xsrc = convertToCell(range(0f0, stop=(n[1]-1)*d[1], length=nsrc))
    ysrc = convertToCell(range(0f0, stop=0f0, length=nsrc))
    zsrc = convertToCell(range(d[1], stop=d[1], length=nsrc))

    # Set up source geometry (cell array with source locations for each shot)
    xsrc = convertToCell(range(0f0, stop=(n[1]-1)*d[1], length=nsrc))
    ysrc = convertToCell(range(0f0, stop=0f0, length=nsrc))
    zsrc = convertToCell(range(d[1], stop=d[1], length=nsrc))

    # Set up source structure
    srcGeometry = Geometry(xsrc, ysrc, zsrc; dt=dtD, t=timeD)

    # setup wavelet
    f0 = 0.01f0     # kHz
    wavelet = ricker_wavelet(timeD, dtD, f0)
    q = judiVector(srcGeometry, wavelet)

    # Setup options
    opt = Options(subsampling_factor=2, dt_comp=1.0)

    # Setup operators
    Pr = judiProjection(recGeometry)
    F = judiModeling(model; options=opt)
    F0 = judiModeling(model0; options=opt)
    Ps = judiProjection(srcGeometry)
    J = judiJacobian(Pr*F0*adjoint(Ps), q)

    #' # Model and image data

    #' We first model synthetic data using our defined source and true model
    # Nonlinear modeling
    dobs = Pr*F*adjoint(Ps)*q

    #' Plot the shot record
    fig = figure()
    imshow(dobs.data[1], vmin=-1, vmax=1, cmap="PuOr", extent=[xrec[1], xrec[end], timeD/1000, 0], aspect="auto")
    xlabel("Receiver position (m)")
    ylabel("Time (s)")
    title("Synthetic data")
    display(fig)

    # Linearized modeling J*dm
    dD = J*dm

    # Adjoint jacobian, RTM image
    rtm = adjoint(J)*dD
    rtm[:, 1:muteRow] .= 0.0

    #' We show the linearized data.
    fig = figure()
    imshow(dD.data[1], cmap="PuOr", extent=[xrec[1], xrec[end], timeD/1000, 0], aspect="auto")
    xlabel("Receiver position (m)")
    ylabel("Time (s)")
    title("Linearized data")
    display(fig)

    #' And the RTM image
    fig = figure()
    imshow(rtm', cmap="Greys", extent=[0, (n[1]-1)*d[1], (n[2]-1)*d[2], 0 ], aspect="auto")
    xlabel("Lateral position(m)")
    ylabel("Depth (m)")
    title("RTM image")
    display(fig)

    d_calc = J*rtm

    rtm_remig = adjoint(J)*d_calc

    #' We show the linearized data.
    fig = figure()
    imshow(d_calc.data[1], cmap="PuOr", extent=[xrec[1], xrec[end], timeD/1000, 0], aspect="auto")
    xlabel("Receiver position (m)")
    ylabel("Time (s)")
    title("Modeled data from the migrated image")
    display(fig)


    #' And the RTM image
    fig = figure()
    imshow(rtm_remig', cmap="Greys", extent=[0, (n[1]-1)*d[1], (n[2]-1)*d[2], 0 ], aspect="auto")
    xlabel("Lateral position(m)")
    ylabel("Depth (m)")
    title("RTM image")
    display(fig)

    # Save migrated image
    h5open(dataFolder*"rtm_$(modelName).h5", "w") do file
        write(file, "m", rtm.data)
        write(file, "d", collect(d))
    end

    # Save remigrated image
    h5open(dataFolder*"rtm_remig_$(modelName).h5", "w") do file
        write(file, "m", rtm_remig.data)
        write(file, "d", collect(d))
    end

    show()
end

# Single Layer model

n = (300, 200)   # (x,y,z) or (x,z)
d = (10., 10.)
o = (0., 0.)

# Velocity [km/s]
v = ones(Float32,n) .+ 0.5f0
v0 = ones(Float32,n) .+ 0.5f0
v[:,Int(round(end/2)):end] .= 3.5f0

# Save velocity field
h5open(dataFolder*"vel.h5", "w") do file
    write(file, "m", reshape(v, n))
    write(file, "d", collect(d))
end
imshow(v')

# nsrc = 50
# timeD = 3000f0   # receiver recording time [ms]
# dtD = 2f0        # receiver sampling interval [ms]

# # Slowness squared [s^2/km^2]
# m  = (1f0 ./ v).^2
# m0 = (1f0 ./ v0).^2

# # createData(m, m0, n, d, o, nsrc, dtD, timeD, 40, "two_layers")


# # Load marmousi model
# if ~isfile("$(JUDI.JUDI_DATA)/marmousi_model.h5")
    # ftp_data("ftp://slim.gatech.edu/data/SoftwareRelease/Imaging.jl/2DLSRTM/marmousi_model.h5")
# end
# n, d, o, m0, m = read(h5open("$(JUDI.JUDI_DATA)/marmousi_model.h5", "r"), "n", "d", "o", "m0", "m")

# nsrc = 800
# timeD = 3000f0   # receiver recording time [ms]
# dtD = 2          # receiver sampling interval [ms]

# n = (n[1], n[2])
# d = (d[1], d[2])
# o = (o[1], o[2])

# print(n)
# # createData(m, m0, n, d, o, nsrc, dtD, timeD, 40, "marmousi")


# # Load overthrust model
# if ~isfile("$(JUDI.JUDI_DATA)/overthrust_model_2D.h5")
    # ftp_data("ftp://slim.gatech.edu/data/SoftwareRelease/WaveformInversion.jl/2DFWI/overthrust_model_2D.h5")
# end
# n, d, o, m0, m = read(h5open("$(JUDI.JUDI_DATA)/overthrust_model_2D.h5", "r"), "n", "d", "o", "m0", "m")

# nsrc = 400
# timeD = 3000f0   # receiver recording time [ms]
# dtD = 2          # receiver sampling interval [ms]

# n = (n[1], n[2])
# d = (d[1], d[2])
# o = (o[1], o[2])

# print(n)
# # createData(m, m0, n, d, o, nsrc, dtD, timeD, 19, "overthrust")
