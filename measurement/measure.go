package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
)

var (
	mu           sync.Mutex
	num_requests = 0
)

func main() {
	args := os.Args[1:]
	var wg sync.WaitGroup
	url := args[0]
	post_data := args[1]
	concurrency, _ := strconv.Atoi(args[2])
	wg.Add(concurrency)
	max_requests, _ := strconv.Atoi(args[3])
	//fmt.Printf("concur:%d, max_req:%d\n", concurrency, max_requests)
	for i := 0; i < concurrency; i++ {
		go func(url string, post_data string) {
			for {
				resp, err := http.Post(url, "application/json", strings.NewReader(post_data))
				if err != nil {
					continue
				}
				defer resp.Body.Close()
				body, _ := ioutil.ReadAll(resp.Body)
				fmt.Printf("%s\n", body)
				mu.Lock()
				num_requests++
				mu.Unlock()
				if num_requests >= max_requests {
					break
				}
			}
			wg.Done()
		}(url, post_data)
	}
	wg.Wait()
}
