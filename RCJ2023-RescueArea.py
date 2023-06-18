from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import hub as advancedHub
from hub import port
import time
import math
import random
from math import *

# COMMUNICATION
port.E.mode(port.MODE_FULL_DUPLEX)
b=port.E
wait_for_seconds(1)
b.baud(115200)

hub = PrimeHub()

# global color_1
# global color_2
# global color_3

global luz_1
global luz_2
global luz_3

global r1,g1,b1,ov1
global r2,g2,b2,ov2
global r3,g3,b3,ov3

global col_1
global col_3

global dist_cm

global flag_detection

global ant

# MOTORES
motor_pair = MotorPair('C', 'A')
motor_pair.set_motor_rotation(1.07 * math.pi, "cm")

# SENSORES
sen_1 = ColorSensor("B")
sen_2 = ColorSensor("D")
sen_3 = ColorSensor("F")

# AYUDAS
timer = Timer()
flag_detection = False
ant = 0
global s
global dist

# PID
error = 0
error_previo = 0
integral = 0
derivada = 0
proporcional = 0
kp = 3.95    # 3.95 antes
ki = 0.02
kd = 0.4
salida = 0

# DISPLAY
H = 9
L = 7
_ = 0

nada = [
    [_,_,_,_,_],
    [_,_,_,_,_],
    [_,_,_,_,_],
    [_,_,_,_,_],
    [_,_,_,_,_],
]

flecha_der = [
    [_,_,H,_,_],
    [_,_,_,H,_],
    [H,H,H,H,H],
    [_,_,_,H,_],
    [_,_,H,_,_],
]

flecha_izq = [
    [_,_,H,_,_],
    [_,H,_,_,_],
    [H,H,H,H,H],
    [_,H,_,_,_],
    [_,_,H,_,_],
]

flecha_atras = [
    [_,_,H,_,_],
    [_,_,H,_,_],
    [H,_,H,_,H],
    [_,H,H,H,_],
    [_,_,H,_,_],
]

flecha_frente = [
    [_,_,H,_,_],
    [_,H,H,H,_],
    [H,_,H,_,H],
    [_,_,H,_,_],
    [_,_,H,_,_],
]

blanco_h = [
    [_,_,H,_,_],
    [_,_,_,_,_],
    [H,_,_,_,H],
    [_,_,_,_,_],
    [_,_,H,_,_],
]

blanco_l = [
    [_,_,L,_,_],
    [_,_,_,_,_],
    [L,_,_,_,L],
    [_,_,_,_,_],
    [_,_,L,_,_],
]

cruz_h = [
    [_,_,H,_,_],
    [_,_,H,_,_],
    [H,H,H,H,H],
    [_,_,H,_,_],
    [_,_,H,_,_],
]

l_izq = [
    [_,_,H,_,_],
    [_,_,H,_,_],
    [H,H,H,_,_],
    [_,_,H,_,_],
    [_,_,H,_,_],
]

l_der = [
    [_,_,H,_,_],
    [_,_,H,_,_],
    [_,_,H,H,H],
    [_,_,H,_,_],
    [_,_,H,_,_],
]

cruz_l = [
    [_,_,L,_,_],
    [_,_,L,_,_],
    [L,L,L,L,L],
    [_,_,L,_,_],
    [_,_,L,_,_],
]

equis = [
    [H,_,_,_,H],
    [_,H,_,H,_],
    [_,_,H,_,_],
    [_,H,_,H,_],
    [H,_,_,_,H],
]

equis_d = [
    [_,H,H,H,_],
    [H,H,_,H,H],
    [H,_,H,_,H],
    [H,H,_,H,H],
    [_,H,H,H,_],
]

verde = [
    [H,_,_,_,H],
    [H,_,_,_,H],
    [_,H,_,H,_],
    [_,H,_,H,_],
    [_,_,H,_,_],
]

verde_l = [
    [L,_,_,_,L],
    [L,_,_,_,L],
    [_,L,_,L,_],
    [_,L,_,L,_],
    [_,_,L,_,_],
]

buscar = [
    [H,H,H,_,_],
    [H,_,_,H,_],
    [H,H,H,_,_],
    [H,_,_,H,_],
    [H,H,H,_,_],
]

derecha = [
    [H,H,H,_,_],
    [H,_,_,H,_],
    [H,_,_,_,H],
    [H,_,_,H,_],
    [H,H,H,_,_],
]

izquierda = [
    [H,H,H,H,H],
    [_,_,H,_,_],
    [_,_,H,_,_],
    [_,_,H,_,_],
    [H,H,H,H,H],
]

######################################################################################## LINE FOLLOWING FUNCTIONS ########################################################################################

############## Funciones de Giro #################
def giro_90_der():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < 83):
        motor_pair.start_tank(60,-60)
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    print('Angulo:', angle)

