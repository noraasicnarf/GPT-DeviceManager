import serial
from time import sleep
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=0)
#Process command to arduino

# arduino response mapping
mappings = {

#Sucessful response
    'A': {'result' : {'fan_on': 'success'}},
    'a': {'result' : {'fan_off': 'success'}},
    'B': {'result' : {'light_on': 'success'}},
    'b': {'result' : {'light_off': 'success'}},

# Check the arduino code also 
#     'C': {'result' : {'': 'success'}},
#     'c': {'result' : {'': 'success'}},

#Failed response
    'X': {'result' : {'fan_on': 'already on'}},
    'x': {'result' : {'fan_off': 'already off'}},
    'Y': {'result' : {'light_on': 'already on'}},
    'y': {'result' : {'light_off': 'already off'}},

#     'Z': {'result' : {'': 'assistant response'}},
#     'z': {'result' : {'': 'assistant response'}}
}



def send_command(commands: list) :
        received_char = []
        for command in commands:
                device = command['device']
                action = command['action']
                if device == 'fan':
                        received_char.append(mappings[send_code('A' if action == 'turn_on' else 'a')])
                elif device == 'light':
                        received_char.append(mappings[send_code('B' if action == 'turn_on' else 'b')])
                # elif device == 'add_your_device_here':
                #         received_char.append(mappings[send_code('C' if action == 'turn_on' else 'c')])
        return received_char

def send_code(char):
        arduino.write(char.encode('utf-8'))
        while True:
                data = arduino.readline(arduino.in_waiting)
                if data:
                        return data.decode('utf-8')
        
        
        