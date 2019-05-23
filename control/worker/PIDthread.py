import threading


class ControllThread(threading.Thread):
    def __init__(self, set_points, output, control_signal, current_time, REFERENCE, PID, set_point):
        super(ControllThread, self).__init__()
        self.set_points = set_points
        self.output = output
        self.control_signal = control_signal
        self.current_time = current_time
        self.REFERENCE = REFERENCE
        self.PID = PID
        self.old_time = 0
        self.set_point = set_point
        self.stoprequest = threading.Event()

    def run(self):
        while not self.stoprequest.isSet():
            observed_value = self.output[0][1][self.REFERENCE]
            self.set_point[0] = self.calculateSetPoint()
            time = self.current_time[0]
            if self.old_time != time:
                if time > 0.01:
                    print("observed_value: ", observed_value, " | set_point: ",
                          self.set_point[0], " | time: ", time)
                    signal = self.PID.update(observed_value, self.set_point[0], time)
                    print("signal: ", signal / 3e-8)
                    self.control_signal[0] = signal / 3e-8
            self.old_time = time

    def calculateSetPoint(self):
        for t, s in reversed(self.set_points):
            if self.current_time[0] > t:
                return s

    def join(self, timeout=None):
        self.stoprequest.set()
        super(ControllThread, self).join(timeout)
