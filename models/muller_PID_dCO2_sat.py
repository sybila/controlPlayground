import numpy as np

# Define model
def model(x,t,dCO2_sat):
    # Constants
    kH_cp = 0.03
    P_in_atm = 1
    kB_b = 500000000
    kLa_CO2_eff = 29
    gCO2_in_ppm = 5000
    kB_f = 15.81
    kW_b = 2
    KW = 0.00000000000001
    k1_m_f = 8028000
    k1_m_b = 0.34956
    k2_m_f = 21600000000000
    k2_m_b = 1101600000
    k1_p_f = 133.56
    k1_p_b = 96120000
    k2_p_f = 213984
    k2_p_b = 180000000000000
    kW_f = 0.00000000000002

    # Output
    xdot = np.zeros(7)

    # Calculate derivatives
    # 0 = A_m
    # 1 = HA
    # 2 = OH_m
    # 3 = H_p
    # 4 = CO3_2m
    # 5 = HCO3_m
    # 6 = dCO2

    xdot[0] = + (kB_f*x[1]-kB_b*x[3] * x[0])
    xdot[1] = - (kB_f*x[1]-kB_b*x[3] * x[0])
    xdot[2] = - (k1_m_f*x[2] * x[6]-k1_m_b*x[5]) - (k2_m_f*x[2] * x[5]-k2_m_b*x[4]) + (kW_f-kW_b*x[2] * x[3])
    xdot[3] = + (k1_p_f*x[6]-k1_p_b*x[3] * x[5]) + (k2_p_f*x[5]-k2_p_b*x[3] * x[4]) + (kB_f*x[1]-kB_b*x[3] * x[0]) + (kW_f-kW_b*x[2] * x[3])
    xdot[4] = + (k2_m_f*x[2] * x[5]-k2_m_b*x[4]) + (k2_p_f*x[5]-k2_p_b*x[3] * x[4])
    xdot[5] = + (k1_m_f*x[2] * x[6]-k1_m_b*x[5]) + (k1_p_f*x[6]-k1_p_b*x[3] * x[5]) - (k2_m_f*x[2] * x[5]-k2_m_b*x[4]) - (k2_p_f*x[5]-k2_p_b*x[3] * x[4])
    xdot[6] = - (k1_m_f*x[2] * x[6]-k1_m_b*x[5]) - (k1_p_f*x[6]-k1_p_b*x[3] * x[5]) + (dCO2_sat * kLa_CO2_eff-kLa_CO2_eff*x[6])

    return xdot

# required constants and varaibles
VARS = ['A_m', 'HA', 'OH_m', 'H_p', 'CO3_2m', 'HCO3_m', 'dCO2']
plotting_vars = ['CO3_2m', 'dCO2']
SCALE = 1e6

# PID parameters
kP = 4.61730615181
kI = 40.4386149656
kD = 0.0

# Initial Conditions
x0 = np.empty(7)

x0[0] = 0.0075                  # A_m
x0[1] = 0.0075                  # HA
x0[2] = 3.16e-08                # OH_m
x0[3] = 0                       # H_p
x0[4] = 0                       # CO3_2m
x0[5] = 0                       # HCO3_m
x0[6] = 3.164556962025317e-07   # dCO2

# Initial Control Signal
u_ss = 0.00015

# Time Interval (min)
t = np.linspace(0,5,1000)

# Storage of results
observables = [np.ones(len(t)) * x0[i] for i in range(7)]
u = np.ones(len(t)) * u_ss

# set point
sp = np.zeros(len(t))
sp[0:] = u_ss
sp[100:200] = 0.000175
sp[200:] = 0.0002
