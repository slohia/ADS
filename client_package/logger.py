######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : logger.py
## Description  : program to provide the ADS content log functions
## Author       : Manish Choudhary
## Start Date   : 21 FEB 2014
## Last Revised :
######################################################################################

import time
import os


class ADSLog:
    def __init__(self, ads):
        self.config = ads.config
        self.ads_log_path = self.config.env["ads_log_path"]
        self.ads_log = self.ads_log_path + "/" + self.config.env["ads_log_file"]
        self.ads_log_level = self.config.usr_env["LOG_LEVEL"]
        if not os.path.isdir(self.ads_log_path):
            os.makedirs(self.ads_log_path)

    def debug_logger(self, msg):
        print msg
        ads_log_fh = open(self.ads_log, 'a+')
        ads_log_fh.write(time.strftime("%Y-%m-%d %H:%M:%S") + " :: " + msg + "\n")		# Locale neutral date format!
        ads_log_fh.close()

    def info_logger(self, msg):
        ads_log_fh = open(self.ads_log, 'a+')
        ads_log_fh.write(time.strftime("%Y-%m-%d %H:%M:%S") + " :: " + msg + "\n")		# Locale neutral date format!
        ads_log_fh.cose()

    def client_logger(self, msg):
        pass

    def log_msg(self, msg):
        if self.ads_log_level == 'info':
            self.info_logger(msg)
        if self.ads_log_level == 'debug':
            self.debug_logger(msg)
        if self.ads_log_level == 'client':
            self.client__logger(msg)
        return True