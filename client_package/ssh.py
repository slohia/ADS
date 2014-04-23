######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : ssh.py
## Description  : module to provide SSH functionality for command execution and file transfer
## Author       : Manish Choudhary
## Start Date   : 10 MAR 2014
## Last Revised :
######################################################################################

import paramiko


class SSH:

    def __init__(self, ads):
        self.log = ads.log

    def connect(self, remote_ip, remote_username, remote_password):
        try:
            self.log.log_msg("\n")
            self.log.log_msg("SSH Connection Request with following parameters:")
            self.log.log_msg("remote_ip:%s" % remote_ip)
            self.log.log_msg("remote_username:%s" % remote_username)
            self.log.log_msg("remote_password:%s" % remote_password)
            self.log.log_msg("Processing SSH Connection Request..")
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.log.log_msg("Establishing SSH Connection..")
            ssh_client.connect(remote_ip, username=remote_username, password=remote_password)
            self.log.log_msg("CONNECTED Successfully")
            return ssh_client
        except Exception, e:
            self.log.log_msg("Exception while establishing SSH connection:%s" % str(e))

    def execute(self, ssh_client, commands):
        execution_results = []
        commands_to_execute = []
        if not ssh_client:
            self.log.log_msg("No Valid SSH Client Handle")
            return
        try:
            self.log.log_msg("\n")
            self.log.log_msg("Remote Command Execution Request")
            commands_to_execute.extend(commands)
            for command in commands_to_execute:
                self.log.log_msg("Executing Command: %s" % command)
                stderr, stdout, stdin = ssh_client.exec_command(command)
                self.log.log_msg("Execution Result:")
                execution_results.append(stdout.read())
                for line in execution_results[-1].splitlines():
                    self.log.log_msg(line)
            return execution_results
        except Exception,e:
            self.log.log_msg("Exception while executing remote command:%s" %str(e))
            return False

    def disconnect(self, ssh_client):
        if not ssh_client:
            self.log.log_msg("No Valid SSH Client Handle")
            return False
        try:
            self.log.log_msg("\n")
            self.log.log_msg("SSH Disconnection Request")
            self.log.log_msg("Disconnecting..")
            ssh_client.close()
            self.log.log_msg("DISCONNECTED")
            return True
        except Exception, e:
            self.log.log_msg("Exception while terminating the SSH Connection" % str(e))
            return False

    def transfer_file_client_to_ads_server(self, ssh_client, local_path, remote_path):
        try:
            self.log.log_msg("transfer_file_client_to_ads_server Request")
            sftp = ssh_client.open_sftp()
            remote_path = remote_path + "/" + local_path.split('/')[-1]
            self.log.log_msg("Transferring file from '"+str(local_path)+"' to '"+str(remote_path) + "'")
            sftp.put(local_path, remote_path)
            self.log.log_msg("File Transferred Successfully")
            sftp.close()
            return True
        except Exception,e:
            self.log.log_msg("Exception while transferring the file" % str(e))
            return False

    def transfer_file_ads_server_to_client(self, ssh_client, remote_path, local_path):
        try:
            self.log.log_msg("transfer_file_ads_server_to_client Request")
            sftp = ssh_client.open_sftp()
            self.log.log_msg("Transferring file from '"+str(remote_path)+"' to '"+str(local_path)+"'")
            sftp.get(remote_path, local_path)
            self.log.log_msg("File Transferred Successfully")
            sftp.close()
            return True
        except Exception,e:
            self.log.log_msg("Exception while transferring the file" % str(e))
            return False

    def get_ack_stat_from_server(self, ssh_client, remote_path):
        try:
            self.log.log_msg("get_ack_stat_from_server Request")
            sftp = ssh_client.open_sftp()
            self.log.log_msg("Getting stat from the remote server for: " + str(remote_path))
            file_stat = sftp.stat(remote_path)
            self.log.log_msg("Stat Received Successfully.")
            sftp.close()
            return file_stat
        except Exception, e:
            self.log.log_msg("Exception while getting stat of the file" % str(e))
            return False
