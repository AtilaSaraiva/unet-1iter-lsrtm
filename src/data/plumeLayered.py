from devito import

shape = (101, 101)  # Number of grid point (nx, nz)
spacing = (10., 10.)  # Grid spacing in m. The domain size is now 1km by 1km
origin = (0., 0.)  # What is the location of the top left corner. This is necessary to define

fpeak = 0.025# Source peak frequency is 25Hz (0.025 kHz)
t0w = 1.0 / fpeak
omega = 2.0 * np.pi * fpeak
qmin = 0.1
qmax = 100000
npad=50
dtype = np.float32

nshots = 21
nreceivers = 101
t0 = 0.
tn = 1000.  # Simulation last 1 second (1000 ms)
filter_sigma = (5, 5) # Filter's length

v = np.empty(shape, dtype=dtype)

# Define a velocity profile. The velocity is in km/s
vp_top = 1.5

v[:] = vp_top # Top velocity 
v[:, 30:65]= vp_top +0.5
v[:, 65:101]= vp_top +1.5
v[40:60, 35:55]= vp_top+1

init_damp = lambda func, nbl: setup_w_over_q(func, omega, qmin, qmax, npad, sigma=0)
model = Model(vp=v, origin=origin, shape=shape, spacing=spacing,
              space_order=8, bcs=init_damp,nbl=npad,dtype=dtype)
model0 = Model(vp=v, origin=origin, shape=shape, spacing=spacing,
              space_order=8, bcs=init_damp,nbl=npad,dtype=dtype)

dt = model.critical_dt 
s = model.grid.stepping_dim.spacing
time_range = TimeAxis(start=t0, stop=tn, step=dt)
nt=time_range.num
