package main

import (
	"fmt"
	"net/http"
	"time"
)

// Function that handles web requests
func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, World!")
}

// Function that calls the API
func callAPI() {
	// Dummy function to represent API calling
	fmt.Println("Calling API...")
	// Add your API calling code here
}

func main() {
	// Set up the web server in a goroutine
	go func() {
		http.HandleFunc("/", handler)
		fmt.Println("Starting server at port 8080")
		if err := http.ListenAndServe(":8080", nil); err != nil {
			fmt.Println("Server error:", err)
		}
	}()

	// Set up the ticker to call the API every 10 seconds
	go func() {
		ticker := time.NewTicker(10 * time.Second)
		for range ticker.C {
			callAPI()
		}
	}()

	// Keep the main function alive
	select {} // This blocks forever unless an interrupt is received
}
