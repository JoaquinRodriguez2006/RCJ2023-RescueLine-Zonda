from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor
from spike.control import wait_for_seconds, wait_until, Timer
from spike import MotorPair
import math
from hub import port

import hub as advancedHub
import time
import math
import random

hub = PrimeHub()
timer = Timer()


# COMUNICACION
port.E.mode(port.MODE_FULL_DUPLEX)
b=port.E
wait_for_seconds(1)
b.baud(115200)
wait_for_seconds(1)

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


global s

def update():
    global r1,g1,b1,ov1
    global r3,g3,b3,ov3

    global col_1
    global col_3

    r1,g1,b1,ov1 = sen_1.get_rgb_intensity()
    r3,g3,b3,ov3 = sen_3.get_rgb_intensity()

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


    global luz_1
    global luz_2
    global luz_3

    luz_1 = sen_1.get_reflected_light()
    luz_2 = sen_2.get_reflected_light()
    luz_3 = sen_3.get_reflected_light()


def giro_90_der():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < 83):
        motor_pair.start_tank(30,-30)
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)

def giro_90_izq():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() > -83):
        motor_pair.start_tank(-30,30)
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)

def giro_180_der():
    giro_90_der()
    giro_90_der()
    motor_pair.move_tank(0.7,'cm',30,-30)

def giro_180_izq():
    giro_90_izq()
    giro_90_izq()
    motor_pair.move_tank(0.7,'cm',-30,30)

def girar_num_grados_der(num):
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < num):
        motor_pair.start_tank(30, -30)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

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
                motor_pair.move_tank(5.3,'cm',50,80)
                giro_90_der()
                # motor_pair.move_tank(2,'cm',30,30)
                buscar_linea('der')
                motor_pair.move_tank(1.8,'cm',80,50)
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
                motor_pair.move_tank(5.3,'cm',80,50)
                giro_90_izq()
                # motor_pair.move_tank(2,'cm',30,30)
                buscar_linea('izq')
                motor_pair.move_tank(1.8,'cm',50,80)
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


