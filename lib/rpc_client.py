######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : rpc_server.py
## Description  : module to provide client side rpc functionality
## Author       : Manish Choudhary
## Start Date   : 20 MAR 2014
## Last Revised :
######################################################################################
import xmlrpclib
import socket


class RPCClient:

    def __init__(self):
        self.machine_ip = socket.gethostbyname(socket.gethostname())
        #self.machine_ip = '192.168.1.1'
        self.machine_name = socket.gethostname()
        self.rpc_server = 'http://localhost:8006'

    def get_uid_from_server(self):
        server = xmlrpclib.Server(self.rpc_server)
        return server.get_uid(self.machine_name, self.machine_ip)

    def get_existing_uid_from_server(self):
        pass  # Implement this to get the existing UID in case the client crashes and wants to continue with the same ID
              # Not implementing for now. Have to think about the attack surface it may expose.

if __name__ == "__main__":
    rpc = RPCClient()
    print rpc.get_uid_from_server()