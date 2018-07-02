import numpy as np

# required constants and variables
VARS = ['A_m', 'HA', 'OH_m', 'H_p', 'CO3_2m', 'HCO3_m', 'dCO2']
plotting_vars = ['CO3_2m', 'dCO2']
SCALE = 1e6

# Initial Conditions
x0 = np.empty(7)

x0[0] = 0.0075                  # A_m
x0[1] = 0.0075                  # HA
x0[2] = 3.16e-08                # OH_m
x0[3] = 0                       # H_p
x0[4] = 0                       # CO3_2m
x0[5] = 0                       # HCO3_m
x0[6] = 3.164556962025317e-07   # dCO2

# Time Interval (min)
t = np.linspace(0,5,1000)

# Storage of results
observables = [np.ones(len(t)) * x0[i] for i in range(7)]
controls = zip(t, np.append(np.ones(500) * 2500, np.ones(len(t) - 500) * 5000))

# set point
sp = np.zeros(len(t))
sp[0:] = 1000*3e-8
sp[200:400] = 0.000175
sp[400:] = 0.0002

# reference variable
REFERENCE = 6

# ODEs
ODEs = ["+ (15.81*x[1]-500000000*x[3] * x[0])",
    	"- (15.81*x[1]-500000000*x[3] * x[0])",
        "- (8028000*x[2] * x[6]-0.34956*x[5]) - (21600000000000*x[2] * x[5]-1101600000*x[4]) + (0.00000000000002-2*x[2] * x[3])",
    	"+ (133.56*x[6]-96120000*x[3] * x[5]) + (213984*x[5]-180000000000000*x[3] * x[4]) + (15.81*x[1]-500000000*x[3] * x[0]) + (0.00000000000002-2*x[2] * x[3])",
    	"+ (21600000000000*x[2] * x[5]-1101600000*x[4]) + (213984*x[5]-180000000000000*x[3] * x[4])",
    	"+ (8028000*x[2] * x[6]-0.34956*x[5]) + (133.56*x[6]-96120000*x[3] * x[5]) - (21600000000000*x[2] * x[5]-1101600000*x[4]) - (213984*x[5]-180000000000000*x[3] * x[4])",
    	"- (8028000*x[2] * x[6]-0.34956*x[5]) - (133.56*x[6]-96120000*x[3] * x[5]) + ((0.03*control_signal[0])/1e+6 * 29-29*x[6])"]