def verifica_l_giro():
    manzana = 0
    update()
    motor_pair.move_tank(0.3,'cm',-80,-80)
    if luz_1 < 40 and luz_2 < 40 and luz_3 < 40:
        motor_pair.move_tank(4,'cm',80,80)
    elif luz_3 < 40 or luz_1 < 40:
        # print('capaz',r1,g1,b1,'    ',r3,g3,b3)
        # motor_pair.move_tank(2.5,'cm',-80,-80)
        motor_pair.move_tank(1.5,'cm',-80,-80)
        posible_verde()
        motor_pair.start_tank(0,0)
        if col_1 == 'green' or col_3 == 'green':
            # print('confirmamos',r1,g1,b1,'    ',r3,g3,b3)
            # motor_pair.move_tank(0.6,'cm',-80,-80)
            verifica_verde()
        else:
            wait_for_seconds(0.1)
            motor_pair.move_tank(1.4,'cm',80,80)
            # motor_pair.move_tank(0.7,'cm',-80,-80)
            # wait_for_seconds(0.1)
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -32):
                update()
                motor_pair.start_tank(-80,80)
                if luz_2 < 30:
                    motor_pair.start_tank(0,0)
                    # motor_pair.move_tank(2.5,'cm',30,30)
                    update()
                    buscar_linea("izq")
                    motor_pair.move_tank(2.4,'cm',50,30)
                    if col_1 == 'green' or col_3 == 'green':
                        motor_pair.move_tank(1.5,'cm',80,80)
                    manzana = 1
                    break
            motor_pair.start_tank(0,0)
            wait_for_seconds(0.1)
            if manzana == 0:
                hub.motion_sensor.reset_yaw_angle()
                while hub.motion_sensor.get_yaw_angle() < 31:
                    motor_pair.start_tank(80,-80)
                # motor_pair.move_tank(0,'cm',0,0)
                # motor_pair.move_tank(0.5,'cm',80,-80)
                # motor_pair.move_tank(0.5,'cm',80,-80)
                motor_pair.start_tank(0,0)
                wait_for_seconds(0.1)
                update()
                if luz_2 > 1:
                    hub.motion_sensor.reset_yaw_angle()
                    while (hub.motion_sensor.get_yaw_angle() < 31):
                        update()
                        motor_pair.start_tank(80,-80)
                        if luz_2 < 30:
                            motor_pair.start_tank(0,0)
                            # motor_pair.move_tank(2.5,'cm',30,30)
                            update()
                            buscar_linea("der")
                            motor_pair.move_tank(2.4,'cm',30,50)
                            if col_1 == 'green' or col_3 == 'green':
                                motor_pair.move_tank(1.5,'cm',80,80)
                            manzana = 1
                            break
                    motor_pair.start_tank(0,0)
                    wait_for_seconds(0.1)
                    if manzana == 0:
                        hub.motion_sensor.reset_yaw_angle()
                        while hub.motion_sensor.get_yaw_angle() > -31:
                            motor_pair.start_tank(-80,80)
                        motor_pair.move_tank(1,'cm',-80,-80)
                        update()
                        correccion = luz_1 - luz_3
                        correccion = int(correccion * 1.95)
                        motor_pair.move_tank(2,'cm',-45 + correccion,-45 - correccion)
                        # motor_pair.move_tank(2,'cm',-30,-30)
                        if correccion < 0:
                            motor_pair.move_tank(0.5,'cm',-80,80)
                        else:
                            motor_pair.move_tank(0.5,'cm',80,-80)
                else:
                    motor_pair.move_tank(1,'cm',-50,-50)
                    update()
                    correccion = luz_1 - luz_3
                    correccion = int(correccion * 2.5)
                    motor_pair.move_tank(2,'cm',-45 - correccion,-45 + correccion)
                    # motor_pair.move_tank(2,'cm',-30,-30)
                    if correccion < 0:
                        motor_pair.move_tank(1,'cm',-80,80)
                    else:
                        motor_pair.move_tank(1,'cm',80,-80)
    else:
        manzana = 0
    manzana = 0

def verifica_doble_negro():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    motor_pair.move_tank(0.4,'cm',80,80)
    update()
    if col_1 == 'green' or col_3 == "green":
        verifica_verde()
    elif luz_1 < 27 and luz_3 < 27:
        verifica_l_giro()
    else:
        correccion = luz_1 - luz_3
        correccion = int(correccion * 1.5)
        motor_pair.move_tank(2,'cm',-45 - correccion,-45 + correccion)
        if correccion > 0:
            motor_pair.move_tank(1.5,'cm',-80,80)
        else:
            motor_pair.move_tank(1.5,'cm',80,-80)
        # motor_pair.move_tank(2,'cm',-30,-30)


def distance_com():
    global s
    global dist
    b.write("Obstaculo\n")
    # motor_pair.start_tank(0, 0)
    # wait_for_seconds(0.2)
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

ant = 0


#################################################
#################################################
#################################################

