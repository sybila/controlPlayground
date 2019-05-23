import numpy as np

# required constants and variables
VARS = ['A_m', 'HA', 'OH_m', 'H_p', 'CO3_2m', 'HCO3_m', 'dCO2']
plotting_vars = ['CO3_2m', 'dCO2']
SCALE = 1e6

# Initial Conditions
x0 = np.empty(7)

x0[0] = 0.0075  # A_m
x0[1] = 0.0075  # HA
x0[2] = 3.16e-08  # OH_m
x0[3] = 0  # H_p
x0[4] = 0  # CO3_2m
x0[5] = 0  # HCO3_m
x0[6] = 3.164556962025317e-07  # dCO2

# Storage of results
# signals = [(0, 5000), (2, 4000), (3, 3999), (4, 3000), (5, 2500)]
# solver fails with more then 2 changes, WHY?

# PID parameters
kP = 8.86
kI = 0.05
kD = 0.0125

# set point
set_points = [(0, 0.00015)]  # , (2, 0.00012)]

# reference variable
REFERENCE = 6

# ODEs
ODEs = ["(kB_f*x[1]-kB_b*x[3] * x[0])",
        "- (kB_f*x[1]-kB_b*x[3] * x[0])",
        "- (k1_m_f*x[2] * x[6]-k1_m_b*x[5]) - (k2_m_f*x[2] * x[5]-k2_m_b*x[4]) + (kW_f-kW_b*x[2] * x[3])",
        "+ (k1_p_f*x[6]-k1_p_b*x[3] * x[5]) + (k2_p_f*x[5]-k2_p_b*x[3] * x[4]) + (kB_f*x[1]-kB_b*x[3] * x[0]) + (kW_f-kW_b*x[2] * x[3])",
        "+ (k2_m_f*x[2] * x[5]-k2_m_b*x[4]) + (k2_p_f*x[5]-k2_p_b*x[3] * x[4])",
        "+ (k1_m_f*x[2] * x[6]-k1_m_b*x[5]) + (k1_p_f*x[6]-k1_p_b*x[3] * x[5]) - (k2_m_f*x[2] * x[5]-k2_m_b*x[4]) - (k2_p_f*x[5]-k2_p_b*x[3] * x[4])",
        "- (k1_m_f*x[2] * x[6]-k1_m_b*x[5]) - (k1_p_f*x[6]-k1_p_b*x[3] * x[5]) + ((kH_cp*control_signal*P_in_atm)/1e+6 * kLa_CO2_eff-kLa_CO2_eff*x[6])"]
parameters = ['kH_cp = 0.03', 'P_in_atm = 1', 'kB_b = 500000000',
              'kLa_CO2_eff = 29', 'kB_f = 15.81', 'kW_b = 2',
              'KW = 0.00000000000001', 'k1_m_f = 8028000', 'k1_m_b = 0.34956',
              'k2_m_f = 21600000000000', 'k2_m_b = 1101600000', 'k1_p_f = 133.56',
              'k1_p_b = 96120000', 'k2_p_f = 213984', 'k2_p_b = 180000000000000',
              'kW_f = 0.00000000000002']
