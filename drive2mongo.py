# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import sys
from bottle import get, route, run, template
import re
import datetime
from datetime import date
from bottle import response

import logging
logger = logging.getLogger()

import os
import pymongo
import gridfs
import pytz
from bson.codec_options import CodecOptions

TZ=pytz.timezone("Asia/Taipei")

MONGODB_URI=os.environ["MONGODB_URI"]
client = pymongo.MongoClient(MONGODB_URI)
collection_gdimage = client["khcc"]["gdimages"].with_options(codec_options=CodecOptions(tz_aware=True,tzinfo=TZ))

# -s writer      981.67KB     19eiu77nNmtZzXjj7LOXkqkUx9V6YZbEAew     2017-04-11 05:17:15 +0000 UTC   /基本需求研究院/全民修屋第一期/照片/建業/P_20170411_104454.jpg

def parse_drive_list(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        for l in lines:
            line = l.split("\t")

            drive_id = line[1]

            fullpath = line[-1]


            if "建業" in fullpath:
                location = "ZY"
            else:
                location = "FS"
            
            pathname = os.path.split(fullpath)[0]
            filename = os.path.split(fullpath)[1].strip()

            address = pathname.split("/")[-1]


            record = {
                    "driver_id":drive_id,
                    "location":location,
                    "address":address}

            print(record)
            
            collection_gdimage.insert(record)

parse_drive_list("/home/test/tmp/gdlist.txt")
