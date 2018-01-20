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

var start time.Time
var UeRespIp_Arg string
var SgwReqIp_Arg string
var total_accept = 0
var num_requests = 100

func hello(w http.ResponseWriter, req *http.Request) {
	body, _ := ioutil.ReadAll(req.Body)
	var t test_struct
	err := json.Unmarshal(body, &t)
	if err != nil {
		panic(err)
	}
	io.WriteString(w, "Success")
	go func(message string, ueid int) {
		if message == "attach_accept" {
			total_accept++
			till_now := time.Since(start)
			fmt.Printf("Accepted:%d, time till now:%d ms\n", total_accept, till_now / time.Millisecond)
			if (total_accept == num_requests - 1) {
				elapsed := time.Since(start)
				fmt.Printf("Time taken to complete %d requests is %d ms\n", num_requests, elapsed / time.Millisecond);
				os.Exit(3)
			}
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
	req_url := "http://128.110.153.209:8080/function/attach_request"
	for i := 1; i < num_requests; i++ {
		ueid := i
		u := UeInfo{UeRespIp: UeRespIp_Arg, SgwReqIp: SgwReqIp_Arg, UeId: ueid, UeIdType: "guti", EnbUeS1apId: "456", Ecgi: "789", UeCap: "none"}
		form := new(bytes.Buffer)
		json.NewEncoder(form).Encode(u)
		go func(req_url string, form io.Reader) {
		  http.Post(req_url, "application/json", form)
		} (req_url, form)
		//time.Sleep(10 * time.Millisecond)
	}
}
func main() {
	argsWithoutProg := os.Args[1:]
	fmt.Println(argsWithoutProg[0])
	fmt.Println(argsWithoutProg[1])
	UeRespIp_Arg = argsWithoutProg[0]
	SgwReqIp_Arg = argsWithoutProg[1]
	start = time.Now()
	go send_requests()
	http.HandleFunc("/", hello)
	http.ListenAndServe(":8001", nil)
}
