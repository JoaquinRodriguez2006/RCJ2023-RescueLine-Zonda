from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
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

def distance_com():
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

ant = 0

def obstacle_detection():
    global ant
    global s
    global dist
    dist = 0
    distance_com()
    print("Primer While")        #########################################
    while (dist != 1):  # distancia mayor a 5
        motor_pair.start_tank(20, 20)
        distance_com()
    color_2 = sen_2.get_reflected_light()
    girar_num_grados_der(16)
    color_2 = sen_2.get_reflected_light()
    print("Segundo While")        #########################################
    while (color_2 > 19):
        color_2 = sen_2.get_reflected_light()
        motor_pair.start_tank(-20,20)
    motor_pair.start_tank(0, 0)
    distance_com()
    print("Tercer While")        #########################################
    while (dist <= 3): # distancia menor a 10
        motor_pair.start_tank(-20, -20)
        distance_com()
    motor_pair.start_tank(0, 0)
    motor_pair.move_tank(1, 'cm', -20, -20)
    print("Pregunta por el Ant")        #########################################
    if (ant == 0):
        ant = 1
        girar_num_grados_der(45)
        distance_com()
        print("Primer if")        #########################################
        if (dist == 6):# si la distancia es mayor a 20
            hub.light_matrix.show_image('HAPPY')
            girar_num_grados_der(30)
            distance_com()
            print("Segundo if")        #########################################
            if (dist == 6):# si la distancia es mayor a 20
                motor_pair.move_tank(3.5, 'cm', -21, 50) # Antes estaba en 24
                motor_pair.move_tank(17, 'cm', 21, 50)
                # hub.light_matrix.show_image('HEART')
                timer.reset()
                color_1 = sen_1.get_reflected_light()
                print("Cuarto While")        #########################################
                while (color_1 > 20): # Antes estaba en 45
                    color_1 = sen_1.get_reflected_light()
                    motor_pair.start_tank(18, 50)
                    if (timer.now() > 1):
                        color_1 = sen_1.get_reflected_light()
                        print("Quinto While")        #########################################
                        while (color_1 > 20):
                            color_1 = sen_1.get_reflected_light()
                            motor_pair.start_tank(15, 50)
                            timer.reset()
                motor_pair.start_tank(0, 0)
                hub.light_matrix.show_image('DIAMOND')
                motor_pair.move_tank(2, 'cm', 20, 20)
                color_2 = sen_2.get_reflected_light()
                print("Sexto While")        #########################################
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(20, -20)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 20, 20)
            else:
                print("Primer else")        #########################################
                color_2 = sen_2.get_reflected_light()
                hub.light_matrix.show_image('ANGRY')
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() > -159):
                    motor_pair.start_tank(-2, 20)
                hub.motion_sensor.reset_yaw_angle()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3.5, 'cm', 33, 20)
                motor_pair.move_tank(17, 'cm', 25, 10)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                print("While el Else")        #########################################
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(50, 18)
                    if (timer.now() > 1.5):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(60, 15) # Antes eran 80/18
                            timer.reset()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(2, 'cm', 20, 20)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(-20, 20)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 20, 20)
        else:
            print("Segundo Else")        #########################################
            color_2 = sen_2.get_reflected_light()
            hub.light_matrix.show_image('ANGRY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -109):
                motor_pair.start_tank(-20, 20)
            hub.motion_sensor.reset_yaw_angle()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(4.8, 'cm', 25, 22)
            motor_pair.move_tank(13, 'cm', 45, 20)
            hub.light_matrix.show_image('HEART')
            timer.reset()
            color_2 = sen_2.get_reflected_light()
            while (color_2 > 20): # Antes estaba en 45
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(50, 20)
                if (timer.now() > 1.5):
                    color_2 = sen_2.get_reflected_light()
                    while (color_2 > 20):
                        color_2 = sen_2.get_reflected_light()
                        motor_pair.start_tank(50, 10) # Antes eran 80/18
                        timer.reset()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(2, 'cm', 20, 20)
            color_2 = sen_2.get_reflected_light()
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(-20, 20)
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 20, 20)

    elif (ant == 1):
        print("El Elif")        #########################################
        ant = 0
        hub.motion_sensor.reset_yaw_angle()
        while (hub.motion_sensor.get_yaw_angle() > -45):
            motor_pair.start_tank(-20, 20)
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(0, 0)
        distance_com()
        print("Otro IF")        #########################################
        if (dist == 6):    # si distancia es mayor a 20
            hub.light_matrix.show_image('HAPPY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() > -30):
                motor_pair.start_tank(-20, 20)
            hub.motion_sensor.reset_yaw_angle()
            distance_com()
            print("Segundo Otro IF")        #########################################
            if (dist == 6):    # si distancia es mayor a 20
                motor_pair.move_tank(3, 'cm', 48, -20) # Antes estaba en 24
                motor_pair.move_tank(17, 'cm', 46, 18)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(46, 17)
                    if (timer.now() > 1.2):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(46, 14)
                            timer.reset()
                motor_pair.start_tank(0, 0)
                hub.light_matrix.show_image('DIAMOND')
                motor_pair.move_tank(2, 'cm', 20, 20)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(-20, 20)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 20, 20)
            else:
                color_2 = sen_2.get_reflected_light()
                hub.light_matrix.show_image('ANGRY')
                hub.motion_sensor.reset_yaw_angle()
                while (hub.motion_sensor.get_yaw_angle() < 170):
                    motor_pair.start_tank(20, -45)
                hub.motion_sensor.reset_yaw_angle()
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(4, 'cm', -22, 50)
                motor_pair.move_tank(13, 'cm', 22, 50)
                hub.light_matrix.show_image('HEART')
                timer.reset()
                color_2 = sen_2.get_reflected_light()
                while (color_2 > 20): # Antes estaba en 45
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(20, 40)
                    if (timer.now() > 1.5):
                        color_2 = sen_2.get_reflected_light()
                        while (color_2 > 20):
                            color_2 = sen_2.get_reflected_light()
                            motor_pair.start_tank(16, 80) # Antes eran 80/18
                            timer.reset()
                motor_pair.start_tank(0, 0)
                hub.light_matrix.show_image('DIAMOND')
                motor_pair.move_tank(2, 'cm', 20, 20)
                color_2 = sen_2.get_reflected_light()
                while color_2 > 20:
                    color_2 = sen_2.get_reflected_light()
                    motor_pair.start_tank(20, -20)
                motor_pair.start_tank(0, 0)
                motor_pair.move_tank(3, 'cm', 20, 20)
        else:
            print("Ultimo Else")        #########################################
            color_2 = sen_2.get_reflected_light()
            hub.light_matrix.show_image('ANGRY')
            hub.motion_sensor.reset_yaw_angle()
            while (hub.motion_sensor.get_yaw_angle() < 125):
                angle = hub.motion_sensor.get_yaw_angle()
                motor_pair.start_tank(20, -20)
                # print(angle)
            hub.motion_sensor.reset_yaw_angle()
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 18, 50)
            motor_pair.move_tank(17, 'cm', 17, 50)
            hub.light_matrix.show_image('HEART')
            timer.reset()
            color_2 = sen_2.get_reflected_light()
            while (color_2 > 20): # Antes estaba en 45
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(17, 50)
                if (timer.now() > 1.2):
                    color_2 = sen_2.get_reflected_light()
                    while (color_2 > 20):
                        color_2 = sen_2.get_reflected_light()
                        motor_pair.start_tank(13, 50) # Antes eran 80/18
                        timer.reset()
            motor_pair.start_tank(0, 0)
            hub.light_matrix.show_image('DIAMOND')
            motor_pair.move_tank(2, 'cm', 20, 20)
            color_2 = sen_2.get_reflected_light()
            while color_2 > 20:
                color_2 = sen_2.get_reflected_light()
                motor_pair.start_tank(20, -20)
            motor_pair.start_tank(0, 0)
            motor_pair.move_tank(3, 'cm', 20, 20)

