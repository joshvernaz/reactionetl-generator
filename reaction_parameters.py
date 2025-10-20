from math import pi

# Ideal gas constant
R = 8.314 # J mol^-1 K^-1

# Pre-exponential factor
# Borovinskaya, E. et al. (2019) Experimental Studies of Ethyl Acetate Saponification Using Different Reactor Systems ... Applied Sciences, 2019, 9(3)
Ar = 10 * 10**6 / 1000 # m^3 mol^-1 s^-1

# Enthalpy of reaction at 298 K
# NIST (Ethyl Acetate, Ethanol) and Argonne's Active Thermochemical Tables (Hydroxide Ion, Acetate Ion)
DH_Rx_298 = -50210 # J mol^-1

# Activation energy
# Borovinskaya, E. et al. (2019) Experimental Studies of Ethyl Acetate Saponification Using Different Reactor Systems ... Applied Sciences, 2019, 9(3)
Ea = 45380 # J mol^-1

# Reaction vessel dimensions and parameters
DIAMETER = 0.0635 # m, Interior
HEIGHT = 0.316 # m, Interior
THICKNESS = 0.005 # m
AREA = pi * (DIAMETER + 2 * THICKNESS) * (HEIGHT + 2 * THICKNESS) + pi * (DIAMETER + 2 * THICKNESS)**2 / 2
VOLUME = pi * (DIAMETER/2)**2 * HEIGHT # m^3, Interior
Tcool = 295 # K, jacket water maintained at this temperature

# Heat transfer coefficients
THERMAL_CONDUCTIVITY = 1.1 # W m^-1 K^-1
h_i = 500 # W m^-2 K^-1, Interior convection
h_o = 1000 # W m^-2 K^-1, Exterior convection
U = (1/h_i + THICKNESS/THERMAL_CONDUCTIVITY + 1/h_o)**-1
UA = U * AREA # W K^-1
UA_V = UA / VOLUME # Appears as a constant in dT/dt

# Heat capacity (BULK) at constant pressure - treat constant w.r.t temperature
# Assuming water heat capacity dominates
CP = 4100 # J kg^-1 K^-1

# Density
rho = 1050 # kg m^-3
