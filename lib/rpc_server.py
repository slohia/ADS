######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : rpc_server.py
## Description  : module to provide server side rpc functionality to make the interfaces available to clients
## Author       : Manish Choudhary
## Start Date   : 20 MAR 2014
## Last Revised :
######################################################################################

from lib.db import DB
from utils.logger import ADSLog
import socket
import SimpleXMLRPCServer
import datetime
import random
import hashlib
import os
from utils.multidict import MultiDict
from SOM.som import SOM

class ClientFunctions:

    def __init__(self, ads):
        self.log = ads.log
        self.db = ads.db
        self.config = ads.config
        self.available_client_repo = 0

    def _private_function(self):
        pass

    def store_new_client_info(self, client_dict):
        self.log.log_msg("Storing the new client info in DB under clients table.")
        session = self.db.connect_db()
        self.db.insert_db(session, 'clients', client_dict)
        self.db.commit_transaction(session)
        self.db.disconnect_db(session)

    def get_uid(self, client_hostname, client_ip_address):
        client_dict = MultiDict()
        client_dict['vm_ip'] = client_ip_address
        client_dict['vm_name'] = client_hostname
        self.log.log_msg("Request to generate UID from client with hostname %s and IP %s" %(client_dict['vm_name'], client_dict['vm_ip']))
        current_time = datetime.datetime.utcnow()
        random_number = long(random.random()*100000000000000000L)
        raw_data_for_id = str(current_time)+' '+str(random_number)+' '+str(client_ip_address)+' '+str(client_hostname)
        client_dict['vm_id'] = hashlib.sha256(raw_data_for_id).hexdigest()
        client_dict['primary_server'] = '0.0.0.0'
        self.log.log_msg("Assigning UID: %s " % client_dict['vm_id'])
        self.store_new_client_info(client_dict)
        return str(client_dict['vm_id'])

    def get_server_repository(self, client_id):
        self.log.log_msg("Request to create server repository...")
        xml_repository = self.config.xml['ads_xml_repository']
        self.available_client_repo += 1
        new_repo_for_client = xml_repository + '/client_repo_' + str(self.available_client_repo)
        if not os.path.exists(new_repo_for_client):
            os.makedirs(new_repo_for_client)
        self.log.log_msg("Created server repository SUCCESSFULLY! " + new_repo_for_client)

        self.log.log_msg("Creating learning process for client")
        cpu_process = SOM(client_id, 'cpu', 32, 32, 3, 0.05, 100)
        cpu_process.start()
        memory_process = SOM(client_id, 'memory', 32, 32, 2, 0.05, 100)
        memory_process.start()
        network_process = SOM(client_id, 'network', 32, 32, 4, 0.05, 100)
        network_process.start()
        disk_process = SOM(client_id, 'disk', 32, 32, 5, 0.05, 100)
        disk_process.start()

        return new_repo_for_client


class RPC:

    def __init__(self, ads):
        self.log = ads.log
        self.db = ads.db
        self.config = ads.config

    def run_rpc_service(self):
        self.log.log_msg("Starting RPC service @ 10.0.0.61:8006")
        server = SimpleXMLRPCServer.SimpleXMLRPCServer(("10.0.0.61", 8006))
        server.register_instance(ClientFunctions(self))
        server.serve_forever()

#if __name__ == "__main__":
#    rpc_server = ClientFunctions()
#    print rpc_server.run_rpc_service()