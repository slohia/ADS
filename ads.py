######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : ads.py
## Description  : Main Server Module
## Author       : Manish Choudhary
## Start Date   : 21 FEB 2014
## Last Revised :
######################################################################################

from config.ads_config import ADSConfig
from utils.logger import ADSLog
from utils.xml_util import XMLOperations
from utils.multidict import MultiDict
from lib.rpc_server import RPC
from lib.db import DB
import glob
import os
import time
from multiprocessing import Process


class ADS:
    def __init__(self):
        self.config = ADSConfig()
        self.log = ADSLog(self)
        self.xml = XMLOperations(self)
        self.db = DB(self)
        self.rpc = RPC(self)
        self.xml_repository = self.config.xml['ads_xml_repository']
        self.glob_lookup_arg = self.xml_repository + "/*/*.xml"
        self.parameter_types = self.config.usr_env['parameter_types']
        self.session = self.db.connect_and_generate_db()


    def store_data_in_db(self):
        while True:
            time.sleep(5)
            current_file_name_list = []
            current_param_dict = MultiDict()
            current_file_name_list.extend(glob.glob(self.glob_lookup_arg))
            for current_file_name in current_file_name_list:
                print current_file_name_list
                current_param_dict = self.xml.read_xml(current_file_name)
                #print current_param_dict
                if self.db.update_client_info(self.session, current_param_dict['client']):
                    self.log.log_msg("True from update")
                for each_parameter_type in self.parameter_types:
                    print each_parameter_type
                    self.db.insert_db(self.session, each_parameter_type, current_param_dict['client'], current_param_dict[each_parameter_type])
                #self.db.insert_db(self.session, 'clients', current_param_dict['client'])
                self.db.commit_transaction(self.session)
                os.remove(current_file_name)

    def run(self):
        try:
            storage_process = Process(target=self.store_data_in_db)
            anomaly_detection_process = Process(target=self.run_anomaly_detection)
            rpc_process = Process(target=self.run_rpc)
            rpc_process.start()
            storage_process.start()
            anomaly_detection_process.start()
            rpc_process.join()
            storage_process.join()
            anomaly_detection_process.join()
        except Exception, e:
            self.log.log_msg("Exception in run(): %s" % str(e))

    def run_rpc(self):
        try:
            self.rpc.run_rpc_service()
        except Exception, e:
            self.log.log_msg("Exception in run_rpc(): %s" % str(e))

    def run_anomaly_detection(self):
        try:
            while True:
                self.log.log_msg("Running Anomaly Detection")
                vm_id_list = self.db.fetch_vm_ids_from_db(self.session)
                print vm_id_list
                for vm_id in vm_id_list:
                    for each_parameter_type in self.parameter_types:
                        algorithm_input_list = self.get_data_for_algorithm(vm_id[0], each_parameter_type)
                        print algorithm_input_list
                time.sleep(5)
        except Exception, e:
            self.log.log_msg("Exception in run_anomaly_detection(): %s" % str(e))

    def get_data_for_algorithm(self, vm_id, table_name):
        try:
            return self.db.fetch_db(self.session, vm_id, table_name)
        except Exception, e:
            self.log.log_msg("Exception in get_data_for_algorithm(): %s" % str(e))


if __name__ == "__main__":
    ads = ADS()
    ads.run()