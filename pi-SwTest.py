import RPi.GPIO as GPIO
import time

mainCTL_SW = 27
mainEMG_SW = 22
ir_sw = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(ir_sw, GPIO.IN)
GPIO.setup(mainCTL_SW, GPIO.IN)
GPIO.setup(mainEMG_SW, GPIO.IN)

while True:
    print('GPIO',ir_sw,GPIO.input(ir_sw))
    print('GPIO',mainCTL_SW,GPIO.input(mainCTL_SW))
    print('GPIO',mainEMG_SW,GPIO.input(mainEMG_SW))
    time.sleep(1)

GPIO.cleanup()