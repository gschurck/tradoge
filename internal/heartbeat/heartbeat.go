package heartbeat

import (
	"log"
	"net/http"
	"time"
)

var (
	client *http.Client
	url    string
)

func init() {
	client = &http.Client{
		Timeout: 10 * time.Second,
	}
}

// SetHeartbeatURL sets the URL to send heartbeats to
func SetHeartbeatURL(newURL string) {
	url = newURL
}

func sendRequest(url string) {
	if url == "" {
		return
	}
	_, err := client.Get(url)
	if err != nil {
		log.Println("Failed to send heartbeat:", err)
	}
}

// SendHeartbeat sends a heartbeat to the URL
func SendHeartbeat() {
	sendRequest(url)
}

// SendFailure sends a failure heartbeat to the URL
func SendFailure() {
	sendRequest(url + "/failure")
}
