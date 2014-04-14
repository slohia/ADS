######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : ADSconfig.py
## Description  : Configuration File for Anomaly Detection System
## Author       : Manish Choudhary
## Start Date   : 21 FEB 2014
## Last Revised :
######################################################################################

import os

class ADSConfig:
    def __init__(self):
        self.sys_env = {

        }

        self.env = {
            "ads_log_path"              : "/tmp/ads/log",
            "ads_log_file"              : "ads.log"
        }

        self.usr_env = {
            "LOG_LEVEL"                 : "debug", #info or debug
            #"parameter_types"          : ['cpu', 'memory', 'disk', 'network']
            "parameter_types"           : ['cpu'],
            "anomaly_detection_period"  : 5 #in minutes
        }

        self.xml = {
            "ads_xml_repository"        : "/tmp/ads/xml"
        }

        self.pattern = {

        }