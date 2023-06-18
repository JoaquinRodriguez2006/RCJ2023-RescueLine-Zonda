from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor
from spike.control import wait_for_seconds
from hub import port
from spike import MotorPair
import math

import hub as advancedHub
import time
import math
import random

hub = PrimeHub()

port.E.mode(port.MODE_FULL_DUPLEX)
b=port.E
wait_for_seconds(1)
b.baud(115200)

# MOTORES
motor_pair = MotorPair('C', 'A')
motor_pair.set_motor_rotation(3.2 * math.pi,'cm')

# SENSORES
sen_1 = ColorSensor("B")
sen_2 = ColorSensor("D")
sen_3 = ColorSensor("F")

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

def update():

    global luz_1
    global luz_2
    global luz_3

    luz_1 = sen_1.get_reflected_light()
    luz_2 = sen_2.get_reflected_light()
    luz_3 = sen_3.get_reflected_light()

    global r1,g1,b1,ov1
    global r3,g3,b3,ov3

    global col_1
    global col_3

    r1,g1,b1,ov1 = sen_1.get_rgb_intensity()
    r3,g3,b3,ov3 = sen_3.get_rgb_intensity()

    luz_1 = sen_1.get_reflected_light()
    luz_2 = sen_2.get_reflected_light()
    luz_3 = sen_3.get_reflected_light()

    if r1 + 20 < g1 > b1 and g1 < 220:# g1 = 205
        # print('MANZANA: ',r1,g1,b1)
        col_1 = 'green'
    elif r1 + 20 < g1 > b1 + 10 and g1 < 260:
        # print('AGROPECUARIO: ',r1,g1,b1)
        col_1 = 'green'
    elif r1 > 700 and g1 > 700 and b1 > 700:
        col_1 = 'plateado'
    else:
        # print('PERA: ',r1,g1,b1)
        col_1 = 'no'
        # print(r1,g1,b1)

    if r3 + 20 < g3 > b3 and g3 < 220: # g3 = 205
        # print('Verde: ',r3,g3,b3)
        col_3 = 'green'
    elif r3 + 20 < g3 > b3 + 10 and g3 < 260:
        # print('Verde blanquesino',r3,g3,b3)
        # print('a')
        col_3 = 'green'
    elif r3 > 700 and g3 > 700 and b3 > 700:
        col_3 = 'plateado'
    else:
        # print('no: ',r3,g3,b3)
        col_3 = 'no'

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

def giro_180_der():
    giro_90_der()
    giro_90_der()
    motor_pair.move_tank(0.7,'cm',80,-80)

def giro_180_izq():
    giro_90_izq()
    giro_90_izq()
    motor_pair.move_tank(0.7,'cm',-80,80)

def posible_verde():
    pera = 0
    hub.motion_sensor.reset_yaw_angle()
    while hub.motion_sensor.get_yaw_angle() < 10:
        update()
        motor_pair.start_tank(60,-60)
        if col_1 == 'green' or col_3 == 'green':
            motor_pair.start_tank(0,0)
            pera = 1
            break
    motor_pair.start_tank(0,0)
    wait_for_seconds(0.1)
    if pera == 0:
        hub.motion_sensor.reset_yaw_angle()
        while hub.motion_sensor.get_yaw_angle() > -10:
            motor_pair.start_tank(-60,60)
        motor_pair.start_tank(0,0)
        wait_for_seconds(0.1)
        hub.motion_sensor.reset_yaw_angle()
        while hub.motion_sensor.get_yaw_angle() > -10:
            update()
            motor_pair.start_tank(-60,60)
            if col_1 == 'green' or col_3 == 'green':
                motor_pair.start_tank(0,0)
                pera = 1
                break
        motor_pair.start_tank(0,0)
        wait_for_seconds(0.1)
        if pera == 0:
            hub.motion_sensor.reset_yaw_angle()
            while hub.motion_sensor.get_yaw_angle() < 10:
                motor_pair.start_tank(60,-60)
            motor_pair.start_tank(0,0)

