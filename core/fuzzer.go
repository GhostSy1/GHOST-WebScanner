package main

import (
	"fmt"
	"net/http"
	"time"
)

// Ghost-SY1 High-Speed Go Web Fuzzer & API Endpoint Discoverer
func FuzzEndpoint(target string, word string, results chan<- string) {
	url := fmt.Sprintf("%s/%s", target, word)
	client := &http.Client{Timeout: 3 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == 200 || resp.StatusCode == 403 {
		results <- fmt.Sprintf("[+] Discovered Endpoint: /%s (Status: %d)", word, resp.StatusCode)
	}
}

func RunGoFuzzer(target string) {
	words := []string{"admin", "login", "api/v1", "config.json", ".env", "dashboard", "graphql", "backup.sql", "wp-login.php"}
	results := make(chan string, len(words))

	for _, word := range words {
		go FuzzEndpoint(target, word, results)
	}

	for i := 0; i < len(words); i++ {
		select {
		case res := <-results:
			fmt.Println(res)
		case <-time.After(4 * time.Second):
			// Timeout non-blocking
		}
	}
}
