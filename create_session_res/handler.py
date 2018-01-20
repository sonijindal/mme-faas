'''
Copyright (c) 2017 Sonika Jindal

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
'''

import sys
import logging
import config
import pymysql
import requests
import json
import urllib
import time

rds_host  = config.rds_host
name = config.db_username
password = config.db_password
db_name = config.db_name

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except Exception as e:
    LOGGER.error(e)
    LOGGER.error(e.args)
    sys.exit()
except: 
    LOGGER.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

LOGGER.info("SUCCESS: Connection to RDS mysql instance succeeded")

def handle(event):
    LOGGER.info('CREATE SESSION RESPONSE function')
    LOGGER.info(event)
    item_count = 0
    parsed = event.split("&")
    ue_id=parsed[0].split("=")[1]
    ue_id_type=parsed[1].split("=")[1]
    ue_resp_ip=parsed[2].split("=")[1]
    with conn.cursor() as cur:
        LOGGER.info("Updating table")
        LOGGER.info(event)
        try:
            cur.execute("UPDATE ue_info SET s1_sgw_teid='2345', s5_pgw_teid='6789' where ue_id=%s;",(ue_id))
            conn.commit()
        except Exception as e:
            LOGGER.error(e)
            LOGGER.error(e.args)
            sys.exit()
    payload={}
    payload['ue_id']=int(ue_id)
    payload['ue_id_type']=ue_id_type
    payload['ue_resp_ip']=ue_resp_ip

    url = "http://"+config.gateway+":8080/function/attach_accept"
    headers = {
      'content-type': "application/json" 
    }
    invoke_response = requests.post(url,headers=headers,data=json.dumps(payload))
 
    LOGGER.info(invoke_response)
    
    return "create_session_req"
