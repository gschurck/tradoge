package twitter

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/gschurck/tradoge/internal/heartbeat"
	"github.com/gschurck/tradoge/internal/trading"
	"github.com/gschurck/tradoge/internal/types"
	twitterscraper "github.com/imperatrona/twitter-scraper"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"
	"time"
)

const rateLimitError = "429 Too Many Requests"

func updateTwitterCookies(config types.TradogeConfig) {
	scraper := twitterscraper.New()
	log.Println("Logging in to Twitter...")
	//log.Println("AuthToken:", config.Twitter.Tokens.AuthToken)
	//log.Println("CT0:", config.Twitter.Tokens.CT0)
	scraper.SetAuthToken(
		twitterscraper.AuthToken{
			Token:     config.Twitter.Tokens.AuthToken,
			CSRFToken: config.Twitter.Tokens.CT0,
		})

	cookies := scraper.GetCookies()
	data, _ := json.Marshal(cookies)
	var f *os.File
	f, _ = os.Create("data/twitter-cookies.json")
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

func loginFromCookies() *twitterscraper.Scraper {
	scraper := twitterscraper.New()
	f, _ := os.Open("data/twitter-cookies.json")
	var cookies []*http.Cookie
	err := json.NewDecoder(f).Decode(&cookies)
	if err != nil {
		log.Fatalln("Failed to read Twitter cookies file:", err)
	}
	scraper.SetCookies(cookies)
	return scraper
}

func getLoggedInScrapper(config types.TradogeConfig) *twitterscraper.Scraper {
	if _, err := os.Stat("./data/twitter-cookies.json"); os.IsNotExist(err) {
		log.Println("Twitter cookies file does not exist")
		updateTwitterCookies(config)
	}
	scraper := loginFromCookies()
	if !scraper.IsLoggedIn() {
		log.Println("Not logged in")
		updateTwitterCookies(config)
		scraper = loginFromCookies()
		if !scraper.IsLoggedIn() {
			log.Println("Still not logged in after saving new cookies")
			panic("Failed to log in to Twitter")
		}
	}
	log.Println("Logged in to Twitter")
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

func getLastMatchingTweet(scraper *twitterscraper.Scraper, query string) (*twitterscraper.Tweet, error) {
	// this call is delayed by the built-in rate limiter of the scraper
	tweets := scraper.SearchTweets(context.Background(), query, 1)
	for tweet := range tweets {
		if tweet.Error != nil {
			log.Printf("Failed to get last tweet: %v", tweet.Error)
			heartbeat.SendFailure()
			if strings.Contains(tweet.Error.Error(), rateLimitError) {
				log.Println("Rate limited, waiting 5 minutes...")
				time.Sleep(5 * time.Minute)
				break
			}
			panic(tweet.Error)
		}
		return &tweet.Tweet, nil
	}
	return nil, fmt.Errorf("no tweet found")
}

func MonitorTweets(config types.TradogeConfig) {
	scraper := getLoggedInScrapper(config)
	delaySeconds := config.Twitter.RequestDelaySeconds
	scraper.WithDelay(delaySeconds)

	scraper.SetSearchMode(twitterscraper.SearchLatest)
	keywords := strings.Join(config.TradingPairs[0].SearchKeywords, " OR ")
	query := fmt.Sprintf("(%s) (from:elonmusk)", keywords)
	if !config.TradingPairs[0].IncludeReplies {
		query += " -filter:replies"
	}
	log.Println("Query:", query)
	log.Printf("Start to search for new tweets every %d seconds...", delaySeconds)

	lastTweet, err := getLastMatchingTweet(scraper, query)
	if err != nil {
		log.Println("No older tweet found, defaulting to time 0")
		lastTweet = &twitterscraper.Tweet{
			TimeParsed: time.Unix(0, 0),
		}
	}
	trader := trading.NewTrader()
	for {
		//log.Println("Checking for new tweets...")
		heartbeat.SendHeartbeat()
		newTweet, err := getLastMatchingTweet(scraper, query)
		if err != nil {
			// No new tweet found so we continue and check again after the delay
			continue
		}
		if newTweet.TimeParsed.After(lastTweet.TimeParsed) && newTweet.ID != lastTweet.ID {
			log.Println("New tweet found:", newTweet.Text, newTweet.TimeParsed, newTweet.PermanentURL)
			lastTweet = newTweet
			trader.ProcessNewTweet(config, newTweet.Text)
		}
	}
}
