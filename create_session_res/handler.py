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
import rds_config
import pymysql
import requests
#import boto3
import json
import urllib
import time

rds_host  = "128.110.153.209"
name = "root"
password = "root123"
db_name = "mme_ue_db"

'''
rds_host  = rds_config.rds_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
'''

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
    """
    This function fetches content from mysql RDS instance
    """
    item_count = 0
    print(event) 
    #data = event['body']
    data = event
    LOGGER.info(data)
    parsed = data.split("&")
    LOGGER.info(parsed)
    ue_id=parsed[0].split("=")[1]
    ue_id_type=parsed[1].split("=")[1]
    ue_resp_ip=parsed[2].split("=")[1]
    LOGGER.info("UE ID value:")
    LOGGER.info(ue_id)
    LOGGER.info(ue_id_type)
    LOGGER.info(ue_resp_ip)
    
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
    '''
    lambda_client = boto3.client('lambda')
    try:
        invoke_response = lambda_client.invoke(
            FunctionName='attach_accept',
            InvocationType='Event',
            Payload=json.dumps(payload))
        LOGGER.info(invoke_response)
    except Exception as e:
        LOGGER.info(e)
        raise e
    '''
    gateway = "128.110.153.209"
    url = "http://"+gateway+":8080/function/attach_accept"
    headers = {
      'content-type': "application/json" 
    }
    invoke_response = requests.post(url,headers=headers,data=json.dumps(payload))
 
    LOGGER.info(invoke_response)
    
    return "create_session_req"
