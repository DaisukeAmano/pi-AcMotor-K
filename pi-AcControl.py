#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO # RPi.GPIOモジュールを使用
import time
import sys

# LEDとスイッチのGPIO番号
# デフォルトはRPZ-IR-Sensorの緑LEDと赤SW
# 必要に応じて変更

#停止・緊急停止ピン
mainCTL_SW = 27
mainEMG_SW = 22

#光電センサ
ir_sw = 17

#インバータ制御用ピン
inverter_STF = 23
inverter_STR = 24

#割り込み検知用変数
mainEMG = False

def main():
    # GPIO番号指定の準備
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)

    # 出力に設定
    GPIO.setup(inverter_STF, GPIO.OUT)
    GPIO.setup(inverter_STR, GPIO.OUT)

    # GPIO SETUP
    GPIO.setup(ir_sw, GPIO.IN)
    GPIO.setup(mainCTL_SW, GPIO.IN)
    GPIO.setup(mainEMG_SW, GPIO.IN)

    # 割り込みsetup
    GPIO.add_event_detect(mainEMG_SW, GPIO.FALLING, callback=callback, bouncetime=1000)

    #物体検知設定・初期化
    objectsNum = 3
    objCount = 0
    dirSTF = True
    dirSTR = False
    global mainEMG

    print('====MAIN====')
    while True:
        try:
            mainCTL = GPIO.input(mainCTL_SW)
            if mainCTL==1 and mainEMG==False:
                print('START')
                #Start motor
                GPIO.output(inverter_STF, dirSTF)
                GPIO.output(inverter_STR, dirSTR)
                #untill 3 objects detected
                while objCount<objectsNum:
                    mainCTL = GPIO.input(mainCTL_SW)
                    if mainCTL==0 or mainEMG==True:
                        print('STOP')
                        break
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
                if mainCTL==1:       
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
            elif(mainCTL==0 and mainEMG==True):
                mainEMG = False
                print('RESET')
            else:
                GPIO.output(inverter_STF, False)
                GPIO.output(inverter_STR, False)

        except KeyboardInterrupt:               #Ctrl+Cキーが押された
            GPIO.output(inverter_STF, False)
            GPIO.output(inverter_STR, False)
            GPIO.cleanup()                      #GPIOをクリーンアップ
            print('BREAK')
            sys.exit()

def callback(channel):
    global mainEMG
    mainEMG = True
    print("EMG STOP DETECTED")

if __name__ == "__main__":
    main()