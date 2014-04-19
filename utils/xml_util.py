######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : xml_util.py
## Description  : module to facilitate xml read and write operations
## Author       : Manish Choudhary
## Start Date   : 10 MAR 2014
## Last Revised :
######################################################################################

import xml.etree.ElementTree as xmlTree
from multidict import MultiDict


class XMLOperations:

    def __init__(self, ads):
        self.config = ads.config
        self.log = ads.log

    def read_xml(self, xml_file):
        try:
            self.log.log_msg("Reading from the xml: %s" % str(xml_file))
            param_dict = MultiDict()
            tree = xmlTree.parse(str(xml_file))
            print tree.find('parameters')
            root = tree.getroot()
            # print root
            param_dict['client']['vm_ip'] = root.attrib['ip']
            param_dict['client']['vm_name'] = root.attrib['name']
            param_dict['client']['vm_id'] = root.attrib['id']
            for child in root:
                print child
                for sub_child in child:
                    print sub_child
                    param_dict[child.tag][sub_child.tag] = sub_child.text
            self.log.log_msg("Successfully Read from the xml: %s" % str(xml_file))
            return param_dict
        except Exception, e:
            self.log.log_msg("Exception in reading the xml: %s" % str(e))

    def write_xml(self, param_dict):
        try:
            self.log.log_msg("Generating XML")
            root = xmlTree.Element("parameters")
            for key, value in param_dict.items():
                child = xmlTree.SubElement(root, str(key))
                for sub_key, sub_value in value.items():
                    sub_child = xmlTree.SubElement(child, str(sub_key))
                    sub_child.text = str(sub_value)
            tree = xmlTree(root)
            tree.write("params_uid.xml")
            self.log.log_msg("XML Generation Completed Successfully")
        except Exception, e:
            self.log.log_msg("Exception in generating the xml: %s" % str(e))