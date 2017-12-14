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
import boto3
import json
import urllib
import random

rds_host  = rds_config.rds_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except Exception as e:
    logger.error(e)
    logger.error(e.args)
    sys.exit()
except: 
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def select_with_key(ue_id):
    logger.info("Checking for key:")
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT * from ue_info where ue_id=%s;", (ue_id))
        except Exception as e:
            logger.error(e)
            logger.error(e.args)
            sys.exit()
    return cur.rowcount

def insert(ue_id, ue_id_type, enb_ue_s1ap_id, ecgi, ue_cap, mme_s1ap_ue_id, eps_bearer_id, apn, pgw_ip, ue_state):
    logger.info("Inserting key:")
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO ue_info (ue_id, ue_id_type, enb_ue_s1ap_id, ecgi, ue_cap, mme_s1ap_ue_id, eps_bearer_id, apn, pgw_ip, ue_state) "\
            "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",\
            (ue_id, ue_id_type, enb_ue_s1ap_id, ecgi, ue_cap, mme_s1ap_ue_id, eps_bearer_id, apn, pgw_ip, ue_state))
            conn.commit()
        except Exception as e:
            logger.error(e)
            logger.error(e.args)
            sys.exit()

def generate_mme_s1ap_ue_id():
    while True:
        id = random.randint(0,100000)
        with conn.cursor() as cur:
            logger.info("Inserting table")
    
            try:
                cur.execute("INSERT INTO mme_ue_ids (mme_s1ap_ue_id)" \
                    "VALUES ( %s);",(str(id)))
                conn.commit()
                break
            except Exception as e:
                logger.error(e)
                logger.error(e.args)
                continue
    
    return id

def generate_eps_bearer_id():
    return "5"

def get_apn_from_hss():
    return "XYZ"
    
def get_pgw_from_apn():
    return "128.100.3.4"

def handler(event, context):
    """
    This function fetches content from mysql RDS instance
    """
    item_count = 0
    logger.info(event)
    body = json.loads(event['body'])
    logger.info(body)
    logger.info(body['UeId'])
    #count = select_with_key(event['ue_id'])
    #if count != 0:
    #    print("Count:",count)
    #    return "One Accept already in progress!"
    #else:
    
    mme_s1ap_ue_id = generate_mme_s1ap_ue_id()
    print(mme_s1ap_ue_id)
    
    eps_bearer_id = generate_eps_bearer_id()
    print(eps_bearer_id)
    apn = get_apn_from_hss()
    print(apn)
    pgw_ip = get_pgw_from_apn()
    print(pgw_ip)
    ue_state = "1"
    
    insert(body['UeId'],body['UeIdType'], body['EnbUeS1apId'], body['Ecgi'], body['UeCap'], mme_s1ap_ue_id,\
        eps_bearer_id, apn, pgw_ip, ue_state)
    print("record inserted!")
    
    payload={}
    payload['ue_id'] = body['UeId']
    payload['ue_id_type']= body['UeIdType']
    payload['enb_ue_s1ap_id']= body['EnbUeS1apId']
    payload['ecgi']= body['Ecgi']
    payload['ue_cap']= body['UeCap']
    payload['mme_s1ap_ue_id']= mme_s1ap_ue_id
    payload['eps_bearer_id']= eps_bearer_id
    payload['apn']= apn
    payload['pgw_ip']= pgw_ip
    payload['ue_state']=ue_state
    payload['ue_resp_ip']=body['UeRespIp']
    payload['sgw_req_ip']=body['SgwReqIp']
    lambda_client = boto3.client('lambda')
    try:
        invoke_response = lambda_client.invoke(
            FunctionName='create_session_req',
            InvocationType='Event',
            Payload=json.dumps(payload))
    except Exception as e:
        print(e)
        raise e
    
    print(invoke_response)
    
    return "ADDED"

