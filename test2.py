#!/bin/python
# -*- coding: utf-8 -*-

import sys
import os

from getpass import getpass

import logging

from libsynomail.classes import File
from libsynomail.nas import init_connection,files_path,move_path,get_info,copy_path,rename_path,convert_office, create_task, create_folder, get_teams

from libsynomail.syneml import read_eml


#read_eml('This.eml')
#read_eml('bdu.eml')

#{'access_time': 1688993051, 'adv_shared': False, 'app_properties': {'type': 'none'}, 'capabilities': {'can_comment': True, 'can_delete': True, 'can_encrypt': True, 'can_organize': True, 'can_preview': True, 'can_read': True, 'can_rename': True, 'can_share': True, 'can_write': True}, 'change_id': 13483, 'change_time': 1688993051, 'content_snippet': '', 'content_type': 'document', 'created_time': 1681963384, 'display_path': '/mydrive/Pendings.osheet', 'dsm_path': '', 'encrypted': False, 'file_id': '747817950530027435', 'hash': '21fb5ca82721c55195603c7cf780921d', 'image_metadata': {'time': 1688993050}, 'labels': [], 'max_id': 13483, 'modified_time': 1688993050, 'name': 'Pendings.osheet', 'owner': {'display_name': 'vInd1', 'name': 'vInd1', 'nickname': 'Antonio - Aes', 'uid': 1102}, 'parent_id': '731171064029159427', 'path': '/Pendings.osheet', 'permanent_link': 'tF0sNfozL0zh3biNgh4KPhDvQI7VtXDf', 'properties': {'object_id': '1102_VPU81NIVRH04PEB79P9D2DFSRK.sh'}, 'removed': False, 'revisions': 8, 'shared': False, 'shared_with': [], 'size': 5441, 'starred': True, 'support_remote': False, 'sync_id': 13483, 'sync_to_device': False, 'type': 'file', 'version_id': '13483'}


PASS = getpass()
init_connection('despacho',PASS)

#path = 'team-folders/Data/Mail/IN/asr 1.odoc'
#dest = 'team-folders/Data/Notes/2024/asr in/asr_0001'

#files = files_path("/team-folders/")
files = get_teams()
print(files)
for file in files:
    if file and file[0].isdigit():
        #print(file)
        create_folder(f'/team-folders/{file}',file)

#move_path(path,dest)
#print(get_info(path))



#create_task("/vInd1/home_todo/",'La primera tarea en el chat')

#convert_office("/team-folders/Despacho/Originals/Pl_0064.rtf")
#convert_office(str(761775199073909955))

#files = files_path("/team-folders/Despacho")
#print(files)
#files = files_path("/mydrive")
#files = files_path('https://nas.prome.sg:5001/d/f/spHGLiAf3Ja99mP4PPmqYdEoz4fwS80A')
#for file in files:
#    print(file)
#    print('---')

#print(get_info("/team-folders/Archive/r out 2023/Aes-r_2065.odoc"))

#path = "/mydrive/00 - Admin/Patata.odoc"
#id_file = "771757611870630345"
#path = "/team-folders/Despacho/ToSend/Done/Patata.odoc"
#path = "1102_HA5TUQ2FHD5O52D8ECLN0BKTVC.doc"
#path = "771758824448111599"

#print(get_info(path))
#print(get_info(id_file))

#copy_path(path,"/team-folders/File Sharing/Antonio/Tests/Mail asr/Mail to asr/cr-asr_0260.odoc")


#copy_path("/mydrive/Untitled.osheet","/mydrive/00 - Admin/tests/Untitle.osheet")
#rename_path(path,"potato.odoc")
#convert_office("/mydrive/00 - Admin/Patata.docx")

