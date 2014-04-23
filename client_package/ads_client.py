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
import calendar
import os
from rpc_client import RPCClient
from ssh import SSH
from logger import ADSLog
from xml_util import XMLOperations
from ads_client_config import ADSClientConfig
from system_monitor import SystemMonitor
from multidict import MultiDict
from machine_address import MachineAddress


class ADSClient:

    def __init__(self):
        self.machine_address = MachineAddress()
        self.config = ADSClientConfig()
        self.log = ADSLog(self)
        self.rpc = RPCClient(self)
        self.ssh = SSH(self)
        self.xml = XMLOperations(self)
        self.sys_mon = SystemMonitor(self)
        self.assigned_uid = ""
        self.remote_path_on_server = ""
        self.server_timeout_period = self.config.usr_env['server_timeout_period']
        self.monitoring_period = self.config.usr_env['monitoring_period']
        self.is_primary_alive = True
        self.has_repo_on_secondary = False
        self.xml_repository = self.config.xml['ads_xml_repository']
        if not os.path.isdir(self.xml_repository):
            os.makedirs(self.xml_repository)

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
            self.log.log_msg("Fetching Page Faults")
            system_dict['memory']['page_faults'] = self.sys_mon.page_faults()
            self.log.log_msg("Fetching Utilization")
            #system_dict['memory']['utilization'] = self.sys_mon.memory_utilization()
            system_dict['memory']['utilization'] = 50
            self.log.log_msg("Fetching write_byte_rate")
            # system_dict['disk']['write_bytes_rate'] = self.sys_mon.write_bytes()
            system_dict['disk']['write_bytes_rate'] = 100
            self.log.log_msg("Fetching read_byte_rate")
            read_bytes_result = self.sys_mon.read_bytes()
            system_dict['disk']['cache_read_bytes_rate'] = read_bytes_result[0]
            system_dict['disk']['buffer_read_bytes_rate'] = read_bytes_result[1]
            self.log.log_msg("Fetching disk utilization")
            system_dict['disk']['utilization'] = self.sys_mon.used_disk_percent()
            self.log.log_msg("Fetching total files")
            # system_dict['disk']['total_files'] = self.sys_mon.total_files()
            system_dict['disk']['total_files'] = 100
            self.log.log_msg("Fetching vm_name")
            system_dict['client']['vm_name'] = socket.gethostname()
            self.log.log_msg("Fetching vm_ip")
            system_dict['client']['vm_ip'] = self.machine_address.get_lan_ip()
            print "VM ID IS: %s" % system_dict['client']['vm_ip']
            self.log.log_msg("Fetching vm_id")
            system_dict['client']['vm_id'] = self.assigned_uid
            return system_dict
        except Exception, e:
            self.log.log_msg("Exception in extract_system_performance_data :%s" % str(e))

    def transfer_to_server(self, remote_path, path_to_xml):
        try:
            print "r: " + remote_path
            print "l: " + path_to_xml
            if self.is_primary_alive:
                remote_ip = self.config.env['primary_server_ip']
                remote_username = self.config.env['primary_server_username']
                remote_password = self.config.env['primary_server_password']
            else:
                remote_ip = self.config.env['secondary_server_ip']
                remote_username = self.config.env['secondary_server_username']
                remote_password = self.config.env['secondary_server_password']
            ssh_client = self.ssh.connect(remote_ip, remote_username, remote_password)
            self.ssh.transfer_file_client_to_ads_server(ssh_client, path_to_xml, remote_path)
            self.ssh.disconnect(ssh_client)
        except Exception, e:
            self.log.log_msg("Exception in transfer_to_server :%s" % str(e))

    def get_ack_stat(self):
        try:
            remote_ip = self.config.env['primary_server_ip']
            remote_username = self.config.env['primary_server_username']
            remote_password = self.config.env['primary_server_password']
            ssh_client = self.ssh.connect(remote_ip, remote_username, remote_password)
            ack_stat = self.ssh.get_ack_stat_from_server(ssh_client, self.remote_path_on_server+'/ack')
            self.ssh.disconnect(ssh_client)
            return ack_stat
        except Exception,e:
            self.log.log_msg("Exception in get_acks_from_server :%s" % str(e))

    def is_primary_server_alive(self):
        try:
            ack_stat = self.get_ack_stat()
            if ack_stat:
                current_time = calendar.timegm(time.gmtime())
                if current_time - ack_stat.st_mtime > self.monitoring_period * self.server_timeout_period:
                    self.log.log_msg("Primary server is not alive.")
                    self.is_primary_alive = False
            else:
                self.log.log_msg("Primary server is not alive.")
                self.is_primary_alive = False

        except Exception, e:
            self.log.log_msg("Exception in is_primary_server_alive :%s" % str(e))
            return True

    def client_controller(self):
        try:
            self.assigned_uid = self.rpc.get_uid_from_server()
            self.remote_path_on_server = self.rpc.get_server_repository(self.assigned_uid)
            print "assigned Id:" + self.assigned_uid
            print "remote path", self.remote_path_on_server
            while True:
                self.is_primary_server_alive()
                if not self.is_primary_alive:
                    if not self.has_repo_on_secondary:
                        self.remote_path_on_server = self.rpc.get_server_repository(self.assigned_uid, "secondary")
                        self.has_repo_on_secondary = True
                system_dict = self.extract_system_performance_data()
                print system_dict
                path_to_xml = self.xml.write_xml(system_dict)
                print path_to_xml
                self.transfer_to_server(self.remote_path_on_server, path_to_xml)
                os.remove(path_to_xml)
                time.sleep(self.monitoring_period)
        except Exception, e:
            self.log.log_msg("Exception in client_controller :%s" % str(e))

if __name__ == "__main__":
    ads_client = ADSClient()
    print ads_client.client_controller()