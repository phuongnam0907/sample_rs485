#!/usr/bin/python3

import os
import time
import logging
import serial


class SerialPort(object):
    FAILED = -1
    SUCCESS = 0

    def __init__(self, port, baudrate):
        self._path = os.path.abspath(os.getcwd()) + "/log"
        if not os.path.exists(self._path):
            os.mkdir("log", mode=0o777, dir_fd=None)

        # Set basic config
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename="log/" + str(__name__) + ".log",
                            filemode='w')
        # Create handlers
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        # Set a format which is simpler for console use
        formatter_console = logging.Formatter('%(name)-12s: %(levelname)-8s| %(message)s')
        # tell the handler to use this format
        console_handler.setFormatter(formatter_console)
        logging.getLogger('').addHandler(console_handler)

        # Create Logger
        self._logger = logging.getLogger(__name__)

        self._port = port
        self._baudrate = baudrate

        self._logger.info("Config serial with Port {} - Baudrate {}".format(self._port, self._baudrate))
        self._serial = serial.Serial(self._port, self._baudrate)

    def open(self):
        self._logger.info("Opening port {}...".format(self._port))
        try:
            if not self._serial.isOpen():
                self._serial.open()
            time.sleep(0.1)
            if self._serial.isOpen():
                self._logger.info("Port {} is opened!".format(self._port))
        except:
            self._logger.error("Failed to open Serial port {}".format(self._port))

    def close(self):
        self._logger.info("Closing port {}...".format(self._port))
        try:
            if self._serial.isOpen():
                self._serial.close()
            time.sleep(0.1)
            if not self._serial.isOpen():
                self._logger.info("Port {} is closed!".format(self._port))
        except:
            self._logger.error("Failed to close Serial port {}".format(self._port))

    def read_sensor(self, data, timeout=1000):
        value = SerialPort.FAILED

        if data is None or len(data) == 0:
            self._logger.error("Input data is empty")
            return SerialPort.FAILED

        self._logger.info("Getting sensor data from port {}...".format(self._port))
        if self._serial.isOpen():
            self._logger.debug("Writing data: {}".format(data))
            self._serial.write(serial.to_bytes(data))
            time.sleep(0.5)
            bytes_to_read = self._serial.inWaiting()
            if bytes_to_read > 0:
                out = self._serial.read(bytes_to_read)
                data_array = [b for b in out]
                self._logger.debug("Reading data: {} - Length is {}".format(out, len(data_array)))
                if len(data_array) >= 7:
                    array_size = len(data_array)
                    value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
        else:
            self._logger.error("Port {} is not opened.".format(self._port))

        return value
