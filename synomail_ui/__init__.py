#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from appdirs import user_config_dir
import json

_ROOT = os.path.abspath(os.path.dirname(__file__))
#path_config = user_config_dir('synomail','prome')
path_config = "/".join(_ROOT.split("/")[:-1])
path_config += "/config"

if not os.path.exists(path_config):
    os.mkdir(path_config)
    #Here I should create the file

with open(f"{path_config}/config.json","r") as f:
    CONFIG = json.load(f)

with open(f"{path_config}/ctrs.json","r") as f:
    CONFIG |= json.load(f)

with open(f"{path_config}/deps.json","r") as f:
    CONFIG |= json.load(f)

with open(f"{path_config}/forti_mail.json","r") as f:
    CONFIG |= json.load(f)