def verifica_verde():
    manzana = 0
    pera = 0
    motor_pair.start_tank(0,0)
    # if not col_1 == 'green' and not col_3 == 'green':
    #    motor_pair.move_tank(0.6,'cm',80,80)
    update()
    if col_1 == 'green':
        manzana = 1
    elif col_3 == 'green':
        pera = 1
    motor_pair.move_tank(0.5,'cm',80,80)
    update()
    if col_1 == 'green' and col_3 == 'green':
        giro_180_der()
        motor_pair.move_tank(0.5,'cm',80,80)
        update()
        # if color_3 == 'green' or color_1 == 'green':
        #    motor_pair.move_tank(1.5,'cm',50,50)
        # buscar_linea('der')
    elif col_3 == 'green' and not col_1 == 'green':
        motor_pair.move_tank(0.7,'cm',-80,80)
        # motor_pair.move_tank(0.9,'cm',-80,80)
        update()
        if col_1 == 'green' and col_3 == 'green':
            giro_180_der()
            motor_pair.move_tank(0.5,'cm',80,80)
            update()
        else:
            # motor_pair.move_tank(0.7,'cm',-80,20)
            if col_3 == 'green' and not col_1 == 'green':
                # motor_pair.move_tank(0.9,'cm',-100,0)
                # motor_pair.move_tank(0.5,'cm',-80,-80)
                # motor_pair.move_tank(1,'cm',50,50)
                motor_pair.move_tank(3.5,'cm',30,80)
                giro_90_der()
                # motor_pair.move_tank(2,'cm',30,30)
                buscar_linea('der')
                motor_pair.move_tank(2.8,'cm',80,50)
                update()
                if luz_2 > 40:
                    motor_pair.move_tank(0.8,'cm',-80,-80)
                update()
                if col_3 == 'green' or col_1 == 'green':
                    motor_pair.move_tank(1.5,'cm',80,30)
            else:
                motor_pair.move_tank(2,'cm',-70,0)
    elif col_1 == 'green' and not col_3 == 'green':
        motor_pair.move_tank(0.7,'cm',80,-80)
        # motor_pair.move_tank(0.9,'cm',80,-80)
        update()
        if col_3 == 'green' and col_1 == 'green':
            giro_180_izq()
            update()
        else:
            # motor_pair.move_tank(0.7,'cm',20,-80)
            if col_1 == 'green' and not col_3 == 'green':
                # motor_pair.move_tank(0.9,'cm',0,-100)
                # motor_pair.move_tank(0.5,'cm',-80,-80)
                # motor_pair.move_tank(1,'cm',50,50)
                motor_pair.move_tank(3.5,'cm',80,30)
                giro_90_izq()
                # motor_pair.move_tank(2,'cm',30,30)
                buscar_linea('izq')
                motor_pair.move_tank(2.8,'cm',50,80)
                update()
                if luz_2 > 40:
                    motor_pair.move_tank(0.8,'cm',-50,-50)
                    update()
                if col_3 == 'green' or col_1 == 'green':
                    motor_pair.move_tank(1.5,'cm',30,80)
            else:
                motor_pair.move_tank(2,'cm',0,-70)
    else:
        if manzana == 1:
            motor_pair.move_tank(2,'cm',0,-70)
        elif pera == 1:
            motor_pair.move_tank(2,'cm',-70,0)
        else:
            motor_pair.move_tank(2,'cm',-50,-50)

def buscar_linea(direccion):
    motor_pair.start_tank(0,0)
    if direccion == 'der':
        motor_pair.move_tank(0.6,'cm',60,0)
        while luz_1 > 23 and luz_2 > 23:
            update()
            motor_pair.start_tank(80,-80)
        motor_pair.start_tank(0,0)
        if luz_2 < 30:
            motor_pair.move_tank(0.7,'cm',-60,60)
        else:
            # motor_pair.move_tank(1,'cm',-80,80)
            while luz_2 > 20:
                update()
                motor_pair.start_tank(-80,80)
            # motor_pair.move_tank(0.7,'cm',-80,80)
    elif direccion == 'izq':
        motor_pair.move_tank(0.6,'cm',0,60)
        while luz_3 > 23 and luz_2 > 23:
            update()
            motor_pair.start_tank(-60,60)
        if luz_2 < 30:
            motor_pair.move_tank(0.7,'cm',60,-60)
        else:
            # motor_pair.move_tank(1,'cm',80,-80)
            while luz_2 > 20:
                update()
                motor_pair.start_tank(80,-80)
            # motor_pair.move_tank(0.7,'cm',80,-80)

def sender():
    m = b.send().encode()


def receiver():
    m = b.read(1).decode()
    return m

def obstacle_detection():
    s = b.read(1).decode()
    if s == 'C':
        pass
    if s == 'S':
        motor_pair.start_tank(0, 0)


while True:
    update()

    if col_1 == 'plateado' or col_3 == 'plateado':
        break
# Communication Protocol for Obstacle detection
    # Receiver
    
    else:
        update()
        if col_1 == 'green' or col_3 == 'green':
            # print('a')
            motor_pair.start_tank(0,0)
            verifica_verde()
        # elif (luz_1 < 30 and luz_2 < 30 and luz_1 != 'green') or (luz_3 < 30 and luz_2 < 30 and luz_3 != 'green'):
        #    motor_pair.move_tank(4.5,'cm',80,80)
        elif luz_1 < 26 and luz_3 < 26:
            motor_pair.start_tank(0,0)
        elif luz_1 > 50 and luz_2 > 50 and luz_3 > 50:
            motor_pair.start_tank(60,60)
        # elif hub.motion_sensor.get_roll_angle() > 1 or hub.motion_sensor.get_roll_angle() < -1:
        #    loma_burro()
        else:
            error = luz_1 - luz_3
            proporcional = error
            integral = integral + error * 0.04
            derivada = (error - error_previo) / 0.04
            # salida = int(kp * proporcional + ki * integral + kd * derivada)
            error_previo = error

            if luz_3 < 20 or luz_1 < 20:
                salida = int(4 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(30 + salida,30 - salida)
            elif luz_3 < 40 or luz_1 < 40:
                salida = int(3 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(40 + salida,40 - salida)
            else:
                salida = int(1.7 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(50 + salida,50 - salida)