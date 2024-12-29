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

// SendHeartbeat sends a heartbeat to the URL
func SendHeartbeat() {
	_, err := client.Get(url)
	if err != nil {
		log.Println("Failed to send heartbeat:", err)
	}
}

// SendFailure sends a failure heartbeat to the URL
func SendFailure() {
	_, err := client.Get(url + "/fail")
	if err != nil {
		log.Println("Failed to send failure heartbeat:", err)
	}
}
