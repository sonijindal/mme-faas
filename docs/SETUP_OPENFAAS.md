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


## Install OpenFaas
```
git clone https://github.com/openfaas/faas && \
cd faas && \
git checkout 0.6.5 && \
./deploy_stack.sh
```

## Install docker
```
curl -sSL https://get.docker.com/ | sh
sudo docker swarm init
```
## Login to docker hub for pushing images
```
docker login
```

## Build and deploy functions
```
faas-cli build -f <function>.yml
faas-cli push -f <function>.yml
faas-cli deploy -f <function>.yml
```

## Check logs
```
docker service logs <function> -f
```

## Remove a function
```
docker service rm <function>
```

## Testing
1. Start http_server in one terminal
2. Start http_client in another terminal: 
```
go run http_client.go <ue_resp_ip> <sgw_req_ip>
```

For each request sent from the client, it should receive "Got the attach accept!!"
