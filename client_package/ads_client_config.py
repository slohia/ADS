######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : ADSconfig.py
## Description  : Configuration File for Anomaly Detection System
## Author       : Manish Choudhary
## Start Date   : 21 FEB 2014
## Last Revised :
######################################################################################

import os


class ADSClientConfig:
    def __init__(self):
        self.sys_env = {

        }

        self.env = {
            "ads_log_path"              : "/tmp/ads/log",
            "ads_log_file"              : "ads.log",
            "primary_server_ip"         : "127.0.0.1",
            "secondary_server_ip"       : "0.0.0.0",
            "server_port"               : "8001",
            "server_username"           : "manish",
            "server_password"           : "passw0rd!"
        }

        self.usr_env = {
            "LOG_LEVEL"                 : "debug", #info/debug/client
            "server_timeout_period"     : 3, #number of missing acknowledgement
            "monitoring_period"         : 30 #in seconds
        }

        self.xml = {
            "ads_xml_repository"        : "/tmp/ads/xml"
        }

        self.pattern = {

        }