def giro_90_izq():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() > -83):
        motor_pair.start_tank(-60,60)
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    print('Angulo:', angle)

############## Funciones de Comunicación - TOFs - Arduino Uno ##############

def obstaculo_com():
    global s
    global dist
    b.write("Obstaculo\n")
    # motor_pair.start_tank(0, 0)
    wait_for_seconds(0.2)
    s=b.read(5).decode()
    print(s)
    if (s!='R' and s!='RR' and s!='RRR'):
        if (s!='C' and s!='CC' and s!='CCC'):
            if (s!='S' and s!='SS' and s!='SSS'):
                if (s!='L' and s!='LL' and s!='LLL'):
                    if (s!='M' and s!='MM' and s!='MMM'):
                        if (s!='N' and s!='NN' and s!='NNN'):
                            dist = 7
                        else:
                            dist = 6
                    else:
                        dist = 5
                else:
                    dist = 4
            else:
                dist = 3
        else:
            dist = 2
    else:
        dist = 1
    print(dist)

def rescue_com(message):
    global s
    global dist
    b.write(message)
    # motor_pair.start_tank(0, 0)
    # wait_for_seconds(0.2)
    s=b.read(5).decode()
    if (s!='n' and s!='nn' and s!='nnn'): # 1: Near
        if (s!='a' and s!='aa' and s!='aaa'): # 2: Always
            if (s!='f' and s!='ff' and s!='fff'): # 3: Far
                if (s!='u' and s!='uu' and s!='uuu'): # 4: Nule
                    dist = 5
                else:
                    dist = 4
            else:
                dist = 3
        else:
            dist = 2
    else:
        dist = 1
    print(dist)

ant = 0

def get_distance():
    s = b.read(100).decode()
    if s == 'A': # Andar
        return 'A'
    if s == 'F': # Frenar
        return 'F'
    if s == 'N': # No detecta
        return 'N'
    if s == 'R': # Re Lejos
        return 'R'
    if s == 'C': # Cerca
        return 'C'
    if s == 'S': # Siempre
        return 'S'
    if s == 'L':# Lejos
        return 'L'
    if s == 'M': # Muy Lejos
        return 'M'

def ball_finding_izq(angle):
    hub.motion_sensor.reset_yaw_angle()
    while hub.motion_sensor.get_yaw_angle() < -angle:
        motor_pair.start_tank(-85, 90)

    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

def ball_finding_der(angle):
    hub.motion_sensor.reset_yaw_angle()
    while hub.motion_sensor.get_yaw_angle() < angle:
        motor_pair.start_tank(90, -85)
        #if get_distance() != 'N' or 'S' or 'L' or 'M':
        #    motor_pair.stop()
        #else:
        #    pass
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

def search_silver():
    motor_pair.start(speed=30)
    while True:
        if sen_1.get_reflected_light() > 85 and sen_3.get_reflected_light() > 85:
            motor_pair.start(speed=0)

######################################################################################## RESCUE AREA FUNCTIONS ########################################################################################
def detect_walls(assigned_distance):
    global s
    global dist
    rescue_com()
    if (dist <= assigned_distance): # distancia menor a 10
        return True
    
def turn_x_degrees(num):
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < num):
        motor_pair.start_tank(90, -85)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()


######################################################################################## MAIN CODE ########################################################################################

state = 'start'

for substates in 'rescue':
    substate = 'looking for the ball'
    substate = 'exploring'
    substate = 'aligning with wall'
    substate = 'looking fot the green corner'
    substate = 'depositing the ball'
    substate = 'depositing the cube'


while True:
    state = 'rescue'
    substate = 'exploring'

    if (state == 'rescue') and (substate == 'exploring'):
        motor_pair.start_tank(20,20)
        rescue_com()
        if detect_walls(1):
            turn_x_degrees(-90)
            motor_pair.move_tank(9, 'cm', 20, 20)
            substate = 'looking for ball'
    
    if (state == 'rescue') and (substate == 'looking for ball'):
        rescue_com("Rescue_l\n")
        hub.motion_sensor.reset_yaw_angle()
        while (s != 's') or (hub.motion_sensor.get_yaw_angle() < 90):
            hub.light_matrix.show_image('HAPPY')
        motor_pair.start_tank(0, 0)
        hub.motion_sensor.reset_yaw_angle()

        
"""while True:
    while True:
        if sen_1.get_reflected_light() > 85 and sen_3.get_reflected_light() > 85:
        motor_pair.start_tank(30, 30)
        rescue_com()
        if (dist <= 1): # distancia menor a 10
            hub.light_matrix.show_image('HAPPY')
            motor_pair.start_tank(0, 0)
        if detect_walls:
            hub.light_matrix.show_image('HAPPY')
            giro_90_der()
            motor_pair.move_tank(9, 'cm', 30, 30)"""