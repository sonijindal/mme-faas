/*
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
*/
// This is the UE
// go run http_client.go <ue_resp_ip> <sgw_req_ip>
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

type test_struct struct {
	Message  string `json:"message"`
	UeId     int    `json:"ueId"`
	UeIdType string `json:"ueIdType"`
}

var UeRespIp_Arg string
var SgwReqIp_Arg string

func hello(w http.ResponseWriter, req *http.Request) {
	body, _ := ioutil.ReadAll(req.Body)
	//fmt.Printf("%s\n", body)
	var t test_struct
	err := json.Unmarshal(body, &t)
	if err != nil {
		panic(err)
	}
	fmt.Println(t.Message)
	fmt.Println(t.UeId)
	io.WriteString(w, "Success")
	go func(message string, ueid int) {
		if message == "attach_accept" {
			fmt.Println("Got the attach accept!!")
		} else {
			fmt.Printf("Message(%s) not supported!\n", message)
		}
	}(t.Message, t.UeId)
}

type UeInfo struct {
	UeRespIp    string
	SgwReqIp    string
	UeId        int
	UeIdType    string
	EnbUeS1apId string
	Ecgi        string
	UeCap       string
}

func send_requests() {
	//TODO: Don't hardcode
	req_url := "attach_accept url from API gateway, eg: https://desaqbahb0.execute-api.us-east-1.amazonaws.com/prod/attach_request"
	for i := 1; i < 10; i++ {
		ueid := i
		u := UeInfo{UeRespIp: UeRespIp_Arg, SgwReqIp: SgwReqIp_Arg, UeId: ueid, UeIdType: "guti", EnbUeS1apId: "456", Ecgi: "789", UeCap: "none"}
		form := new(bytes.Buffer)
		json.NewEncoder(form).Encode(u)
		fmt.Println("Sending attach_request,", ueid)
		http.Post(req_url, "application/json; charset=utf-8", form)
		//fmt.Println(resp)
		time.Sleep(1000 * time.Millisecond)
	}
}
func main() {
	argsWithoutProg := os.Args[1:]
	fmt.Println(argsWithoutProg[0])
	fmt.Println(argsWithoutProg[1])
	UeRespIp_Arg = argsWithoutProg[0]
	SgwReqIp_Arg = argsWithoutProg[1]
	go send_requests()
	http.HandleFunc("/", hello)
	http.ListenAndServe(":8000", nil)
}
