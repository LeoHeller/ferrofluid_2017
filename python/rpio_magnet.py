import RPIO
from RPIO import PWM
import time
from time import sleep # in s

pins_pwm=[4,17,27,22] 
pins_pol=[18,23,24,25] 

mag_value=[0,0,0,0]


# PWM pins:
servo = PWM.Servo()

def all_off():
    for pin in pins_pol:
        RPIO.output(pin, False)

    for pin in pins_pwm:
        servo.set_servo(pin, 0) #set PWM pin to off

    mag_value=[0,0,0,0]


def main():
    try:
        setup()

    finally:
        # turn all pins off
        all_off()

def setup():
    # Setup PWM and DMA channel 0
    PWM.set_loglevel(1)
    print("Set loglevel\n")
    # PWM.setup()
    PWM.init_channel(0)

    # polarity pins are outputs:
    for pin in pins_pol:
        RPIO.setup(pin, RPIO.OUT, initial=RPIO.LOW)
        # defined as output
        # all output off

    for pin in pins_pwm:
      # Set servo on GPIO17 to 0 us. 20ms is one PWM period.
      servo.set_servo(pin, 0) #define pin as pwm output

    # all magnets turned off
    magnet(0,0,0)
    magnet(1,0,0)
    magnet(2,0,0)
    magnet(3,0,0)


def magnet(nummer, staerke, polaritaet):
    if not ((0 <= nummer <=3) and (0<= staerke <= 100) and (0<= polaritaet <=1)):
        #fehler
        print("magnet: falscher Parameter. Magnet=" + str(nummer) + ", Staerke=" + str(staerke) + ", Polaritaet=" + str(polaritaet))
        return -1

    servo.set_servo(pins_pwm[nummer], staerke*200)

    mag_value[nummer] = staerke

    RPIO.output(pins_pol[nummer], polaritaet)
    return 0

def mag_st(nummer, staerke):
    if staerke < 0:
        staerke = 0
    if staerke > 100:
        staerke = 100
    if not ((0 <= nummer <=3) and (0<= staerke <= 100)):
        #fehler
        print("mag_st: falscher Parameter. Magnet=" + str(nummer) + ", Staerke=" + str(staerke))
        return -1

    servo.set_servo(pins_pwm[nummer], staerke*200)
    mag_value[nummer] = staerke
    return 0

def pol(nummer,polaritaet):
    if not ((0 <= nummer <=3) and  (0<= polaritaet <=1)):
        print("magnet: falscher Parameter. Magnet=" + str(nummer) + ", Polaritaet=" + str(polaritaet))
        return -1

    servo.set_servo(pins_pwm[nummer], 0) # magnet abschalten, bevor wir die Polaritaet umschalten
    sleep(.1)
    RPIO.output(pins_pol[nummer], polaritaet)
    sleep(.1)
    servo.set_servo(pins_pwm[nummer], mag_value[nummer]*200) # magnet wieder auf vorherige Staerke schalten
    return 0

if __name__ == "__main__":
    main()
