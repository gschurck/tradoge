package main

import (
	"context"
	"fmt"
	twitterscraper "github.com/imperatrona/twitter-scraper"
)

func twitter() {
	scraper := twitterscraper.New()

	for tweet := range scraper.GetTweets(context.Background(), "elonmusk", 5) {
		if tweet.Error != nil {
			panic(tweet.Error)
		}
		fmt.Println(tweet.Text)
	}
	/*
		scraper.SetAuthToken(twitterscraper.AuthToken{Token: token, CSRFToken: "ct0"})

		// After setting Cookies or AuthToken you have to execute IsLoggedIn method.
		// Without it, scraper wouldn't be able to make requests that requires authentication
		if !scraper.IsLoggedIn() {
			panic("Invalid AuthToken")
		}

		for tweet := range scraper.GetTweets(context.Background(), "x", 50) {
			if tweet.Error != nil {
				panic(tweet.Error)
			}
			fmt.Println(tweet.Text)
		}
	*/
}
