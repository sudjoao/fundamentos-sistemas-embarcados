import RPi.GPIO as GPIO
import time

semaforos_outputs = [[1, 26, 21], [20, 16, 12]]
botoes_pedestres = [8, 7]
estados = ['001001', '100001', '010001', '001001', '001100', '001010', '001001']


def turn_on_lights(current_state):
    if current_state == '001001':
        GPIO.output(semaforos_outputs[0][0], GPIO.LOW)
        GPIO.output(semaforos_outputs[1][0], GPIO.LOW)
        GPIO.output(semaforos_outputs[0][2], GPIO.HIGH)
        GPIO.output(semaforos_outputs[1][2], GPIO.HIGH)
    elif current_state == '100001':
        GPIO.output(semaforos_outputs[0][2], GPIO.LOW)
        GPIO.output(semaforos_outputs[0][0], GPIO.HIGH)
    elif current_state == '010001':
        GPIO.output(semaforos_outputs[0][0], GPIO.LOW)
        GPIO.output(semaforos_outputs[0][1], GPIO.HIGH)
    elif current_state == '001100': 
        GPIO.output(semaforos_outputs[1][2], GPIO.LOW)
        GPIO.output(semaforos_outputs[1][0], GPIO.HIGH)
    elif current_state == '001010':
        GPIO.output(semaforos_outputs[1][0], GPIO.LOW)
        GPIO.output(semaforos_outputs[1][1], GPIO.HIGH)
    

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([1, 26, 21, 20, 16, 12], GPIO.OUT)
    GPIO.setup(botoes_pedestres, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    i = 0
    while i < 5:
        for estado in estados:
            print(estado)
            turn_on_lights(estado)
            time.sleep(1)
        i+=1
    GPIO.cleanup()

main()