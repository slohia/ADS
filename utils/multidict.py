######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : logger.py
## Description  : program to  create a custom dictionary to store multi level dictionary
## Author       : Manish Choudhary
## Start Date   : 21 FEB 2014
## Last Revised :
######################################################################################


class MultiDict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value