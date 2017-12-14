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

## Parameter generation:

### role_arn

Create an invoker role following the steps in [this](https://www.oreilly.com/learning/how-do-i-invoke-a-lambda-from-another-lambda-in-aws) from 1:22min

### req_url
1. Create API_GATEWAY from api gateway console. Follow instructions in [this link](http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-from-example.html)

2. Add API_GATEWAY trigger to `attach_request` and `create_session_res` and set the `Security` as `None` from the dropdown menu.
3. Note the URLs for both the functions and update in `http_client.go` and `http_server.go`

### Database
#### Create RDS MySQL database:

Follow these [instructions](http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateInstance.html) to create an RDS instance.

###### rds_host

From the RDS console, copy the host url and enter in the `rds_host` field of `rds_config.py`

###### db_username

At step 7 from the aws [link](http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateInstance.html), the username you entered needs to be set in `db_username` field of `rds_config.py`

###### db_password

At step 7 from the aws [link](http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateInstance.html), the password you entered needs to be set in `db_password` field of `rds_config.py`

###### db_name

Connect to the `rds_host` using CLI or MySQLWorkBench

CLI:

```
$ mysql -h <rds_host> -P 3306 -u <db_username> -p
<db_password>

mysql> CREATE DATABASE mme_ue_db
mysql> use mme_ue_db
```
#### Create two tables:

Using CLI or MySQLWorkBench create two tables as follows:

```
mysql> CREATE TABLE `ue_info` (
  `ue_id` int(11) NOT NULL,
  `ue_id_type` varchar(45) NOT NULL,
  `ue_state` int(11) DEFAULT NULL,
  `enb_ue_s1ap_id` varchar(45) DEFAULT NULL,
  `ue_cap` varchar(45) DEFAULT NULL,
  `mme_s1ap_ue_id` int(11) DEFAULT NULL,
  `ecgi` varchar(45) DEFAULT NULL,
  `eps_bearer_id` int(11) DEFAULT NULL,
  `pgw_ip` varchar(45) DEFAULT NULL,
  `apn` varchar(45) DEFAULT NULL,
  `tai` varchar(45) DEFAULT NULL,
  `s1_sgw_teid` varchar(45) DEFAULT NULL,
  `s5_pgw_teid` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ue_id`),
  UNIQUE KEY `ue_id_UNIQUE` (`ue_id`));

mysql> describe ue_info;
+----------------+-------------+------+-----+---------+-------+
| Field          | Type        | Null | Key | Default | Extra |
+----------------+-------------+------+-----+---------+-------+
| ue_id          | int(11)     | NO   | PRI | NULL    |       |
| ue_id_type     | varchar(45) | NO   |     | NULL    |       |
| ue_state       | int(11)     | YES  |     | NULL    |       |
| enb_ue_s1ap_id | varchar(45) | YES  |     | NULL    |       |
| ue_cap         | varchar(45) | YES  |     | NULL    |       |
| mme_s1ap_ue_id | int(11)     | YES  |     | NULL    |       |
| ecgi           | varchar(45) | YES  |     | NULL    |       |
| eps_bearer_id  | int(11)     | YES  |     | NULL    |       |
| pgw_ip         | varchar(45) | YES  |     | NULL    |       |
| apn            | varchar(45) | YES  |     | NULL    |       |
| tai            | varchar(45) | YES  |     | NULL    |       |
| s1_sgw_teid    | varchar(45) | YES  |     | NULL    |       |
| s5_pgw_teid    | varchar(45) | YES  |     | NULL    |       |
+----------------+-------------+------+-----+---------+-------+
13 rows in set (0.06 sec)

mysql> CREATE TABLE `mme_ue_ids` (
  `mme_s1ap_ue_id` int(11) NOT NULL,
  PRIMARY KEY (`mme_s1ap_ue_id`)
)

mysql> describe mme_ue_ids;
+----------------+---------+------+-----+---------+-------+
| Field          | Type    | Null | Key | Default | Extra |
+----------------+---------+------+-----+---------+-------+
| mme_s1ap_ue_id | int(11) | NO   | PRI | NULL    |       |
+----------------+---------+------+-----+---------+-------+
1 row in set (0.05 sec)
```


