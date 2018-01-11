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

import logging
import json
import requests

# This function sends the create session request to SGW

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

def handle(event):
    LOGGER.info("Inside create session req")
    LOGGER.info(event)
    print("Inside create session req")
    print(event)
    event = json.loads(event)    
    eve={"Message":"create_session_req", "UeId":event['ue_id'], "UeIdType":event['ue_id_type'], "UeRespIp":event['ue_resp_ip']}
    payload=json.dumps(eve)
    url = "http://"+event['sgw_req_ip']+":8002"
    headers = {
      'content-type': "application/json" 
    }
    r = requests.post(url,headers=headers,data=payload)
    print(r)

    return "create_session_res"

