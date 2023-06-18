from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import hub as advancedHub
import time
import math
import random
from math import *

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
distancia = DistanceSensor('E')

# AYUDAS
timer = Timer()
flag_detection = False
ant = 0

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

# FUNCIONES

def matrix_to_image(matrix):
    return advancedHub.Image(":".join(["".join([str(n) for n in r]) for r in matrix]))

def mostrar(img,sec = 0):
    display = matrix_to_image(nada)
    advancedHub.display.show(display)
    display = matrix_to_image(img)
    advancedHub.display.show(display)
    wait_for_seconds(sec)

def update():
    # global color_1
    # global color_2
    # global color_3

    global luz_1
    global luz_2
    global luz_3

    global r1,g1,b1,ov1
    global r3,g3,b3,ov3

    global col_1
    global col_3

    r1,g1,b1,ov1 = sen_1.get_rgb_intensity()
    r3,g3,b3,ov3 = sen_3.get_rgb_intensity()

    global dist_cm

    luz_1 = sen_1.get_reflected_light()
    luz_2 = sen_2.get_reflected_light()
    luz_3 = sen_3.get_reflected_light()

    # color_1 = sen_1.get_color()
    # color_2 = sen_2.get_color()
    # color_3 = sen_3.get_color()

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

    dist_cm = distancia.get_distance_cm()

    if dist_cm == None:
        dist_cm = 200

def get_distance():
    dist_cm = distancia.get_distance_cm()
    if (dist_cm == None):
        dist_cm = 200
    return dist_cm

def giro_90_der():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < 80):
        motor_pair.start_tank(80,-80)
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    print('Angulo:', angle)

def giro_90_izq():
    motor_pair.start_tank(0,0)
    # wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() > -80):
        motor_pair.start_tank(-80,80)
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

def girar_num_grados_der(num):
    hub.motion_sensor.reset_yaw_angle()
    while (hub.motion_sensor.get_yaw_angle() < num):
        motor_pair.start_tank(90, -85)
    motor_pair.start_tank(0, 0)
    hub.motion_sensor.reset_yaw_angle()

def posible_verde():
    pera = 0
    hub.motion_sensor.reset_yaw_angle()
    while hub.motion_sensor.get_yaw_angle() < 10:
        update()
        motor_pair.start_tank(80,-80)
        if col_1 == 'green' or col_3 == 'green':
            motor_pair.start_tank(0,0)
            pera = 1
            break
    motor_pair.start_tank(0,0)
    wait_for_seconds(0.1)
    if pera == 0:
        hub.motion_sensor.reset_yaw_angle()
        while hub.motion_sensor.get_yaw_angle() > -10:
            motor_pair.start_tank(-80,80)
        motor_pair.start_tank(0,0)
        wait_for_seconds(0.1)
        hub.motion_sensor.reset_yaw_angle()
        while hub.motion_sensor.get_yaw_angle() > -10:
            update()
            motor_pair.start_tank(-80,80)
            if col_1 == 'green' or col_3 == 'green':
                motor_pair.start_tank(0,0)
                pera = 1
                break
        motor_pair.start_tank(0,0)
        wait_for_seconds(0.1)
        if pera == 0:
            hub.motion_sensor.reset_yaw_angle()
            while hub.motion_sensor.get_yaw_angle() < 10:
                motor_pair.start_tank(80,-80)
            motor_pair.start_tank(0,0)

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
                    mostrar(l_der)
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
            # mostrar(equis,2)
            # mostrar(nada)
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
                            mostrar(l_izq)
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
                    # mostrar(equis_d,2)
                    # mostrar(nada)
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
    mostrar(cruz_l)
    motor_pair.move_tank(0.4,'cm',80,80)
    update()
    if col_1 == 'green' or col_3 == "green":
        verifica_verde()
    elif luz_1 < 27 and luz_3 < 27:
        mostrar(cruz_h)
        mostrar(nada,0)
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
        mostrar(nada,0)

