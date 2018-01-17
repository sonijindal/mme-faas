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
import grequests
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

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

try:
    #conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, port=3306, connect_timeout=5)
    print("Before connect call")
    db_connect_start = time.time()
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, port=3306)
    print("DB connection took %s seconds" % (time.time() - db_connect_start))
    print("After connect call")
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
    #id = random.randint(0,100000)
    
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

def get_async_web_response(url, method='GET', params=None, headers=None, encode=False, verify=None, use_verify=False, callback=None):
    import grequests
    # make a string with the request type in it:
    response = None
    request = None
    try:
        if 'POST' == method:
            if use_verify:
                request = grequests.post(url, data=params, headers=headers, verify=verify, callback=callback)
            else:
                request = grequests.post(url, data=params, headers=headers, callback=callback)
        else:
            request = requests.get(url, data=params, headers=headers, callback=callback)

        if request:
            response = grequests.send(request, grequests.Pool(1))
            return response
        else:
            return response
    except:
        return response

def handle(event):
    """
    This function fetches content from mysql RDS instance
    """
    print("Hello! You said: " + event)
    func_start = time.time()
    item_count = 0
    logger.info(event)
    body = json.loads(event)
    #logger.info(body)
    print(body['UeId'])
    #count = select_with_key(event['ue_id'])
    #if count != 0:
    #    print("Count:",count)
    #    return "One Accept already in progress!"
    #else:
    checkpoint = time.time()
    mme_s1ap_ue_id = generate_mme_s1ap_ue_id()
    print("Generated ue IDs, %s seconds" % (time.time() - checkpoint))
    print(mme_s1ap_ue_id)
    
    eps_bearer_id = generate_eps_bearer_id()
    print(eps_bearer_id)
    apn = get_apn_from_hss()
    print(apn)
    pgw_ip = get_pgw_from_apn()
    print(pgw_ip)
    ue_state = "1"
    
    checkpoint = time.time()
    insert(body['UeId'],body['UeIdType'], body['EnbUeS1apId'], body['Ecgi'], body['UeCap'], mme_s1ap_ue_id,\
        eps_bearer_id, apn, pgw_ip, ue_state)
    print("record inserted!")
    print("Inserted entry, %s seconds" % (time.time() - checkpoint))
        
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
    '''
    lambda_client = boto3.client('lambda')
    try:
        invoke_response = lambda_client.invoke(
            FunctionName='create_session_req',
            InvocationType='Event',
            Payload=json.dumps(payload))
    except Exception as e:
        print(e)
        raise e
    '''
    
    checkpoint = time.time()
    gateway = "128.110.153.209"
    url = "http://"+gateway+":8080/function/create_session_req"
    headers = {
      'content-type': "application/json" 
    }
    get_async_web_response(url, 'POST', params=json.dumps(payload), headers=headers)
    #invoke_response = requests.post(url,headers=headers,data=json.dumps(payload))
    print("Sent request to create_session_req, %s seconds" % (time.time() - checkpoint))
    print("Function execution took %s seconds" % (time.time() - func_start))
 
    print(invoke_response)
    
    return "ADDED"

