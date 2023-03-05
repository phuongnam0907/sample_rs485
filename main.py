from Communication.SerialCommunication import SerialPort
from Communication import SubFunctions as comFuncs

if __name__ == '__main__':
    data = [3, 3, 0, 0, 0, 1, 133, 232]

    port = comFuncs.find_serial_port()
    baudrate = comFuncs.find_serial_baudrate()
    print("Find port {} - baudrate {}".format(port, baudrate))

    serial = SerialPort(port=port, baudrate=baudrate)
    serial.open()

    ret = serial.read_sensor(data)
    print(ret)