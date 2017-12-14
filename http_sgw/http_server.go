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

package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"strconv"
)

type test_struct struct {
	Message  string `json:"message"`
	UeId     int    `json:"ueId"`
	UeIdType string `json:"ueIdType"`
	UeRespIp string `json:"ueRespIp"`
}

func hello(w http.ResponseWriter, req *http.Request) {
	body, _ := ioutil.ReadAll(req.Body)
	var t test_struct
	err := json.Unmarshal(body, &t)
	if err != nil {
		panic(err)
	}
	fmt.Println(t.Message)
	fmt.Println(t.UeId)
	fmt.Println(t.UeRespIp)
	io.WriteString(w, "Hello world!")
	go func(message string, ueid int, ueRespIp string) {
		if message == "create_session_req" {
			// TODO: Don't hardcode
			req_url := "url of create_session_res from API gateway, eg. https://desaqbahb0.execute-api.us-east-1.amazonaws.com/prod/create_session_res"
			fmt.Println("Calling lambda create_session_res")
			form := make(url.Values)
			fmt.Println(ueid)
			fmt.Println(strconv.Itoa(ueid))
			form.Add("ue_id", strconv.Itoa(ueid))
			form.Add("ue_id_type", "guti")
			form.Add("ue_resp_ip", ueRespIp)
			http.PostForm(req_url, form)
		} else if message == "attach_accept" {
			fmt.Println("Got the attach accept!!")
		} else {
			fmt.Printf("Message(%s) not supported!\n", message)
		}
	}(t.Message, t.UeId, t.UeRespIp)
}

func main() {
	http.HandleFunc("/", hello)
	http.ListenAndServe(":8000", nil)
}