def verifica_verde():
    manzana = 0
    pera = 0
    motor_pair.start_tank(0,0)
    mostrar(verde_l)
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
        mostrar(verde)
        mostrar(flecha_atras,0)
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
            mostrar(verde)
            mostrar(flecha_atras,0)
            giro_180_der()
            motor_pair.move_tank(0.5,'cm',80,80)
            update()
        else:
            # motor_pair.move_tank(0.7,'cm',-80,20)
            if col_3 == 'green' and not col_1 == 'green':
                mostrar(verde)
                mostrar(flecha_der,0)
                # motor_pair.move_tank(0.9,'cm',-100,0)
                # motor_pair.move_tank(0.5,'cm',-80,-80)
                # motor_pair.move_tank(1,'cm',50,50)
                motor_pair.move_tank(3.5,'cm',30,100)
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
                mostrar(nada,0)
                motor_pair.move_tank(2,'cm',-70,0)
    elif col_1 == 'green' and not col_3 == 'green':
        motor_pair.move_tank(0.7,'cm',80,-80)
        # motor_pair.move_tank(0.9,'cm',80,-80)
        update()
        if col_3 == 'green' and col_1 == 'green':
            mostrar(verde)
            mostrar(flecha_atras,0)
            giro_180_izq()
            update()
        else:
            # motor_pair.move_tank(0.7,'cm',20,-80)
            if col_1 == 'green' and not col_3 == 'green':
                mostrar(verde)
                mostrar(flecha_izq,0)
                # motor_pair.move_tank(0.9,'cm',0,-100)
                # motor_pair.move_tank(0.5,'cm',-80,-80)
                # motor_pair.move_tank(1,'cm',50,50)
                motor_pair.move_tank(3.5,'cm',100,30)
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
                mostrar(nada,0)
                motor_pair.move_tank(2,'cm',0,-70)
    else:
        mostrar(nada,0)
        if manzana == 1:
            motor_pair.move_tank(2,'cm',0,-70)
        elif pera == 1:
            motor_pair.move_tank(2,'cm',-70,0)
        else:
            motor_pair.move_tank(2,'cm',-50,-50)
    # mostrar(nada,0)

def buscar_linea(direccion):
    motor_pair.start_tank(0,0)
    mostrar(buscar)
    if direccion == 'der':
        motor_pair.move_tank(0.8,'cm',80,0)
        while luz_1 > 23 and luz_2 > 23:
            update()
            motor_pair.start_tank(80,-80)
        motor_pair.start_tank(0,0)
        # mostrar(equis)
        if luz_2 < 30:
            motor_pair.move_tank(0.7,'cm',-80,80)
        else:
            # motor_pair.move_tank(1,'cm',-80,80)
            while luz_2 > 20:
                update()
                motor_pair.start_tank(-80,80)
            # motor_pair.move_tank(0.7,'cm',-80,80)
    elif direccion == 'izq':
        motor_pair.move_tank(0.8,'cm',0,80)
        while luz_3 > 23 and luz_2 > 23:
            update()
            motor_pair.start_tank(-80,80)
        # mostrar(equis)
        if luz_2 < 30:
            motor_pair.move_tank(0.7,'cm',80,-80)
        else:
            # motor_pair.move_tank(1,'cm',80,-80)
            while luz_2 > 20:
                update()
                motor_pair.start_tank(80,-80)
            # motor_pair.move_tank(0.7,'cm',80,-80)
    else:
        mostrar(nada,0)
    mostrar(nada)
    # motor_pair.move_tank(0.8,'cm',50,50)
    # if col_1 == 'green' or col_3 == 'green':
    #    motor_pair.move_tank(2,'cm',50,50)
    # mostrar(nada,0)

def loma_burro():
    update()
    error = luz_1 - luz_3
    proporcional = error
    salida = int(1.7 * proporcional)
    motor_pair.start_tank(30 + salida, 30 - salida)
    update()
    if luz_1 < 16:
        while luz_2 > 25:
            motor_pair.start_tank(-40,40)
            update()
        # motor_pair.move_tank(1,'cm',50,50)
    elif luz_3 < 16:
        while luz_2 > 25:
            motor_pair.start_tank(40,-40)
            update()
        # motor_pair.move_tank(1,'cm',50,50)
    else:
        mostrar(equis)

