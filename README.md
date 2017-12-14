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

## mme_sl_aws

### Test Topology

```
SERVER 1                        Functions                     SERVER 2
+------+                        +------+                      +--------+
|  eNB |                        | MME  |                      | SGW    |
+---+--+                        +--+---+                      +----+---+
    |  Attach_Request              |                               |
    +--------------------------->  |                               |
    |                              |  Create_Session_Request       |
    |                              +-----------------------------> |
    |                              |                               |
    |                              |                               |
    |                              |     Create_Session_Response   |
    |                              | <-----------------------------+
    |                              |                               |
    |   Attach_Accept              |                               |
    | <----------------------------+                               |
    |                              |                               |
    |                              |                               |
```

### Setup at cloud

Please see SETUP_<cloud_provider>.md. Eg, SETUP_AWS.md

### MME Setup

1. Run setup.sh in `attach_request`, `create_session_req`, `create_session_res` and `attach_accept`.
2. Run run.sh from all the above folders.
3. Use two cloudlab ubuntu 16.04 nodes.
4. Copy `http_enb` to one `server1` and `http_sgw` to another `server2`
5. Start `http_sgw` using `go run http_server.go`
6. Start `http_enb` using `go run http_client.go <server1_ip> <server2_ip>`
