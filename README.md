# RS485 Communication
## How to install
Copy <b>Communication</b> folder and <i>requirements.txt</i> file to your workspace (folder) project. <br>

Same level with your main python file (ex: <i>main.py</i>).<br>

Then, run this command:
```
pip3 install -r requirements.txt
```
## How to use
Follow file <i>main.py</i>:
```
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
```

## NOTE
On-develop with <i>Communication/SubFunctions.py</i>