def obstacle_detection():
    global ant
    dist_cm = get_distance()
    if dist_cm > 5:
        motor_pair.start_tank(50, 50)
        dist_cm = get_distance()
    dist_cm = get_distance()
    color_2 = sen_2.get_reflected_light()
    girar_num_grados_der(16)
    color_2 = sen_2.get_reflected_light()
    while (color_2 > 19):
        color_2 = sen_2.get_reflected_light()
        motor_pair.start_tank(-95,95)
    motor_pair.start_tank(0, 0)
    while ((dist_cm) < 10):
        dist_cm = get_distance()
        print(dist_cm)
        motor_pair.start_tank(-80, -80)
    motor_pair.start_tank(0, 0)
    motor_pair.move_tank(1, 'cm', -100, -100)
    if (ant == 0):
        ant = 1
        girar_num_grados_der(45)
        dist_cm = get_distance()
        if (dist_cm > 20):
            hub.light_matrix.show_image('HAPPY')
            girar_num_grados_der(30)
            dist_cm = get_distance()
            if (dist_cm > 20):
                motor_pair.move_tank(3.5, 'cm', -42, 100) # Antes estaba en 24
                motor_pair.move_tank(17, 'cm', 41, 100)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_1 = sen_1.get_reflected_light()
                while (color_1 > 20): # Antes estaba en 45
                    color_1 = sen_1.get_reflected_light()
                    motor_pair.start_tank(36, 100)
                    if (timer.now() > 1):
                        color_1 = sen_1.get_reflected_light()
                        while (color_1 > 20):
                            color_1 = sen_1.get_reflected_light()
                            motor_pair.start_tank(30, 100)
                            timer.reset()
                motor_pair.start_tank(0, 0)
                hub.light_matrix.show_image('DIAMOND')
                motor_pair.move_tank(2, 'cm', 100, 100)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(100, -100)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 100, 100)
            else:
                color_2 = sen_2.get_reflected_light()
                hub.light_matrix.show_image('ANGRY')
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() > -159):
                    motor_pair.start_tank(-95, 100)
                hub.motion_sensor.reset_yaw_angle()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3.5, 'cm', 100, 60)
                motor_pair.move_tank(17, 'cm', 100, 40)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
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
                motor_pair.move_tank(2, 'cm', 100, 100)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(-100, 100)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 100, 100)
        else:
            color_2 = sen_2.get_reflected_light()
            hub.light_matrix.show_image('ANGRY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -109):
                motor_pair.start_tank(-95, 100)
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
            motor_pair.move_tank(2, 'cm', 100, 100)
            color_2 = sen_2.get_reflected_light()
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(-100, 100)
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 100, 100)

    elif (ant == 1):
        ant = 0
        hub.motion_sensor.reset_yaw_angle()
        while (hub.motion_sensor.get_yaw_angle() > -45):
            motor_pair.start_tank(-95, 100)
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(0, 0)
        dist_cm = get_distance()
        if (dist_cm > 20):
            hub.light_matrix.show_image('HAPPY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -30):
                motor_pair.start_tank(-95, 100)
            hub.motion_sensor.reset_yaw_angle()
            dist_cm = get_distance()
            if (dist_cm > 20):
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
                motor_pair.move_tank(2, 'cm', 100, 100)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(-100, 100)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 100, 100)
            else:
                color_2 = sen_2.get_reflected_light()
                hub.light_matrix.show_image('ANGRY')
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() < 170):
                    motor_pair.start_tank(100, -95)
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
                motor_pair.move_tank(2, 'cm', 100, 100)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(100, -100)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 100, 100)
        else:
            color_2 = sen_2.get_reflected_light()
            hub.light_matrix.show_image('ANGRY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() < 125):
                angle = hub.motion_sensor.get_yaw_angle()
                motor_pair.start_tank(100, -95)
                print(angle)
            hub.motion_sensor.reset_yaw_angle()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 36, 100)
            motor_pair.move_tank(17, 'cm', 34, 95)
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
            motor_pair.move_tank(2, 'cm', 100, 100)
            color_2 = sen_2.get_reflected_light()
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(100, -100)
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 100, 100)
    mostrar(nada)


