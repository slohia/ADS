######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : machine_address.py
## Description  : program to get the machine address
## Author       : Manish Choudhary
## Start Date   : 22 APR 2014
## Last Revised :
## (Code Adopted from http://stackoverflow.com/questions/11735821/python-get-localhost-ip)
######################################################################################
import os
import socket
import fcntl
import struct


class MachineAddress:

    def __init__(self):
        pass

    def get_interface_ip(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

    def get_lan_ip(self):
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127.") and os.name != "nt":
            interfaces = [
                "eth0",
                "eth1",
                "eth2",
                "wlan0",
                "wlan1",
                "wifi0",
                "ath0",
                "ath1",
                "ppp0",
                ]
            for ifname in interfaces:
                try:
                    ip = self.get_interface_ip(ifname)
                    break
                except IOError:
                    pass
        return ip