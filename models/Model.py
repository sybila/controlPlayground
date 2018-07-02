from scipy.integrate import odeint

class Model():
	def __init__(self, x0, VARS, plotting_vars, SCALE, control_signal, observables, REFERENCE, ODEs):
		self.x0 = x0
		self.VARS = VARS
		self.plotting_vars = plotting_vars
		self.SCALE = SCALE
		self.control_signal = control_signal
		self.observables = observables
		self.REFERENCE = REFERENCE
		self.ODEs = ODEs

	def evaluateODEs(self, x, t, control_signal):
		return map(eval, self.ODEs)

	def calculateNextStep(self, ts, control_signal):
		y = odeint(self.evaluateODEs, self.x0, ts, args=(control_signal,))

		for j in range(len(self.VARS)):
			self.x0[j] = y[-1][j]

		return y[-1]

