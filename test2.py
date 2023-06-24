#!/bin/python
# -*- coding: utf-8 -*-

import sys
import os

from getpass import getpass

import logging

from libsynomail.classes import File
from libsynomail.nas import init_connection,files_path,move_path,get_info,copy_path,rename_path,convert_office

from libsynomail.syneml import read_eml


#read_eml('This.eml')
#read_eml('That.eml')


PASS = getpass()
init_connection('vInd1',PASS)



#files = files_path("/mydrive")
#for file in files:
#    print(file)
#    print('---')
print(get_info("/team-folders/Archive/ctr out 2023/cr_1119.odoc"))

#path = "/mydrive/00 - Admin/Patata.odoc"
#path = "/team-folders/File Sharing/Antonio/Tests/Archive/asr out 2023/cr-asr_0260.odoc"
#print(get_info(path))

#copy_path(path,"/team-folders/File Sharing/Antonio/Tests/Mail asr/Mail to asr/cr-asr_0260.odoc")


#copy_path("/mydrive/Untitled.osheet","/mydrive/00 - Admin/tests/Untitle.osheet")
#rename_path(path,"potato.odoc")
#convert_office("/mydrive/00 - Admin/Patata.docx")

