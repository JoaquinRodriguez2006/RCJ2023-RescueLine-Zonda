import serial
# USB:
connection = serial.Serial('COM3', 115200, timeout=0.1)
# Bluetooth:
#connection = serial.Serial('/dev/rfcomm0', timeout=0.1)
# send command to the interpreter
connection.write("<<mover:2,valor_sens:4>>".encode("utf_8"))

connection.close()