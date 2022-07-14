import RPi.GPIO as GPIO
import time

output_list = [10, 9, 11]
button_list = [5, 6, 18, 20, 26]

def output_logic(option):
    #A) Acionar os LEDs ligando e desligando individualmente;
    #B) Acionar os LEDs em sequência (temporizada) do primeiro ao último ligando um por um, depois dois a dois, ...
    #C) Acionar os LEDs de um determinado grupo (1, 2, 3 ou 4) de modo a simular um sinal de trânisto temporizado.
    if option == 'a':
        for output in output_list:
            print(f"ligou o {output}")
            GPIO.output(output, GPIO.HIGH)
            time.sleep(1)
            print(f"desligou o {output}")
            GPIO.output(output, GPIO.LOW)
    elif option == 'b':
        for output in output_list:
            GPIO.output(output, GPIO.HIGH)
            time.sleep(1)
        for output in output_list:
            GPIO.output(output, GPIO.LOW)
            time.sleep(1)
        time.sleep(1)
        for i in range(len(output_list)-1):
            GPIO.output((output_list[i], output_list[i+1]), GPIO.HIGH)
            time.sleep(1)
            GPIO.output((output_list[i], output_list[i+1]), GPIO.LOW)
        time.sleep(1)
    else:
        GPIO.output(10, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(10, GPIO.LOW)

def pwm(option):
    #A) Acionar um LED individualmente oscilando sua intensidade de 0% a 100% e em seguida de 100% a 0% em uma curva acendente e descendente linear;
    #B) Acionar os LEDs em sequência
    # ligar de 0-100%, onde o led 1 vai de 0 a 100 depois de 100 a 0
    # led2 começa a partir do momento que o 1 chega em 100%
    for output in output_list:
        p = GPIO.PWM(output, 0.5)
        p.start(1)
        input('Press return to stop:')   # use raw_input for Python 2
        p.stop()

def polling(option):
    if option == 'a':
        while True:
            actives = []
            for button in button_list:
                if GPIO.input(button):
                    actives.append(button)
            print(f'ativos: {actives}')
    else: 
        count = 0
        while True:
            if GPIO.input(5):
                if count < 5:
                    count+=1
                else:
                    print('ativo')
            else:
                if count == 0:
                    print('desativo')
                else:
                    count-=1

def events_interrupiting(option):
    # A) Utilizar o recurso de monitorar eventos para ler o estado de um botão;
    # B) Utilizar as interrupções para monitorar a mudança de estado de um botão;
    # C) Utilizando eventos ou interrupções, tratar o problema de bouncing para ler o estado de uma entrada.
    pass

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(output_list, GPIO.OUT)
    GPIO.setup(button_list, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    algorithm = input()
    if algorithm == '1':
        option = input()
        output_logic(option)
    if algorithm == '2':
        option = input()
        polling(option)
    GPIO.cleanup()

main()