####################### Funciones de Rescate################
def normalize_degs(ang):
    ang = ang % 360
    if ang < 0:
        ang += 360
    if ang == 360:
        ang = 0
    return ang

# Converts from radians to degrees
def radsToDegs(rad):
    return rad * 180 / pi

# Converts a number from a range of value to another
def map_vals(val, in_min, in_max, out_min, out_max):
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def get_degs_from_coords(coords):
    rads = atan2(coords[0], coords[1])
    return radsToDegs(rads)

# Gets the distance to given coordinates
def get_distance_from_coords(position):
    return sqrt((position[0] ** 2) + (position[1] ** 2))

# hub = PrimeHub()



"""
motor_pair = MotorPair("A", "C")
motor_pair.set_motor_rotation(1.07*pi)

distancia= DistanceSensor("E")

sen_1 = ColorSensor("B")
sen_2 = ColorSensor("D")
sen_3 = ColorSensor("F")
"""
last_dist_mes = 0
def measure_distance():
    global last_dist_mes

    dist = distancia.get_distance_cm()
    last_dist_mes = dist
    if dist is None:
        return 10000000
    if dist == 200:
        return last_dist_mes
    return dist



initial_rotation = hub.motion_sensor.get_yaw_angle() + 180


def get_rotation():
    global initial_rotation
    return normalize_degs(hub.motion_sensor.get_yaw_angle() + 180 - initial_rotation)

def rotate_to_degs(degs, orientation="closest", max_speed=100):
    print("turn to degs:", degs)
    degs = normalize_degs(degs)
    accuracy = 2
    init_rotation = get_rotation()
    initial_diff = round(init_rotation - degs)
    while True:
        diff = get_rotation() - degs
        print("degs", degs)
        print("raw_rot", hub.motion_sensor.get_yaw_angle())
        print("rot", get_rotation())
        moveDiff = max(round(get_rotation()), degs) - min(get_rotation(), degs)
        if diff > 180 or diff < -180:
            moveDiff = 360 - moveDiff
        speedFract = int(min(map_vals(moveDiff, accuracy, 20, 50, 100), max_speed))
        if accuracy * -1 < diff < accuracy or 360 - accuracy < diff < 360 + accuracy:
            break
        else:
            if orientation == "closest":
                if 180 > initial_diff > 0 or initial_diff < -180:
                    direction = "right"
                else:
                    direction = "left"
            elif orientation == "farthest":
                if 180 > initial_diff > 0 or initial_diff < -180:
                    direction = "left"
                else:
                    direction = "right"
            else:
                direction = orientation

            if direction == "right":
                motor_pair.start_tank(speedFract * -1, speedFract)
            elif direction == "left":
                motor_pair.start_tank(speedFract, speedFract * -1)
    motor_pair.stop()

def get_90_degs_distances():
    distance_sensor_radious = 4
    dists = {}

    for i in (0, 90, 180, 270):
        rotate_to_degs(i)
        dists[i] = measure_distance() + distance_sensor_radious

    return dists

def measure_and_locate():
    dists = get_90_degs_distances()

    robot_position = [dists[90], dists[0]]

    rectangle_dims = [robot_position[0] + dists[270], robot_position[1] + dists[180]]

    return rectangle_dims, robot_position

def move_to(robot_position, robot_destination, use_dist=True):
    direction = get_degs_from_coords([robot_position[0] - robot_destination[0], (robot_position[1] - robot_destination[1]) * -1])
    distance = get_distance_from_coords([robot_destination[0] - robot_position[0], robot_destination[1] - robot_position[1]])
    rotate_to_degs(direction)
    if use_dist:
        motor_pair.move(distance * -1, speed=100)
    else:
        motor_pair.start(speed=-100)
    return direction, distance

def search_silver():
    motor_pair.start(speed=-100)
    while True:
        if sen_1.get_reflected_light() > 85 and sen_3.get_reflected_light() > 85:
            break

    motor_pair.move(-20, speed=100)

