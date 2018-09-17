from scipy.integrate import odeint
from scipy.integrate import ode

def exec_all(seq):
	for item in seq:
		exec(item, globals())

class Model():
	def __init__(self, x0, VARS, plotting_vars, SCALE, control_signal, REFERENCE, ODEs, parameters):
		self.x0 = x0
		self.VARS = VARS
		self.plotting_vars = plotting_vars
		self.SCALE = SCALE
		self.control_signal = control_signal
		self.REFERENCE = REFERENCE
		self.ODEs = ODEs
		self.parameters = parameters

	def calculateNextStep(self, ts, control_signal):
		return self.useLSODA(ts, control_signal)
		#return self.useLSODE(ts, control_signal)

	# Lsoda method
	def useLSODA(self, ts, control_signal):
		y = odeint(self.LSODAevaluateODEs, self.x0, ts, args=(control_signal,), rtol=1e-9, atol=1e-8)

		for j in range(len(self.VARS)):
			self.x0[j] = y[-1][j]

		return y[-1]

	def LSODAevaluateODEs(self, x, t, control_signal):
		exec_all(self.parameters)
		return map(eval, self.ODEs)

	# Lsode method
	def useLSODE(self, ts, control_signal):
		solver = ode(self.LSODEevaluateODEs).set_integrator('vode', method='BDF',
	                      order=4, rtol=0, atol=1e-6, with_jacobian=False)
		solver.set_initial_value(self.x0, ts[0]).set_f_params(control_signal)

		y = solver.integrate(ts[1])
		print(y)

		for j in range(len(self.VARS)):
			self.x0[j] = y[j]

		return y

	def LSODEevaluateODEs(self, t, x, control_signal):
		exec_all(self.parameters)
		return map(eval, self.ODEs)