def obstacle_detection():
    global ant
    global s
    global dist
    dist = 0
    distance_com()
    print("Primer While")        #########################################
    wait_for_seconds(0.5)
    while (dist != 1):# distancia mayor a 5
        motor_pair.start_tank(20, 20)
        distance_com()
    color_2 = sen_2.get_reflected_light()
    girar_num_grados_der(16)
    color_2 = sen_2.get_reflected_light()
    print("Segundo While")        #########################################
    wait_for_seconds(0.5)
    while (color_2 > 19):
        color_2 = sen_2.get_reflected_light()
        motor_pair.start_tank(-20,20)
    motor_pair.start_tank(0, 0)
    distance_com()
    print("Tercer While")        #########################################
    wait_for_seconds(0.5)
    while (dist <= 3): # distancia menor a 10
        motor_pair.start_tank(-20, -20)
        distance_com()
    motor_pair.start_tank(0, 0)
    motor_pair.move_tank(1, 'cm', -50, -50)
    print("Pregunta por el Ant")        #########################################
    wait_for_seconds(0.5)
    if (ant == 0):
        ant = 1
        girar_num_grados_der(45)
        motor_pair.start_tank(0, 0)
        distance_com()
        distance_com()
        distance_com()
        print("Primer if")        #########################################
        wait_for_seconds(0.5)
        if (dist == 6):# si la distancia es mayor a 20
            hub.light_matrix.show_image('HAPPY')
            girar_num_grados_der(30)
            motor_pair.start_tank(0, 0)
            distance_com()
            distance_com()
            distance_com()
            print("Segundo if")        #########################################
            wait_for_seconds(2)
            if (dist == 6):# si la distancia es mayor a 20
                motor_pair.move_tank(3.5, 'cm', -42, 100) # Antes estaba en 24
                motor_pair.move_tank(17, 'cm', 41, 100)
                # hub.light_matrix.show_image('HEART')
                timer.reset()
                color_1 = sen_1.get_reflected_light()
                print("Cuarto While")        #########################################
                wait_for_seconds(0.5)
                while (color_1 > 20): # Antes estaba en 45
                    color_1 = sen_1.get_reflected_light()
                    motor_pair.start_tank(36, 100)
                    if (timer.now() > 1):
                        color_1 = sen_1.get_reflected_light()
                        print("Quinto While")        #########################################
                        wait_for_seconds(0.5)
                        while (color_1 > 20):
                            color_1 = sen_1.get_reflected_light()
                            motor_pair.start_tank(30, 100)
                            timer.reset()
                motor_pair.start_tank(0, 0)
                hub.light_matrix.show_image('DIAMOND')
                motor_pair.move_tank(2, 'cm', 50, 50)
                color_2 = sen_2.get_reflected_light()
                print("Sexto While")        #########################################
                wait_for_seconds(0.5)
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(20, -20)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 50, 50)
            else:
                print("Primer else")        #########################################
                wait_for_seconds(0.5)
                color_2 = sen_2.get_reflected_light()
                hub.light_matrix.show_image('ANGRY')
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() > -159):
                    motor_pair.start_tank(-20, 20)
                hub.motion_sensor.reset_yaw_angle()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3.5, 'cm', 100, 60)
                motor_pair.move_tank(17, 'cm', 100, 40)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                print("While del Else")        #########################################
                wait_for_seconds(0.5)
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(100, 36)
                    if (timer.now() > 1.5):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(100, 21) # Antes eran 80/18
                            timer.reset()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(2, 'cm', 50, 50)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(-20, 20)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 50, 50)
        else:
            print("Segundo Else")        #########################################
            wait_for_seconds(0.5)
            color_2 = sen_2.get_reflected_light()
            hub.light_matrix.show_image('ANGRY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -109):
                motor_pair.start_tank(-20, 20)
            hub.motion_sensor.reset_yaw_angle()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(4.8, 'cm', 100, 88)
            motor_pair.move_tank(13, 'cm', 95, 40)
            hub.light_matrix.show_image('HEART')
            timer.reset()
            color_2 = sen_2.get_reflected_light()
            while (color_2 > 20): # Antes estaba en 45
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(100, 40)
                if (timer.now() > 1.5):
                    color_2 = sen_2.get_reflected_light()
                    while (color_2 > 20):
                        color_2 = sen_2.get_reflected_light()
                        motor_pair.start_tank(100, 20) # Antes eran 80/18
                        timer.reset()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(2, 'cm', 50, 50)
            color_2 = sen_2.get_reflected_light()
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(-20, 20)
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 50, 50)

    elif (ant == 1):
        print("El Elif")        #########################################
        wait_for_seconds(0.5)
        ant = 0
        hub.motion_sensor.reset_yaw_angle()
        while (hub.motion_sensor.get_yaw_angle() > -45):
            motor_pair.start_tank(-20, 20)
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(0, 0)
        distance_com()
        distance_com()
        distance_com()
        print("Otro IF")        #########################################
        wait_for_seconds(2)
        if (dist == 6):    # si distancia es mayor a 20
            hub.light_matrix.show_image('HAPPY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -30):
                motor_pair.start_tank(-20, 20)
            hub.motion_sensor.reset_yaw_angle()
            motor_pair.start_tank(0, 0)
            distance_com()
            distance_com()
            distance_com()
            print("Segundo Otro IF")        #########################################
            wait_for_seconds(0.5)
            if (dist == 6):    # si distancia es mayor a 20
                motor_pair.move_tank(3, 'cm', 96, -39) # Antes estaba en 24
                motor_pair.move_tank(17, 'cm', 95, 36)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(95, 34)
                    if (timer.now() > 1.2):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(95, 23)
                            timer.reset()
                motor_pair.start_tank(0, 0)
                hub.light_matrix.show_image('DIAMOND')
                motor_pair.move_tank(2, 'cm', 50, 50)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(-20, 20)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 50, 50)
            else:
                color_2 = sen_2.get_reflected_light()
                hub.light_matrix.show_image('ANGRY')
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() < 170):
                    motor_pair.start_tank(20, -20)
                hub.motion_sensor.reset_yaw_angle()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(4, 'cm', -44, 100)
                motor_pair.move_tank(13, 'cm', 43, 100)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(40, 80)
                    if (timer.now() > 1.5):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(16, 80) # Antes eran 80/18
                            timer.reset()
                motor_pair.start_tank(0, 0)
                hub.light_matrix.show_image('DIAMOND')
                motor_pair.move_tank(2, 'cm', 50, 50)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(20, -20)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 50, 50)
        else:
            print("Ultimo Else")        #########################################
            wait_for_seconds(2)
            color_2 = sen_2.get_reflected_light()
            hub.light_matrix.show_image('ANGRY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() < 125):
                angle = hub.motion_sensor.get_yaw_angle()
                motor_pair.start_tank(20, -20)
                # print(angle)
            hub.motion_sensor.reset_yaw_angle()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 36, 100)
            motor_pair.move_tank(17, 'cm', 34, 100)
            hub.light_matrix.show_image('HEART')
            timer.reset()
            color_2 = sen_2.get_reflected_light()
            while (color_2 > 20): # Antes estaba en 45
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(34, 100)
                if (timer.now() > 1.2):
                    color_2 = sen_2.get_reflected_light()
                    while (color_2 > 20):
                        color_2 = sen_2.get_reflected_light()
                        motor_pair.start_tank(26, 100) # Antes eran 80/18
                        timer.reset()
            motor_pair.start_tank(0, 0)
            hub.light_matrix.show_image('DIAMOND')
            motor_pair.move_tank(2, 'cm', 50, 50)
            color_2 = sen_2.get_reflected_light()
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(20, -20)
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 50, 50)


