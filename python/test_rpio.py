import RPIO
from RPIO import PWM
import time
from time import sleep # in s

pins_pwm=[4,17,27,22] 
pins_pol=[18,23,24,25]

# Setup PWM and DMA channel 0
PWM.setup()
PWM.init_channel(0)


servo = PWM.Servo()
# Set servo on GPIO17 to 1200µs (1.2ms)
servo.set_servo(27, 12000)

time.sleep(1000)

