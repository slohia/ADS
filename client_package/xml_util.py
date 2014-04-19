######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : xml_util.py
## Description  : module to facilitate xml read and write operations
## Author       : Manish Choudhary
## Start Date   : 10 MAR 2014
## Last Revised :
######################################################################################

import xml.etree.ElementTree as ET
from multidict import MultiDict
import time
import calendar


class XMLOperations:

    def __init__(self, ads):
        self.config = ads.config
        self.log = ads.log

    def read_xml(self, xml_file):
        try:
            self.log.log_msg("Reading from the xml: %s" % str(xml_file))
            param_dict = MultiDict()
            tree = xmlTree.parse(str(xml_file))
            root = tree.getroot()
            param_dict['client']['vm_ip'] = root.attrib['ip']
            param_dict['client']['vm_name'] = root.attrib['name']
            param_dict['client']['vm_id'] = root.attrib['id']
            for child in root:
                for sub_child in child:
                    param_dict[child.tag][sub_child.tag] = sub_child.text
            self.log.log_msg("Successfully Read from the xml: %s" % str(xml_file))
            return param_dict
        except Exception, e:
            self.log.log_msg("Exception in reading the xml: %s" % str(e))

    def write_xml(self, param_dict):
        try:
            xml_file_name = str(calendar.timegm(time.gmtime()))+".xml"
            print xml_file_name
            path_to_xml = self.config.xml['ads_xml_repository'] + '/' + xml_file_name
            self.log.log_msg("Generating XML")
            print path_to_xml
            tree_root = ET.Element("parameters")
            tree_root.set('ip', param_dict['client']['vm_ip'])
            tree_root.set('id', param_dict['client']['vm_id'])
            tree_root.set('name', param_dict['client']['vm_name'])
            del param_dict['client']
            for key, value in param_dict.items():
                child = ET.SubElement(tree_root, str(key))
                print child
                for sub_key, sub_value in value.items():
                    print sub_key
                    print sub_value
                    sub_child = ET.SubElement(child, str(sub_key))
                    sub_child.text = str(sub_value)
            complete_tree = ET.ElementTree(tree_root)
            print complete_tree
            file_handle = open(path_to_xml, "w")
            complete_tree.write(file_handle, encoding='utf-8', xml_declaration=True, method="xml")
            file_handle.close()
            self.log.log_msg("XML Generation Completed Successfully")
            return path_to_xml
        except Exception, e:
            self.log.log_msg("Exception in generating the xml: %s" % str(e))