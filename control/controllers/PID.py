import time


class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0):
        self.kP = P
        self.kI = I
        self.kD = D
        self.prev_observed_value = 0
        self.prev_ie = 0
        self.prev_time = 0

    def update(self, observed_value, set_point, time):
        # print(observed_value, set_point, time)
        delta_t = time - self.prev_time
        error = set_point - observed_value  # error
        print("error: ", error)

        dpv = (observed_value - self.prev_observed_value) / delta_t  # derivative of the pv
        ie = self.prev_ie + error * delta_t  # integral of the error

        P = self.kP * error
        I = self.kI * ie
        D = self.kD * dpv

        self.prev_observed_value = observed_value
        self.prev_ie = ie
        self.prev_time = time

        """
        u(t) = kP * error(t) + kI * (ie[0, t-1] + ie(t)*dt) + kD * (pv(t) - pv(t-1))/dt
        """
        return P + I + D