#################################################
#################################################
#################################################


def subida():
    error = 0
    error_previo = 0
    integral = 0
    derivada = 0
    proporcional = 0
    kp = 3.95    # 3.95 antes
    ki = 0.02
    kd = 0.4
    salida = 0

    motor_pair.start_tank(20,20)
    wait_for_seconds(0.6)
    motor_pair.start_tank(0,0)
    b.write("Mov_Big_Down\n")
    b.write("Mov_Big_Down\n")
    b.write("Mov_Big_Down\n")
    b.write("Mov_Big_Down\n")
    wait_for_seconds(4)
    motor_pair.move_tank(4, 'cm', 30, 30)
    wait_for_seconds(1)


    while hub.motion_sensor.get_pitch_angle() > 1:
        update()
        error = luz_1 - luz_3
        proporcional = error
        integral = integral + error * 0.05
        derivada = (error - error_previo)
        # salida = int(kp * proporcional + ki * integral + kd * derivada)
        error_previo = error
        salida = int(0.5 * proporcional)
        motor_pair.start_tank(20 + salida,20 - salida)

    motor_pair.start_tank(0,0)
    motor_pair.move_tank(2, 'cm', 20, 20)
    wait_for_seconds(0.2)

    while hub.motion_sensor.get_pitch_angle() != 0:
        update()
        error = luz_1 - luz_3
        proporcional = error
        integral = integral + error * 0.05
        derivada = (error - error_previo)
        # salida = int(kp * proporcional + ki * integral + kd * derivada)
        error_previo = error
        salida = int(0.5 * proporcional)
        motor_pair.start_tank(20 + salida,20 - salida)

    b.write("Mov_Big_Up\n")
    motor_pair.move_tank(4, 'cm', 20, 20)
    wait_for_seconds(1)
    s=b.read(3).decode()
    if s == 'O' or s == 'A' or s == 'OO' or s == 'AO' or s == 'AOO' or s == 'AAO':
        motor_pair.start_tank(0,0)
        wait_for_seconds(1)



