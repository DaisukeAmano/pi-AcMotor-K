import RPi.GPIO as GPIO # RPi.GPIOモジュールを使用
import time
import sys

# LEDとスイッチのGPIO番号
# デフォルトはRPZ-IR-Sensorの緑LEDと赤SW
# 必要に応じて変更
relay_mainIO = 17
relay_dirIO = 27
ir_sw = 22

# GPIO番号指定の準備
GPIO.setmode(GPIO.BCM)

# LEDピンを出力に設定
GPIO.setup(relay_mainIO, GPIO.OUT)
GPIO.setup(relay_dirIO, GPIO.OUT)

#待機時間配列とりあえずなし

# スイッチピンを入力、プルアップに設定
GPIO.setup(ir_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
objCount = 0
dirStatus = False

while True:
    try:
        #Start motor
        GPIO.output(relay_mainIO, 1)
        #untill 3 objects detected
        while objCount<3:
            # スイッチの状態を取得
            sw = GPIO.input(ir_sw)
            # 非検出
            if sw==0:
                #increment count
                objCount+=1
                print(objCount)
                time.sleep(2)
                #if objCount<3:
                    #time.sleep(2)
            else:
                GPIO.output(relay_dirIO, dirStatus)
                time.sleep(0.1)

        #Change direction
        dirStatus = not dirStatus
        GPIO.output(relay_mainIO, 0)
        GPIO.output(relay_dirIO, dirStatus)
        print('Change direction')
        print(dirStatus)
        #reset objCount
        objCount=0
        #decelerating motor
        time.sleep(2)

    except KeyboardInterrupt:               #Ctrl+Cキーが押された
        GPIO.cleanup()                      #GPIOをクリーンアップ
        print('EXIT')
        sys.exit()