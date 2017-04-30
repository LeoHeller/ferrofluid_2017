import pigpio
import time
from time import sleep # in s

pins_pwm=[4,17,27,22] 
pins_pol=[18,23,24,25] 

mag_value=[0,0,0,0]

FREQ=20000 # The PWM cycles per second.

#pwm pins:
PWM1=4
PWM2=17
PWM3=27
PWM4=22
GPIO=[PWM1, PWM2, PWM3, PWM4]

_channels = len(GPIO)

_dc=[0]*_channels

_micros=int(1000000/FREQ)

old_wid = None

pi = pigpio.pi()

def setup():
    # Setup PWM 
    if not pi.connected:
         exit(0)
    
    # Need to explicity set wave GPIO to output mode.
    for g in GPIO:
        pi.set_mode(g, pigpio.OUTPUT)


    # polarity pins are outputs:
    for pin in pins_pol:
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.write(pin, 0)  
        # defined as output
        # all output off

def set_dc(channel, dc):

   if dc < 0:
      dc = 0
   elif dc > _micros:
      dc = _micros

   _dc[channel] = dc


def start_dc():

   global old_wid

   for c in range(_channels):
      d = _dc[c]
      g = GPIO[c]
      if d == 0:
         pi.wave_add_generic([pigpio.pulse(0, 1<<g, _micros)])
      elif d == _micros:
         pi.wave_add_generic([pigpio.pulse(1<<g, 0, _micros)])
      else:
         pi.wave_add_generic(
            [pigpio.pulse(1<<g, 0, d), pigpio.pulse(0, 1<<g, _micros-d)])

   new_wid = pi.wave_create()

   if old_wid is not None:

      pi.wave_send_using_mode(new_wid, pigpio.WAVE_MODE_REPEAT_SYNC)

      # Spin until the new wave has started.
      while pi.wave_tx_at() != new_wid:
         pass

      # It is then safe to delete the old wave.
      pi.wave_delete(old_wid)

   else:

      pi.wave_send_repeat(new_wid)

   old_wid = new_wid



def set_and_start_dc(channel, dc):

   global old_wid

   if dc < 0:
      dc = 0
   elif dc > _micros:
      dc = _micros

   _dc[channel] = dc


   for c in range(_channels):
      d = _dc[c]
      g = GPIO[c]
      if d == 0:
         pi.wave_add_generic([pigpio.pulse(0, 1<<g, _micros)])
      elif d == _micros:
         pi.wave_add_generic([pigpio.pulse(1<<g, 0, _micros)])
      else:
         pi.wave_add_generic(
            [pigpio.pulse(1<<g, 0, d), pigpio.pulse(0, 1<<g, _micros-d)])

   new_wid = pi.wave_create()

   if old_wid is not None:

      pi.wave_send_using_mode(new_wid, pigpio.WAVE_MODE_REPEAT_SYNC)

      # Spin until the new wave has started.
      while pi.wave_tx_at() != new_wid:
         pass

      # It is then safe to delete the old wave.
      pi.wave_delete(old_wid)

   else:

      pi.wave_send_repeat(new_wid)

   old_wid = new_wid


def all_off():
    for pin in pins_pol:
        pi.write(pin, 0)

    for nummer in range(4):
        set_dc (nummer, 0)
        mag_value[nummer]=0
    start_dc()

def main():
    try:
        setup()

    finally:
        # turn all pins off
        all_off()
        pi.stop()

def setup():
    # Setup PWM 
    pi = pigpio.pi()
    if not pi.connected:
         exit(0)
    
    # Need to explicity set wave GPIO to output mode.
    for g in GPIO:
        pi.set_mode(g, pigpio.OUTPUT)


    # polarity pins are outputs:
    for pin in pins_pol:
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.write(pin, 0)  
        # defined as output
        # all output off


def clear():
    all_off()
    pi.stop()
        

def magnet(nummer, staerke, polaritaet):
    if not ((0 <= nummer <=3) and (0<= staerke <= 100) and (0<= polaritaet <=1)):
        #fehler
        print("magnet: falscher Parameter. Magnet=" + str(nummer) + ", Staerke=" + str(staerke) + ", Polaritaet=" + str(polaritaet))
        return -1

    set_dc(nummer,int(staerke * 10000/FREQ))

    mag_value[nummer] = staerke

    pi.write(pins_pol[nummer], polaritaet)
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

    set_dc(nummer,int(staerke * 10000/FREQ))
    mag_value[nummer] = staerke
    return 0

def pol(nummer,polaritaet):
    if not ((0 <= nummer <=3) and  (0<= polaritaet <=1)):
        print("magnet: falscher Parameter. Magnet=" + str(nummer) + ", Polaritaet=" + str(polaritaet))
        return -1
    set_dc(nummer, 0)  # magnet abschalten, bevor wir die Polaritaet umschalten
    sleep(.1)
    pi.write(pins_pol[nummer], polaritaet)    
    sleep(.1)
    set_dc(nummer,int(mag_value[nummer]*10000/FREQ))  # magnet wieder auf vorherige Staerke schalten
    return 0

if __name__ == "__main__":
    main()