def set_gyro_angle(angle):
    global initial_rotation
    wait_for_seconds(0.2)
    initial_rotation = normalize_degs(hub.motion_sensor.get_yaw_angle() + 180 - angle)
    wait_for_seconds(0.2)

def align():
    global initial_rotation
    initial_rotation = hub.motion_sensor.get_yaw_angle() + 180

    dist90 = 0

    dist270 = 0

    rotate_to_degs(90)

    dist90 = measure_distance()

    if dist90 > 30:
        rot_degs = 90

    else:
        rotate_to_degs(270)

        dist270 = measure_distance()

        rot_degs = 270

        print("dist 90:", dist90, ": dist 270:", dist270)

        if dist90 > dist270:
            rotate_to_degs(90)
            rot_degs = 90

    motor_pair.move(30, speed=100)
    motor_pair.stop()
    wait_for_seconds(0.1)
    initial_rotation = normalize_degs(hub.motion_sensor.get_yaw_angle() + 180- rot_degs)
    wait_for_seconds(0.1)
    motor_pair.move(-8, speed=100)

    return rot_degs

def go_to_closest_wall():
    dists = get_90_degs_distances()
    min_dist_degs = min(dists, key=dists.get)
    rotate_to_degs(min_dist_degs)
    motor_pair.start(speed=-100)
    while measure_distance() > 5:
        pass


def follow_wall_until_limit(wall, limit=5):
    motor_pair.start_tank(-100, -100)

    """
    if wall == "right":
        motor_pair.move(-4, steering=-80)
        motor_pair.start_tank(-100, -100)
    elif wall == "left":
        motor_pair.move(-4, steering=80)
        motor_pair.start_tank(-100, -100)
    """

    while measure_distance() > limit:
        pass

    motor_pair.stop()

def turn_corner(direction):
    if direction == "left":
        motor_pair.move(-14, steering=100)
    elif direction == "right":
        motor_pair.move(-14, steering=-100)

def move_to_corner(robot_position, corner, use_dist=True):
    global rectangle_dimensions
    corner_pos = [corner[0] * rectangle_dimensions[0], corner[1] * rectangle_dimensions[1]]
    return move_to(robot_position, corner_pos, use_dist)

##############################################################

"""while True:
    # left_right, down_up, front_back = advancedHub.motion.accelerometer()
    # print("izq_der:",left_right,"###abajo_arriba:",down_up,"###frente_atras:",front_back)
    # manzana = advancedHub.motion.orientation()
    # print(manzana)
    cont = 0
    suma = 0
    # while cont < 100:
        # left_right, down_up, front_back = advancedHub.motion.accelerometer()
        # down_up = hub.motion_sensor.get_pitch_angle()
        # suma = down_up + suma
        # cont = cont + 1
    # suma = suma / 100
    suma = hub.motion_sensor.get_pitch_angle()
    print(suma)
    motor_pair.start_tank(80,-80)"""

