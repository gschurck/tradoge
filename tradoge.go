package main

import (
	"fmt"
	"github.com/gschurck/tradoge/internal/config"
	"github.com/gschurck/tradoge/internal/logger"
	"github.com/gschurck/tradoge/internal/server"
	"github.com/gschurck/tradoge/internal/twitter"
	"github.com/gschurck/tradoge/internal/utils"
	"log"
	"net/http"
	"os"
)

// Function that handles web requests
func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, World!")
}

func main() {
	logger.SetupLogger()
	// Check if the config file exists
	if _, err := os.Stat("./config/config.yaml"); os.IsNotExist(err) {
		log.Println("Config file does not exist")
		log.Println("Creating config file from example")
		err := utils.CopyFile("./config/config.example.yaml", "./config/config.yaml")
		if err != nil {
			log.Println("Failed to create config file:", err)
			return
		}
		log.Println("Config file created successfully")
	}

	conf := config.LoadConfig()

	//trader := trading.NewTrader()
	//trader.ProcessNewTweet(conf, "doge")

	twitter.MonitorTweets(conf)
	/*
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

	*/

	// Keep the main function alive
	//select {} // This blocks forever unless an interrupt is received

	server.StartServer()
}