def bajada():
    error = 0
    error_previo = 0
    integral = 0
    derivada = 0
    proporcional = 0
    kp = 3.95    # 3.95 antes
    ki = 0.02
    kd = 0.4
    salida = 0

    motor_pair.start_tank(0,0)
    motor_pair.move_tank(8, 'cm', -20, -20)
    motor_pair.start_tank(0,0)
    b.write("Mov_Big_Down\n")
    b.write("Mov_Big_Down\n")
    b.write("Mov_Big_Down\n")
    wait_for_seconds(4)
    # print("hola")
    motor_pair.move_tank(5, 'cm', 30, 30)
    wait_for_seconds(1)
    while hub.motion_sensor.get_pitch_angle() < -1:
        update()
        error = luz_1 - luz_3
        proporcional = error
        integral = integral + error * 0.05
        derivada = (error - error_previo)
        # salida = int(kp * proporcional + ki * integral + kd * derivada)
        error_previo = error
        salida = int(0.1 * proporcional)
        motor_pair.start_tank(20 + salida,20 - salida)

    motor_pair.start_tank(0,0)
    b.write("Mov_Big_Up\n")
    wait_for_seconds(1)
    s=b.read(3).decode()
    if s == 'O' or s == 'A' or s == 'OO' or s == 'AO' or s == 'AOO' or s == 'AAO':
        motor_pair.start_tank(0,0)
        wait_for_seconds(1)

############## Funciones de Comunicación - TOFs - Arduino Uno ##############

def rescue_com(message):
    global s
    global dist_rescue
    global vict_status

    b.write(message)
    # motor_pair.start_tank(0, 0)
    # wait_for_seconds(0.2)
    s=b.read(5).decode()
    if (s!='n' and s!='nn' and s!='nnn'): # 1: Near
        if (s!='a' and s!='aa' and s!='aaa'): # 2: Always
            if (s!='f' and s!='ff' and s!='fff'): # 3: Far
                if (s!='u' and s!='uu' and s!='uuu'): # 4: Nule
                    dist_rescue = 5
                else:
                    dist_rescue = 4
            else:
                dist_rescue = 3
        else:
            dist_rescue = 2
    else:
        dist_rescue = 1
    print(dist)

    if (s!='u' and s!= 'uu' and s!='uuu'): # 1: Nule
        if (s!='s' and s!='ss' and s!='sss'): # 2: Spotted Victim
            if (s!='a' and s!='aa' and s!='aaa'): # 3: Always
                if (s!='n' and s!='nn' and s!='nnn'): # 4: Non-Spotted
                    vict_status = 5
                else:
                    vict_status = 4
            else:
                vict_status = 3
        else:
            vict_status = 2
    else:
        vict_status = 1

    return dist
    return vict_status


def victim_com(message):
    global claw_status

    b.write(message)

    s=b.read(5).decode()
    if (s!='d' and s!='dd' and s!='ddd'): # 1: Done
        if (s!='i' and s!='ii' and s!='iii'): # 2: Impossible
            claw_status = 3
        else:
            claw_status = 2
    else:
        claw_status = 1

    return claw_status

######################################################################################## RESCUE AREA FUNCTIONS ########################################################################################
def detect_walls(assigned_distance):
    global s
    global dist
    rescue_com('Rescue\n')
    if (dist <= assigned_distance): # distancia menor a 10
        return True

