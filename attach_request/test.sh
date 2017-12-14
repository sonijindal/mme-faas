:'
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
'

i="0"

while [ $i -lt 10 ]
do
i=$[$i+1]
ue_id="123"$i
echo $ue_id
aws lambda invoke --function-name attach_request --region us-east-1 --profile default --payload '{"ue_id":'$ue_id', "ue_id_type":"guti", "enb_ue_s1ap_id":"456", "ecgi":"789", "ue_cap":"none"}' output.txt
sleep 1
done


