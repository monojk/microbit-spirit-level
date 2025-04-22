""" Tabelle für y und z
         Winkel
    vorn        rechts      x       y       z   Steigung
    ----------------------------------------------------
    0° (horizontal)  0°     0       0   -1040        0 %
    45°              0°     0     720    -720      100 %
    90°(vertikal)    0°     0    1040       0      inf %
    ----------------------------------------------------
    0°              90°  1024       0       0
    45°             90°   720     720       0
    90°             90°     0    1024       0
"""

from microbit import *
from math import atan, degrees, tan, radians

calibrate = 0
what = 1

class KalmanFilter:
    def __init__(self, init_estimate=0.0):
        self.process_var = 1e-4
        self.measurement_var = 0.3
        self.estimate = init_estimate
        self.error_covar = 1

    def update(self, measurement):
        kalman_gain = self.error_covar / (self.error_covar + self.measurement_var)
        self.estimate += kalman_gain * (measurement - self.estimate)
        self.error_covar = (1 - kalman_gain) * self.error_covar
        +self.process_var
        return self.estimate


def calc_mean_3d_accel(accel_data_3d, init_estimate_x, init_estimate_y, init_estimate_z):
    # Create Kalman filters for x, y, z
    kf_x = KalmanFilter(init_estimate_x)
    kf_y = KalmanFilter(init_estimate_y)
    kf_z = KalmanFilter(init_estimate_z)
    filtered_x, filtered_y, filtered_z = [], [], []

    # print("Raw -> Filtered")
    for x, y, z in accel_data_3d:
        fx = kf_x.update(x)
        fy = kf_y.update(y)
        fz = kf_z.update(z)
        filtered_x.append(fx)
        filtered_y.append(fy)
        filtered_z.append(fz)
        # print(
        #     "X: %.2f -> %.2f, Y: %.2f -> %.2f, Z: %.2f -> %.2f" % (x, fx, y, fy, z, fz)
        # )
    # Calculate means
    m_x = sum(filtered_x) / len(filtered_x)
    m_y = sum(filtered_y) / len(filtered_y)
    m_z = sum(filtered_z) / len(filtered_z)
    # print("\nMean Acceleration:\n X: %.3f, Y: %.3f, Z: %.3f" % (m_x, m_y, m_z))
    return m_x, m_y, m_z


x = y = z = 0
iterations = 50
while True:
    init_x = x
    init_y = y
    init_z = z
    accel_data = []
    for i in range(iterations):
        accel_data.append( (accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z()) )
    #    sleep(1)
    x, y, z = calc_mean_3d_accel(accel_data, init_x, init_y, init_z)

    if (z - x) == 0:
        Steigung = 999
        Winkel = 90
    else:
        Steigung = int(-y / (z - x) * 100)
        Winkel = int(degrees(atan(-y / (z - x))))
    if button_a.was_pressed():
        calibrate = Winkel
    elif button_b.was_pressed():
        what = -what
    FinalWinkel = Winkel - calibrate
    FinalSteigung = int(tan(radians(FinalWinkel)) * 100)
    print(
        "x={0}  y={1}  z={2}  Steigung={3}%  Winkel={4}  FinalWinkel={5}  FinalSteigung={6}%".format(
            x, y, z, Steigung, Winkel, FinalWinkel, FinalSteigung
        )
    )
    if what < 0:
        display.scroll("{0}".format(FinalWinkel))
    else:
        display.scroll("{0}%".format(FinalSteigung))
    sleep(500)

display.clear()
