######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : ads_client.py
## Description  : module to provide client controller functionality
## Author       : Manish Choudhary
## Start Date   : 02 APR 2014
## Last Revised :
######################################################################################

import socket
import time
from rpc_client import RPCClient
from ssh import SSH
from logger import ADSLog
from xml_util import XMLOperations
from ads_client_config import ADSClientConfig
from system_monitor import SystemMonitor
from multidict import MultiDict


class ADSClient:

    def __init__(self):
        self.config = ADSClientConfig()
        self.log = ADSLog(self)
        self.rpc = RPCClient(self)
        self.ssh = SSH(self)
        self.xml = XMLOperations(self)
        self.sys_mon = SystemMonitor(self)
        self.assigned_uid = ""
        self.remote_path_on_server = ""

    def extract_system_performance_data(self):
        try:
            self.log.log_msg("In extract_system_performance_data")
            system_dict = MultiDict()
            self.log.log_msg("fetching processes")
            system_dict['cpu']['processes'] = self.sys_mon.number_of_processes()
            self.log.log_msg("fetching system_time")
            system_dict['cpu']['system_time'] = self.sys_mon.system_time()
            self.log.log_msg("fetching user_time")
            system_dict['cpu']['user_time'] = self.sys_mon.user_time()
            #self.log.log_msg("Fetching Utilization")
            #system_dict['memory']['utilization'] = self.sys_mon.memory_utilization()
            self.log.log_msg("Fetching Page Faults")
            system_dict['memory']['page_faults'] = self.sys_mon.page_faults()
            self.log.log_msg("Fetching write_byte_rate")
            system_dict['disk']['write_bytes_rate'] = self.sys_mon.write_bytes()
            self.log.log_msg("Fetching read_byte_rate")
            read_bytes_result = self.sys_mon.read_bytes()
            system_dict['disk']['cache_read_bytes_rate'] = read_bytes_result[0]
            system_dict['disk']['buffer_read_bytes_rate'] = read_bytes_result[1]
            self.log.log_msg("Fetching disk utilization")
            system_dict['disk']['utilization'] = self.sys_mon.used_disk_percent()
            self.log.log_msg("Fetching total files")
            system_dict['disk']['total_files'] = self.sys_mon.total_files()
            self.log.log_msg("Fetching vm_name")
            system_dict['client']['vm_name'] = socket.gethostname()
            self.log.log_msg("Fetching vm_ip")
            system_dict['client']['vm_ip'] = socket.gethostbyname(socket.gethostname())
            self.log.log_msg("Fetching vm_id")
            system_dict['client']['vm_id'] = self.assigned_uid
            return system_dict
        except Exception, e:
            self.log.log_msg("Exception in extract_system_performance_data :%s" % str(e))

    def transfer_to_server(self, remote_path, path_to_xml):
        try:
            print "r: " + remote_path
            print "l: " + path_to_xml
            remote_ip = self.config.env['primary_server_ip']
            remote_username = self.config.env['server_username']
            remote_password = self.config.env['server_password']
            ssh_client = self.ssh.connect(remote_ip, remote_username, remote_password)
            self.ssh.transfer_file_client_to_ads_server(ssh_client, path_to_xml, remote_path)
        except Exception, e:
            self.log.log_msg("Exception in transfer_to_server :%s" % str(e))

    def client_controller(self):
        try:
            self.assigned_uid = self.rpc.get_existing_uid_from_server()
            #self.assigned_uid = "1"
            self.remote_path_on_server = self.rpc.get_server_repository(self.assigned_uid)
            print "assigned Id:" + self.assigned_uid
            print "remote path" + self.remote_path_on_server
            #self.remote_path_on_server = "/tmp/"
            while True:
                system_dict = self.extract_system_performance_data()
                print system_dict
                path_to_xml = self.xml.write_xml(system_dict)
                print path_to_xml
                #self.transfer_to_server(self.remote_path_on_server, path_to_xml)
                time.sleep(self.config.usr_env['monitoring_period'])
        except Exception, e:
            self.log.log_msg("Exception in client_controller :%s" % str(e))

if __name__ == "__main__":
    ads_client = ADSClient()
    print ads_client.client_controller()