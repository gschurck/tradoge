package main

import (
	"context"
	"encoding/json"
	"fmt"
	twitterscraper "github.com/imperatrona/twitter-scraper"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"
)

func updateTwitterCookies(config tradogeConfig) {
	scraper := twitterscraper.New()
	err := scraper.Login(config.Twitter.Username, config.Twitter.Password)
	if err != nil {
		panic(err)
	}
	cookies := scraper.GetCookies()
	data, _ := json.Marshal(cookies)
	var f *os.File
	f, _ = os.Create("twitter-cookies.json")
	_, err = f.Write(data)
	if err != nil {
		log.Fatalln("Failed to write Twitter cookies file:", err)
	}
	err = f.Close()
	if err != nil {
		log.Fatalln("Failed to close Twitter cookies file:", err)
	}
	log.Println("Twitter cookies saved")
}

func removeUsernamesAtStart(tweet string) string {
	// Remove all usernames at the start of the tweet
	re := regexp.MustCompile(`^(@\w+\s)+`)
	return re.ReplaceAllString(tweet, "")
}

func containsIgnoreCase(s, substr string) bool {
	s = strings.ToLower(s)
	substr = strings.ToLower(substr)
	return strings.Contains(s, substr)
}

func loginFromCookies(config tradogeConfig) *twitterscraper.Scraper {
	scraper := twitterscraper.New()
	f, _ := os.Open("twitter-cookies.json")
	var cookies []*http.Cookie
	err := json.NewDecoder(f).Decode(&cookies)
	if err != nil {
		log.Fatalln("Failed to read Twitter cookies file:", err)
	}
	scraper.SetCookies(cookies)
	return scraper
}

func twitter(config tradogeConfig) {
	if _, err := os.Stat("./twitter-cookies.json"); os.IsNotExist(err) {
		log.Println("Twitter cookies file does not exist")
		updateTwitterCookies(config)
	}
	scraper := loginFromCookies(config)
	if !scraper.IsLoggedIn() {
		fmt.Println("Not logged in")
		updateTwitterCookies(config)
		scraper = loginFromCookies(config)
		if !scraper.IsLoggedIn() {
			fmt.Println("Still not logged in after saving new cookies")
			return
		}
	}
	fmt.Println("Logged in")
	var counter = 0
	//scraper.SetSearchMode(twitterscraper.SearchLatest)
	for tweet := range scraper.SearchTweets(context.Background(), "(doge) (from:elonmusk)", 50) {
		counter++
		if tweet.Error != nil {
			panic(tweet.Error)
		}
		fmt.Println(tweet.Text, tweet.TimeParsed, tweet.PermanentURL)
		if containsIgnoreCase(removeUsernamesAtStart(tweet.Text), "doge") {
			fmt.Println(tweet.Text, tweet.TimeParsed, tweet.PermanentURL)
			//fmt.Println("Contains doge")
		}
	}
	fmt.Println("Total tweets:", counter)
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
