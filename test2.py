#!/bin/python
# -*- coding: utf-8 -*-

import sys
import os

from getpass import getpass

import logging

from libsynomail.classes import File
from libsynomail.nas import init_connection,files_path,move_path,get_info,copy_path,rename_path,convert_office, create_task

from libsynomail.syneml import read_eml


#read_eml('This.eml')
read_eml('Aes_32.eml')


#PASS = getpass()
#init_connection('vInd1',PASS)

#create_task("/vInd1/home_todo/",'La primera tarea en el chat')

#convert_office("/team-folders/Despacho/Originals/Pl_0064.rtf")
#convert_office(str(761775199073909955))


#files = files_path("/mydrive")
#for file in files:
#    print(file)
#    print('---')
#print(get_info("/team-folders/Archive/ctr out 2023/cr_1119.odoc"))

#path = "/mydrive/00 - Admin/Patata.odoc"
#path = "/team-folders/File Sharing/Antonio/Tests/Archive/asr out 2023/cr-asr_0260.odoc"
#print(get_info(path))

#copy_path(path,"/team-folders/File Sharing/Antonio/Tests/Mail asr/Mail to asr/cr-asr_0260.odoc")


#copy_path("/mydrive/Untitled.osheet","/mydrive/00 - Admin/tests/Untitle.osheet")
#rename_path(path,"potato.odoc")
#convert_office("/mydrive/00 - Admin/Patata.docx")

