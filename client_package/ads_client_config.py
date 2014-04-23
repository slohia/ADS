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
            "ads_log_path"                          :   "/home/slohia/ads/log",
            "ads_log_file"                          :   "ads.log",
            "primary_server_ip"                     :   "143.215.204.205",
            "secondary_server_ip"                   :   "143.215.206.121",
            "server_port"                           :   "8006",
            "primary_server_username"               :   "slohia",
            "primary_server_password"               :   "1",
            "secondary_server_username"             :   "slohia",
            "secondary_server_password"             :   "1"
        }

        self.usr_env = {
            "LOG_LEVEL"                 : "debug", #info/debug/client
            "server_timeout_period"     : 10, #number of missing acknowledgement
            "monitoring_period"         : 5 #in seconds
        }

        self.xml = {
            "ads_xml_repository"        : "/home/slohia/ads/xml"
        }

        self.pattern = {

        }