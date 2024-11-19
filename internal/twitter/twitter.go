package twitter

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/gschurck/tradoge/internal/types"
	twitterscraper "github.com/imperatrona/twitter-scraper"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"
	"time"
)

func updateTwitterCookies(config types.TradogeConfig) {
	scraper := twitterscraper.New()
	log.Println("Logging in to Twitter...")
	log.Println("Token:", config.Twitter.AuthToken.Token)
	log.Println("CSRFToken:", config.Twitter.AuthToken.CSRFToken)
	scraper.SetAuthToken(
		twitterscraper.AuthToken{
			Token:     config.Twitter.AuthToken.Token,
			CSRFToken: config.Twitter.AuthToken.CSRFToken,
		})

	cookies := scraper.GetCookies()
	data, _ := json.Marshal(cookies)
	var f *os.File
	f, _ = os.Create("twitter-cookies.json")
	_, err := f.Write(data)
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

func getMatchingKeyword(s string, substrs []string) string {
	s = strings.ToLower(s)
	for _, substr := range substrs {
		substr = strings.ToLower(substr)
		if strings.Contains(s, substr) {
			return substr
		}
	}
	return ""
}

func loginFromCookies(config types.TradogeConfig) *twitterscraper.Scraper {
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

func getLoggedInScrapper(config types.TradogeConfig) *twitterscraper.Scraper {
	if _, err := os.Stat("./twitter-cookies.json"); os.IsNotExist(err) {
		log.Println("Twitter cookies file does not exist")
		updateTwitterCookies(config)
	}
	scraper := loginFromCookies(config)
	if !scraper.IsLoggedIn() {
		log.Println("Not logged in")
		updateTwitterCookies(config)
		scraper = loginFromCookies(config)
		if !scraper.IsLoggedIn() {
			log.Println("Still not logged in after saving new cookies")
			panic("Failed to log in to Twitter")
		}
	}
	log.Println("Logged in")
	return scraper
}

func searchTweets(scraper *twitterscraper.Scraper, query string, config types.TradogeConfig) {
	var counter = 0

	for tweet := range scraper.SearchTweets(context.Background(), query, 10) {
		counter++
		if tweet.Error != nil {
			panic(tweet.Error)
		}
		tweetTextOnly := removeUsernamesAtStart(tweet.Text)
		matchingKeyword := getMatchingKeyword(tweetTextOnly, config.TradingPairs[0].SearchKeywords)
		// double check if the tweet contains a keyword
		log.Println(tweet.Text, tweet.TimeParsed, tweet.PermanentURL, tweet.ID)
		if matchingKeyword == "" {
			log.Println("Tweet does not contain any search keywords")
			continue
		}

	}
	log.Println("Total tweets:", counter)
}

func getLastTweet(scraper *twitterscraper.Scraper, query string) *twitterscraper.Tweet {
	tweets := scraper.SearchTweets(context.Background(), query, 1)
	for tweet := range tweets {
		if tweet.Error != nil {
			panic(tweet.Error)
		}
		return &tweet.Tweet
	}
	panic("Failed to get last tweet")
}

func MonitorTweets(config types.TradogeConfig) {
	scraper := getLoggedInScrapper(config)
	scraper.WithDelay(5)

	scraper.SetSearchMode(twitterscraper.SearchLatest)
	keywords := strings.Join(config.TradingPairs[0].SearchKeywords, " OR ")
	query := fmt.Sprintf("(%s) (from:elonmusk)", keywords)
	if !config.TradingPairs[0].IncludeReplies {
		query += " -filter:replies"
	}
	log.Println("Query:", query)

	lastTweet := getLastTweet(scraper, query)
	for {
		time.Sleep(10 * time.Second)
		log.Println("Checking for new tweets...")
		newLastTweet := getLastTweet(scraper, query)
		if newLastTweet.TimeParsed.After(lastTweet.TimeParsed) && newLastTweet.ID != lastTweet.ID {
			log.Println("New tweet found")
		}
	}
}