b.write("Seguidor\n")
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
        #if get_distance() != 'N', 'S', 'L', 'M':
        #    motor_pair.stop()
        #else:
        #    pass
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

last_dist_mes = 0
def measure_distance():
    global last_dist_mes

    dist = get_distance()
    last_dist_mes = dist
    if dist is None:
        return 10000000
    if dist == 'N':
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
    while measure_distance() > 'L':
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

######################################################################################## MAIN CODE ########################################################################################

state = 'start'
while True:
    motor_pair.start(speed=30)
    while True:
        if sen_1.get_reflected_light() > 85 and sen_3.get_reflected_light() > 85:
            state = 'RescueArea'

        if state == 'Rescue Area':
        # First Turn
            motor_pair.move_tank(9, 'cm', left_speed=50, right_speed=50)
            motor_pair.start_tank(0,0)
            giro_90_izq()
            giro_90_der()
        """# Second Turn
            motor_pair.move_tank(15, 'cm', left_speed=50, right_speed=50)
            motor_pair.start_tank(0,0)
            giro_90_izq()
        # Third Turn
            motor_pair.move_tank(15, 'cm', left_speed=50, right_speed=50)
            motor_pair.start_tank(0,0)
            giro_90_izq()
            giro_90_der()
        # Fourth Turn
            motor_pair.move_tank(15, 'cm', left_speed=50, right_speed=50)
            motor_pair.start_tank(0,0)
            giro_90_izq()
        # Fifth Turn
            motor_pair.move_tank(15, 'cm', left_speed=50, right_speed=50)
            motor_pair.start_tank(0,0)
            giro_90_izq()
        # Sixth Turn
            motor_pair.move_tank(15, 'cm', left_speed=50, right_speed=50)
            motor_pair.start_tank(0,0)
            giro_90_izq()
        # Seventh Turn
            motor_pair.move_tank(15, 'cm', left_speed=50, right_speed=50)
            motor_pair.start_tank(0,0)
            giro_90_izq()
        # Eighth Turn
            motor_pair.move_tank(15, 'cm', left_speed=50, right_speed=50)
            motor_pair.start_tank(0,0)
            giro_90_izq()
        # Nineth Turn
            motor_pair.move_tank(15, 'cm', left_speed=50, right_speed=50)
            motor_pair.start_tank(0,0)
            giro_90_izq()
        # Tenth Turn
            motor_pair.move_tank(15, 'cm', left_speed=50, right_speed=50)
            motor_pair.start_tank(0,0)
            giro_90_izq()"""