def detect_victims(assigned_distance):
    global s
    global dist
    global vict_status
    rescue_com('Rescue_v\n')
    if (vict_status <= assigned_distance):
        victim_com(rescue_com('SpottedVictim_r\n')) # Spotted Victim - Rescue it!

def turn_x_degrees(num):
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < num):
        motor_pair.start_tank(90, -85)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()


while True:
    update()
    error = luz_1 - luz_3
    proporcional = error
    integral = integral + error * 0.05
    derivada = (error - error_previo)
    # salida = int(kp * proporcional + ki * integral + kd * derivada)
    error_previo = error

    if col_1 == 'plateado' or col_3 == 'plateado':
        break

    elif hub.motion_sensor.get_pitch_angle() > 10:
        subida()
    elif hub.motion_sensor.get_pitch_angle() < -10:
        bajada()
    else:
        if col_1 == 'green' or col_3 == 'green':
            motor_pair.start_tank(0,0)
            b.write("Verde\n")
            verifica_verde()
        elif luz_1 < 20 and luz_3 < 20:
            motor_pair.start_tank(0,0)
            b.write("Doble Negro\n")
            verifica_doble_negro()
        else:
            b.write("Seguidor\n")
            s=b.read(3).decode()
            # print(s)

            if s == 'F':
                motor_pair.start_tank(0,0)
                obstacle_detection()
            if s == 'A':
                if luz_3 < 25 or luz_1 < 25:
                    salida = int(2.6 * proporcional + ki * integral + kd * derivada)
                    motor_pair.start_tank(20 + salida,20 - salida)
                else:
                    salida = int(1.7 * proporcional + ki * integral + kd * derivada)
                    motor_pair.start_tank(30 + salida,30 - salida)

######## RESCUE AREA ########
while True:
    if col_1 == 'plateado' or col_3 == 'plateado':
        state = 'rescue'
        substate = 'exploring'

        if (state == 'rescue') and (substate == 'exploring'):
            motor_pair.start_tank(20,20)
            rescue_com("Rescue\n")
            if detect_walls(1):
                turn_x_degrees(90)
                if detect_walls(1):
                    turn_x_degrees(270)
                    motor_pair.move_tank(9, 'cm', 20, 20)
                    substate = 'looking for ball'
                else:
                    motor_pair.move_tank(9, 'cm', 20, 20)
                    substate = 'looking for ball'

        if (state == 'rescue') and (substate == 'looking for ball'):
            rescue_com("Rescue_v\n")
            hub.motion_sensor.reset_yaw_angle()
            while (detect_victims(1 or 3 or 4)) or (hub.motion_sensor.get_yaw_angle() < 90):
                hub.light_matrix.show_image('HAPPY')
                motor_pair.start_tank(20, 20) # TO TEST
            motor_pair.start_tank(0, 0)
            hub.motion_sensor.reset_yaw_angle()

        if (state == 'rescue') and (substate == 'looking for green'):
            motor_pair.start_tank(20,20)
            if detect_walls(1):
                motor_pair.start_tank(0,0)
                if sen_1.get_reflected_light() > 85 and sen_3.get_reflected_light() > 85:
                    motor_pair.move_tank(4, 'cm', 20, 20)
                    # DEPOSIT CUBE
                    # CHANGE STATE
                else:
                    turn_x_degrees(90)
                    if detect_walls(1):
                        turn_x_degrees(270)
                    else:
                        pass
"""
if luz_3 < 19 or luz_1 < 19:
                    salida = int(2.6 * proporcional + ki * integral + kd * derivada)
                    motor_pair.start_tank(20 + salida,20 - salida)
                elif luz_3 < 25 or luz_1 < 25:
                    salida = int(1.7 * proporcional + ki * integral + kd * derivada)
                    motor_pair.start_tank(30 + salida,30 - salida)
                else:
                    salida = int(0.9 * proporcional + ki * integral + kd * derivada)
                    motor_pair.start_tank(35 + salida,35 - salida)
"""