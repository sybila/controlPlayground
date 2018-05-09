import time

class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0):

        self.kP = P
        self.kI = I
        self.kD = D
        self.old_feedback = 0
        self.old_ie = 0
        self.old_time = 0

    def update(self, feedback, set_point, time):
        delta_t = time - self.old_time
        error = set_point - feedback                    # error

        dpv = (feedback - self.old_feedback)/delta_t    # derivative of the pv
        ie = self.old_ie + error * delta_t              # integral of the error

        P = self.kP * error
        I = self.kI * ie
        D = self.kD * dpv

        self.old_feedback  = feedback
        self.old_ie = ie
        self.old_time = time

        return P + I + D #+ op