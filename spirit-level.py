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
from math     import atan, degrees, tan, radians

calibrate  = 0
what       = 1
iterations = 100

while True:
    x = y = z = 0
    for i in range(iterations):
        x += accelerometer.get_x()
        y += accelerometer.get_y()
        z += accelerometer.get_z()
        sleep(1)
    x = x / iterations
    y = y / iterations
    z = z / iterations
    if (z-x) == 0 :
        Steigung = 999
        Winkel   = 90
    else :
        Steigung = int( - y / (z-x) * 100 )
        Winkel   = int(degrees(atan( - y / (z-x) )))
    if button_a.was_pressed() :
        calibrate = Winkel
    elif button_b.was_pressed():
        what = -what
    FinalWinkel = Winkel - calibrate
    FinalSteigung = int(tan(radians(FinalWinkel))*100)
    print("x={0}  y={1}  z={2}  Steigung={3}%  Winkel={4}  FinalWinkel={5}  FinalSteigung={6}%".format(x, y, z, Steigung, Winkel, FinalWinkel, FinalSteigung))
    if what < 0 :
        display.scroll("{0}".format(FinalWinkel))
    else :
        display.scroll("{0}%".format(FinalSteigung))
    sleep(500)

display.clear()
