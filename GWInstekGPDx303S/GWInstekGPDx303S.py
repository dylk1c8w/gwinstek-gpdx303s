"""package for GW Instek power supply GPDx303S"""


import time
import serial
import numpy as np


__author__ = "Yuta Kawai <pygo3xmdy11u@gmail.com>"
__status__ = "production"
__version__ = "0.0.0"
__date__ = "2021/09/02"


# constants
# IO_DICT = {0: "OFF", 1: "ON"}
# TRACKINGMODE_DICT = {0:"独立", 1:"直列トラッキング", 2:"並列トラッキング"}
# BAUDRATE_DICT = {0: 115200, 1: 57600, 2: 9600}


class GWInstekGPDx303S:
    def __init__(self, port):
        """establishe communication with the GWInstek GPDx303S

        Parameters
        ----------
        port : str
            port of GWInstek GPDx303S
        """
        self.port = port
        self.instrument = None
        self.current_step = 0.05
        self.voltage_step = 0.05
        self.time_interval = 0.05
        self.baudrate = 9600
        self.time_out = 1.0
        self.connect(port=self.port)

    def __del__(self):
        """close communication with the GWInstek GPDx303S if the program shutdown 
        suddenly by error"""
        self.close()

    def set_current_step(self, current_step):
        """set current step
        
        Parameters
        ----------
        current_step : float
            current step when changing the current value of the power supply 
            gradually
        """
        self.current_step = current_step

    def get_current_step(self):
        """get current step
        
        Returns
        -------
        float
            current step when changing the current value of the power supply 
            gradually
        """
        return self.current_step

    def set_voltage_step(self, voltage_step):
        """set voltage step
        
        Parameters
        ----------
        voltage_step : float
            voltage step when changing the voltage value of the power supply 
            gradually
        """
        self.voltage_step = voltage_step

    def get_voltage_step(self):
        """get voltage step
        
        Returns
        -------
        float
            voltage step when changing the voltage value of the power supply 
            gradually
        """
        return self.voltage_step

    def set_time_interval(self, time_interval):
        """set time interval

        Parameters
        ----------
        time_interval : float
            time interval of command
        """
        self.time_interval = time_interval

    def get_time_interval(self):
        """get time interval

        Returns
        -------
        float
            time interval of command
        """
        return self.time_interval

    def set_time_out(self, time_out):
        """set time out

        Parameters
        ----------
        time_out : float
            The time taken to forcibly terminate a process or data transfer in the 
            middle when it is taking too long.
        """
        self.time_out = time_out

    def get_time_out(self):
        """get time out

        Returns
        -------
        float
            The time taken to forcibly terminate a process or data transfer in the 
            middle when it is taking too long.
        """
        return self.time_out

    def connect(self, port):
        """establishe communication with the GWInstek GPDx303S

        Parameters
        ----------
        port : str
            port of GWInstek GPDx303S
        """
        if port != self.port:
            if self.instrument != None:
                self.close()
            self.port = port
        if self.instrument == None:
            self.instrument = serial.Serial(
                port=port, baudrate=self.baudrate, timeout=self.time_out
            )
            self.REMOTE()

    def close(self):
        """close communication with the GWInstek GPDx303S"""
        if self.instrument != None:
            self.instrument.close()
            self.instrument = None

    def write_command(self, command):
        """write command to the GWInstek GPDx303S

        Parameters
        ----------
        command : str
            command sent to GWInstek GPDx303S
        """
        command = "{}\r\n".format(command)
        self.instrument.write(command.encode("utf-8"))

    def read_command(self):
        """read command to the GWInstek GPDx303S

        Returns
        -------
        str
            string returned from GWInstek GPDx303S
        """
        return str(self.instrument.read_until())[2:-5]

    def query_command(self, command):
        """query command to the GWInstek GPDx303S

        Parameters
        ----------
        command : str
            command sent to GWInstek GPDx303S

        Returns
        -------
        str
            string returned from GWInstek GPDx303S
        """
        self.write_command(command)
        time.sleep(self.time_interval)
        return self.read_command()

    def get_output_status(self):
        """get output status of the GWInstek GPDx303S
        
        Returns
        -------
        int
            output status of the GWInstek GPDx303S
            (0: OFF, 1: ON)
        """
        return int(self.STATUS()[5])

    def on(self):
        """set output ON"""
        self.OUT(1)

    def off(self):
        """set output OFF"""
        self.OUT(0)

    def set_current(self, channel, current):
        """set current
        
        Parameters
        ----------
        channel : int
            channel to change the value of the current
        current : float
            value of current
        """
        self.ISET(channel, current)

    def set_voltage(self, channel, voltage):
        """set voltage
        
        Parameters
        ----------
        channel : int
            channel to change the value of the voltage
        current : float
            value of voltage
        """
        self.VSET(channel, voltage)

    def set_current_quickly(self, channel, current):
        """set current quickly
        
        Parameters
        ----------
        channel : int
            channel to change the value of the current
        current : float
            value of current
        """
        self.ISET(channel, current)

    def set_voltage_quickly(self, channel, voltage):
        """set voltage quickly
        
        Parameters
        ----------
        channel : int
            channel to change the value of the voltage
        current : float
            value of voltage
        """
        self.VSET(channel, voltage)

    def set_current_slowly(self, channel, current):
        """set current slowly
        
        Parameters
        ----------
        channel : int
            channel to change the value of the current
        current : float
            value of current
        """
        if self.get_output_status() == 1:
            present_current = self.IGET(channel)
            if present_current > current:
                current_list = np.arange(present_current, current, -self.current_step)
            else:
                current_list = np.arange(present_current, current, self.current_step)
            for current_value in current_list:
                self.ISET(channel, round(current_value, 3))
                time.sleep(self.time_interval)
        self.ISET(channel, current)

    def set_voltage_slowly(self, channel, voltage):
        """set voltage slowly
        
        Parameters
        ----------
        channel : int
            channel to change the value of the voltage
        current : float
            value of voltage
        """
        if self.get_output_status() == 1:
            present_voltage = self.VGET(channel)
            if present_voltage > voltage:
                voltage_list = np.arange(present_voltage, voltage, -self.voltage_step)
            else:
                voltage_list = np.arange(present_voltage, voltage, self.voltage_step)
            for voltage_value in voltage_list:
                self.VSET(channel, round(voltage_value, 3))
                time.sleep(self.time_interval)
        self.VSET(channel, voltage)

    def turn_off(self):
        """turn off the power supply"""
        self.idn = self.IDN()
        if self.idn[14:18] == "3303":
            channel_list = (1, 2)
        elif self.idn[14:18] == "4303":
            channel_list = (1, 2, 3, 4)
        for ch in channel_list:
            self.set_voltage_slowly(ch, 0.0)
        self.Off()

    def ISET(self, channel, current):
        """set the value of current

        Parameters
        ----------
        channel : int
            channel to change the value of the current
        current : float
            value of current
        """
        command = "ISET{0}:{1}".format(channel, round(current, 3))
        self.write_command(command)

    def IGET(self, channel):
        """get the value of current

        Returns
        -------
        float
            value of current
        """
        command = "ISET{}?".format(channel)
        return float(self.query_command(command)[:-1])

    def VSET(self, channel, voltage):
        """set the value of voltage

        Parameters
        ----------
        channel : int
            channel to change the value of the voltage
        voltage : float
            value of voltage
        """
        command = "VSET{0}:{1}".format(channel, round(voltage, 3))
        self.write_command(command)

    def VGET(self, channel):
        """get the value of voltage

        Returns
        -------
        float
            value of voltage
        """
        command = "VSET{}?".format(channel)
        return float(self.query_command(command)[:-1])

    def IOUT(self, channel):
        """get actual output current

        Parameters
        ----------
        channel : int
            channel to change the value of the current
        current : float
            value of actual output current
        """
        command = "IOUT{}?".format(channel)
        return float(self.query_command(command)[:-1])

    def VOUT(self, channel):
        """get actual output voltage

        Parameters
        ----------
        channel : int
            channel to change the value of the voltage
        voltage : float
            value of actual output voltage
        """
        command = "VOUT{}?".format(channel)
        return float(self.query_command(command))

    def TRACK(self, mode):
        """set the output of the power supply working on independent or tracking mode

        Parameters
        ----------
        mode : int
            tracking mode of GWInstek GPDx303S
            (0: independence, 1: series tracking, 2: parallel tracking)
        """
        command = "TRACK{}".format(mode)
        self.write_command(command)

    def BEEP(self, io):
        """set the BEEP state on or off
        
        Parameters
        ----------
        io : int
            BEEP state of the GWInstek GPDx303S
            (0: OFF, 1: ON)
        """
        command = "BEEP{}".format(io)
        self.write_command(command)

    def OUT(self, io):
        """Set the output state on or off
        
        Parameters
        ----------
        io : int
            output state of the GWInstek GPDx303S
            (0: OFF, 1: ON)
        """
        command = "OUT{}".format(io)
        self.write_command(command)

    def STATUS(self):
        """get the power supply state
        
        Returns
        -------
        str
            state of GWInstek GPDx303S
        """
        command = "STATUS?"
        return self.query_command(command)

    def IDN(self):
        """get instrument identification
        
        Returns
        -------
        str
            instrument identification
        """
        command = "*IDN?"
        return self.query_command(command)

    def RCL(self, memory_number):
        """recall the setting data from the memory which previous saved
        
        Parameters
        ----------
        memory_number : int
            number of memory which previous saved
        """
        command = "RCL{}".format(memory_number)
        self.write_command(command)

    def SAV(self, memory_number):
        """save the setting data to memory
        
        Paremeters
        ----------
        memory_number : int
            number of memory which you want to save the setting data to
        """
        command = "SAV{}".format(memory_number)
        self.write_command(command)

    def BAUD(self, baudrate):
        """set the value of baud rate
        
        Parameters
        ----------
        baudrate : int
            baud rate(0: 115200, 1: 57600, 2: 9600)
        """
        command = "BAUD{}".format(baudrate)
        self.write_command(command)

    def LOCAL(self):
        """return to local mode"""
        command = "LOCAL"
        self.write_command(command)

    def REMOTE(self):
        """return to remote mode"""
        command = "REMOTE"
        self.write_command(command)

    def ERR(self):
        """get instrument error messages
        
        Returns
        -------
        str
            error messages
        """
        command = "ERR?"
        return self.query_command(command)

    def HELP(self):
        """get command list
        
        Returns
        -------
        str
            command list
        """
        command = "HELP?"
        return self.query_command(command)
