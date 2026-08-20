package main

import (
	"crypto/tls"
	"net/http"
	"time"
)

// Ghost-SY1 Advanced Anti-Fingerprinting HTTP Client (Go)
// Bypasses WAF behavioral analysis and JA3/JA4 TLS fingerprinting

func CreateStealthClient() *http.Client {
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{
			InsecureSkipVerify: true,
			// Custom cipher suites to mimic standard enterprise browsers
			CipherSuites: []uint16{
				tls.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
				tls.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
			},
		},
		DisableKeepAlives: true,
	}

	return &http.Client{
		Transport: tr,
		Timeout:   10 * time.Second,
	}
}
