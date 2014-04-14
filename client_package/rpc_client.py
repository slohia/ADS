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

    def __init__(self, ads):
        self.config = ads.config
        self.log = ads.log
        self.machine_ip = socket.gethostbyname(socket.gethostname())
        self.machine_name = socket.gethostname()
        self.primary_server_ip = self.config.env["primary_server_ip"]
        self.secondary_server_ip = self.config.env["secondary_server_ip"]
        self.server_port = self.config.env["server_port"]
        self.rpc_server = 'http://'+self.primary_server_ip+':'+self.server_port
        self.server = xmlrpclib.Server(self.rpc_server)

    def get_uid_from_server(self):
        try:
            return self.server.get_uid(self.machine_name, self.machine_ip)
        except Exception, e:
            self.log.log_msg("Exception in get_uid_from_server :%s" % str(e))

    def get_server_repository(self, server="primary"):
        try:
            if server == "primary":
                return self.server.get_repository()
            elif server == "secondary":
                rpc_server = 'http://'+self.secondary_server_ip+':'+self.server_port
                server = xmlrpclib.Server(rpc_server)
                return server.get_repository()

        except Exception, e:
            self.log.log_msg("Exception in get_server_repository :%s" % str(e))

    def get_existing_uid_from_server(self):
        pass  # Implement this to get the existing UID in case the client crashes and wants to continue with the same ID
              # Not implementing for now. Have to think about the attack surface it may expose.