while True:
    update()

    if col_1 == 'plateado' or col_3 == 'plateado':
        break
    if dist_cm < 7:
        motor_pair.start_tank(0,0)
        obstacle_detection()
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
            verifica_doble_negro()
        elif luz_1 > 50 and luz_2 > 50 and luz_3 > 50:
            motor_pair.start_tank(90,90)
        # elif hub.motion_sensor.get_roll_angle() > 1 or hub.motion_sensor.get_roll_angle() < -1:
        #    mostrar(equis)
        #    loma_burro()
        else:
            # if hub.motion_sensor.get_roll_angle() > 1 or hub.motion_sensor.get_roll_angle() < -1:
            #    mostrar(equis)
            #    loma_burro()
            # else:
            error = luz_1 - luz_3
            proporcional = error
            integral = integral + error * 0.04
            derivada = (error - error_previo) / 0.04
            salida = int(kp * proporcional + ki * integral + kd * derivada)
            error_previo = error

            if luz_3 < 20 or luz_1 < 20:
                salida = int(7 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(50 + salida,50 - salida)
            elif luz_3 < 40 or luz_1 < 40:
                salida = int(3.2 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(70 + salida,70 - salida)
            else:
                salida = int(3 * proporcional + ki * integral + kd * derivada)
                motor_pair.start_tank(100 + salida,100 - salida)
            mostrar(nada)

############################################################################ RESCUE AREA ############################################################################

# MOTORES
motor_pair = MotorPair('A', 'C')
motor_pair.set_motor_rotation(1.07 * math.pi, "cm")

def do_wall_pass(alignment_angle, turn_angle, target_corner, rectangle_dimensions, wall_alignment="x", start_corner=(0, 0), sensor_forward=True, searching_step=10, stop_distance=10, init_start_distance=10, last_pass=True):
    global motor_pair

    margin = 5

    turn_angle = normalize_degs(turn_angle)

    if sensor_forward:
        if wall_alignment == "x":
            start_distance = rectangle_dimensions[0] - init_start_distance
        elif wall_alignment == "y":
            start_distance = rectangle_dimensions[1] - init_start_distance

    else:
        start_distance = init_start_distance

    while True:
        rotate_to_degs(turn_angle)

        if sensor_forward:
            motor_pair.start(speed=100)
            while True:
                distance = measure_distance()
                if distance > start_distance:
                    break
            motor_pair.stop()
            motor_pair.start(speed=-100)
            while True:
                distance = measure_distance()
                if distance < start_distance or distance < stop_distance:
                    break
            motor_pair.stop()

            distance = measure_distance()
            if wall_alignment == "x":
                if start_corner == (0, 0):
                    robot_position = [rectangle_dimensions[0] - distance, margin]
                elif start_corner == (0, 1):
                    robot_position = [rectangle_dimensions[0] - distance, rectangle_dimensions[1] - margin]
                elif start_corner == (1, 1):
                    robot_position = [distance, rectangle_dimensions[1] - margin]
                elif start_corner == (1, 0):
                    robot_position = [distance, margin]
            else:
                if start_corner == (0, 0):
                    robot_position = [margin, rectangle_dimensions[1] - distance]
                elif start_corner == (0, 1):
                    robot_position = [margin, distance]
                elif start_corner == (1, 1):
                    robot_position = [rectangle_dimensions[0] - margin, distance]
                elif start_corner == (1, 0):
                    robot_position = [rectangle_dimensions[0] - margin, rectangle_dimensions[1] - distance]

            if distance < stop_distance:
                break
            start_distance -= searching_step

        else:
            motor_pair.start(speed=-100)
            while True:
                distance = measure_distance()
                if distance < start_distance:
                    break
            motor_pair.stop()
            motor_pair.start(speed=100)
            while True:
                distance = measure_distance()
                if wall_alignment == "x":
                    if distance > start_distance or distance > rectangle_dimensions[0] - stop_distance:
                        break
                elif wall_alignment == "y":
                    if distance > start_distance or distance > rectangle_dimensions[1] - stop_distance:
                        break

            motor_pair.stop()

            distance = measure_distance()
            if wall_alignment == "x":
                if start_corner == (0, 0):
                    robot_position = [distance, margin]
                elif start_corner == (0, 1):
                    robot_position = [distance, rectangle_dimensions[1] - margin]
                elif start_corner == (1, 1):
                    robot_position = [rectangle_dimensions[0] - distance, rectangle_dimensions[1] - margin]
                elif start_corner == (1, 0):
                    robot_position = [rectangle_dimensions[0] - distance, margin]

            else:
                if start_corner == (0, 0):
                    robot_position = [margin, distance]
                elif start_corner == (0, 1):
                    robot_position = [margin, rectangle_dimensions[1] - distance]
                elif start_corner == (1, 1):
                    robot_position = [rectangle_dimensions[0] - margin, rectangle_dimensions[1] - distance]
                elif start_corner == (1, 0):
                    robot_position = [rectangle_dimensions[0] - margin, distance]

            if (wall_alignment == "x" and distance > rectangle_dimensions[0] - stop_distance) or (wall_alignment == "y" and distance > rectangle_dimensions[1] - stop_distance):
                break
            start_distance += searching_step

        ang, dist = move_to_corner(robot_position, target_corner, use_dist=False)
        while sen_2.get_reflected_light() > 40:
            pass

        rotate_to_degs(ang)

        motor_pair.move(dist - 30 + margin, speed=100)
        rotate_to_degs(alignment_angle)

        motor_pair.move(5)

        set_gyro_angle(alignment_angle)

    if last_pass:
        ang, dist = move_to_corner(robot_position, target_corner, use_dist=False)
        while sen_2.get_reflected_light() > 40:
            pass

        rotate_to_degs(ang)

        #motor_pair.move(max(rectangle_dimensions) + 20, speed=100)
        motor_pair.move(dist - 30 + margin, speed=100)
        rotate_to_degs(alignment_angle)

        motor_pair.move(5)

        set_gyro_angle(alignment_angle)




possible_corners = [(0, 0), (0, 1), (1, 1), (1, 0)]

motor_pair.move(-30)

aligned_degs = align()

#motor_pair.move(-30, speed=100)

rectangle_dimensions = [120, 90]
#rectangle_dimensions, robot_position = measure_and_locate()

#motor_pair.move(30, speed=100)

SEARCHING_STEP = 20

STOP_DISTANCE = 20

if aligned_degs == 270:
    black_corner = None
    for corner, direction in zip(((0, 1), (1, 1), (1, 0), (0, 0)), (0, 270, 180, 90)):
        rotate_to_degs(normalize_degs(direction + 20))
        follow_wall_until_limit("right", limit=8)
        if sen_2.get_reflected_light() < 40:
            hub.light_matrix.show_image('HAPPY')
            black_corner = corner
            break

    if black_corner == (1, 1):
        motor_pair.move(rectangle_dimensions[0], speed=100)
        set_gyro_angle(270)
        robot_position = [10, rectangle_dimensions[1]]

        #FIRST WALL
        do_wall_pass(
            alignment_angle=270,
            turn_angle=0,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="y",
            start_corner=(0, 1),
            sensor_forward=False,
            searching_step=20,
            stop_distance=20,
            init_start_distance=20,
            last_pass=False)

        rotate_to_degs(270)
        motor_pair.move(-30)
        rotate_to_degs(0)
        motor_pair.move(15)
        set_gyro_angle(0)
        robot_position = [30, 10]

        #SECOND WALL

        do_wall_pass(
            alignment_angle=0,
            turn_angle=270,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="x",
            start_corner=(0, 0),
            sensor_forward=True,
            searching_step=20,
            stop_distance=10,
            init_start_distance=40)

        rotate_to_degs(270)
        motor_pair.move(rectangle_dimensions[0], speed=100)
        motor_pair.move(-5)
        rotate_to_degs(180)
        motor_pair.move(-30)


    elif black_corner == (1, 0):
        motor_pair.move(rectangle_dimensions[1], speed=100)
        set_gyro_angle(180)
        robot_position = [rectangle_dimensions[0], rectangle_dimensions[1]]

        #FIRST WALL
        do_wall_pass(
            alignment_angle=180,
            turn_angle=90,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="x",
            start_corner=(1, 1),
            sensor_forward=True,
            searching_step=20,
            stop_distance=20,
            init_start_distance=20)

        robot_position = [0, rectangle_dimensions[1]]

        hub.speaker.beep(70, 1)

        rotate_to_degs(270)
        motor_pair.move(20)

        set_gyro_angle(270)

        #SECOND WALL
        do_wall_pass(
            alignment_angle=270,
            turn_angle=0,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="y",
            start_corner=(0, 1),
            sensor_forward=False,
            searching_step=20,
            stop_distance=20,
            init_start_distance=20,
            last_pass=False)

        motor_pair.move(40)

    elif black_corner == (0, 1):
        rotate_to_degs(0)
        motor_pair.start(speed=100)
        while measure_distance() < rectangle_dimensions[1] - (SEARCHING_STEP + 5):
            pass
        motor_pair.stop()
        rotate_to_degs(270)
        motor_pair.move(-30)
        rotate_to_degs(0)
        motor_pair.move(15)
        set_gyro_angle(0)

        #FIRST WALL
        do_wall_pass(
            alignment_angle=0,
            turn_angle=270,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="x",
            start_corner=(0, 0),
            sensor_forward=True,
            searching_step=20,
            stop_distance=20,
            init_start_distance=40)

        rotate_to_degs(90)
        motor_pair.move(20)
        set_gyro_angle(90)

        #SECOND WALL
        do_wall_pass(
            alignment_angle=90,
            turn_angle=0,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="y",
            start_corner=(1, 0),
            sensor_forward=True,
            searching_step=20,
            stop_distance=15,
            init_start_distance=20)


        robot_position = [rectangle_dimensions[0], rectangle_dimensions[1] - 15]
        move_to_corner(robot_position, (0, 0))
        rotate_to_degs(180)
        motor_pair.move(-30)


elif aligned_degs == 90:
    black_corner = None
    for corner, direction in zip(((1, 1), (0, 1), (0, 0), (1, 0)), (0, 90, 180, 270)):
        rotate_to_degs(normalize_degs(direction - 20))
        follow_wall_until_limit("left", limit=8)
        if sen_2.get_reflected_light() < 40:
            hub.light_matrix.show_image('HAPPY')
            black_corner = corner
            break


    if black_corner == (1, 1):
        motor_pair.start(speed=100)
        while measure_distance() < rectangle_dimensions[1] - SEARCHING_STEP:
            pass
        motor_pair.stop()
        rotate_to_degs(90)
        motor_pair.move(-35)
        rotate_to_degs(0)
        motor_pair.move(15)
        set_gyro_angle(0)

        #FIRST WALL
        do_wall_pass(
            alignment_angle=0,
            turn_angle=270,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="x",
            start_corner=(1, 0),
            sensor_forward=False,
            searching_step=20,
            stop_distance=20,
            init_start_distance=30)

        rotate_to_degs(0)
        motor_pair.move(15)
        set_gyro_angle(0)
        motor_pair.move(-5)
        rotate_to_degs(270)
        motor_pair.move(15)
        set_gyro_angle(270)

        #SECOND WALL
        do_wall_pass(
            alignment_angle=270,
            turn_angle=0,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="y",
            start_corner=(0, 0),
            sensor_forward=True,
            searching_step=20,
            stop_distance=10,
            init_start_distance=20)


    elif black_corner == (0, 1):
        motor_pair.move(max(rectangle_dimensions), speed=100)
        set_gyro_angle(90)
        robot_position = [rectangle_dimensions[0], rectangle_dimensions[1]]

        #FIRST WALL
        do_wall_pass(
            alignment_angle=90,
            turn_angle=0,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="y",
            start_corner=(1, 1),
            sensor_forward=False,
            searching_step=20,
            stop_distance=20,
            init_start_distance=20,
            last_pass=False)

        rotate_to_degs(90)
        motor_pair.move(20)
        set_gyro_angle(90)
        motor_pair.move(-40)
        rotate_to_degs(0)
        motor_pair.move(15)
        set_gyro_angle(0)

        #SECOND WALL
        do_wall_pass(
            alignment_angle=0,
            turn_angle=90,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="x",
            start_corner=(1, 0),
            sensor_forward=True,
            searching_step=20,
            stop_distance=10,
            init_start_distance=40)

    elif black_corner == (0, 0):
        motor_pair.move(max(rectangle_dimensions), speed=100)
        set_gyro_angle(180)
        robot_position = [0, 0]

        #FIRST WALL
        do_wall_pass(
            alignment_angle=180,
            turn_angle=270,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="x",
            start_corner=(0, 1),
            sensor_forward=True,
            searching_step=20,
            stop_distance=15,
            init_start_distance=20)

        rotate_to_degs(90)
        motor_pair.move(15)
        set_gyro_angle(90)

        #SECOND WALL
        do_wall_pass(
            alignment_angle=90,
            turn_angle=0,
            target_corner=black_corner,
            rectangle_dimensions=rectangle_dimensions,
            wall_alignment="y",
            start_corner=(1, 1),
            sensor_forward=False,
            searching_step=20,
            stop_distance=20,
            init_start_distance=20,
            last_pass=False)

        motor_pair.move(20)
