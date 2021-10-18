import RPi.GPIO as GPIO # RPi.GPIOモジュールを使用
import time
import sys

# LEDとスイッチのGPIO番号
# デフォルトはRPZ-IR-Sensorの緑LEDと赤SW
# 必要に応じて変更


inverter_STF = 23
inverter_STR = 24
ir_sw = 17

# GPIO番号指定の準備
GPIO.setmode(GPIO.BCM)

# LEDピンを出力に設定
GPIO.setup(inverter_STF, GPIO.OUT)
GPIO.setup(inverter_STR, GPIO.OUT)

# スイッチピンを入力、プルアップに設定
GPIO.setup(ir_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#物体検知設定・初期化
objectsNum = 3
objCount = 0
dirSTF = True
dirSTR = False

while True:
    try:
        #Start motor
        GPIO.output(inverter_STF, dirSTF)
        GPIO.output(inverter_STR, dirSTR)
        #untill 3 objects detected
        while objCount<objectsNum:
            # スイッチの状態を取得
            sw = GPIO.input(ir_sw)
            # 非検出
            if sw==1:
                #increment count
                objCount+=1
                print(objCount)
                if objCount<objectsNum:
                    time.sleep(1)

            else:
                time.sleep(0.1)

        #Change direction
        dirSTF = not dirSTF
        dirSTR = not dirSTR
        #stop inverter
        GPIO.output(inverter_STF, False)
        GPIO.output(inverter_STR, False)
        print('Change direction')
        print('STF', dirSTF, 'STR', dirSTR)
        #reset objCount
        objCount=0
        #decelerating motor
        time.sleep(2)

    except KeyboardInterrupt:               #Ctrl+Cキーが押された
        GPIO.output(inverter_STF, False)
        GPIO.output(inverter_STR, False)
        GPIO.cleanup()                      #GPIOをクリーンアップ
        print('EXIT')
        sys.exit()