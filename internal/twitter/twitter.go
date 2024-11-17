package twitter

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/gschurck/tradoge/internal/trading"
	"github.com/gschurck/tradoge/internal/types"
	twitterscraper "github.com/imperatrona/twitter-scraper"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"
)

func updateTwitterCookies(config types.TradogeConfig) {
	scraper := twitterscraper.New()
	fmt.Println("Logging in to Twitter...")
	fmt.Println("Token:", config.Twitter.AuthToken.Token)
	fmt.Println("CSRFToken:", config.Twitter.AuthToken.CSRFToken)
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
		fmt.Println("Not logged in")
		updateTwitterCookies(config)
		scraper = loginFromCookies(config)
		if !scraper.IsLoggedIn() {
			fmt.Println("Still not logged in after saving new cookies")
			panic("Failed to log in to Twitter")
		}
	}
	fmt.Println("Logged in")
	return scraper
}

func searchTweets(scraper *twitterscraper.Scraper, query string, config types.TradogeConfig, lastTweetFound *twitterscraper.Tweet) {
	var counter = 0

	for tweet := range scraper.SearchTweets(context.Background(), query, 5) {
		counter++
		if tweet.Error != nil {
			panic(tweet.Error)
		}
		tweetTextOnly := removeUsernamesAtStart(tweet.Text)
		matchingKeyword := getMatchingKeyword(tweetTextOnly, config.TradingPairs[0].SearchKeywords)
		// double check if the tweet contains a keyword
		if matchingKeyword == "" {
			fmt.Println("Tweet does not contain any search keywords")
			continue
		}
		fmt.Println(tweet.Text, tweet.TimeParsed, tweet.PermanentURL, tweet.ID)
		//if tweet.TimeParsed.After(lastTweetFound.TimeParsed) && tweet.ID != lastTweetFound.ID {
		//	*lastTweetFound = tweet.Tweet
		//}

	}
	fmt.Println("Total tweets:", counter)
}

func Twitter(config types.TradogeConfig) {
	scraper := getLoggedInScrapper(config)
	lastTweetFound := new(twitterscraper.Tweet)
	lastTweetFound = nil
	fmt.Println("lasttweet =", lastTweetFound)
	scraper.SetSearchMode(twitterscraper.SearchLatest)
	keywords := strings.Join(config.TradingPairs[0].SearchKeywords, " OR ")
	query := fmt.Sprintf("(%s) (from:elonmusk)", keywords)
	fmt.Println("Query:", query)
	searchTweets(scraper, query, config, lastTweetFound)
	if lastTweetFound != nil {
		fmt.Println("Last tweet found:", lastTweetFound.Text)
	}
}

func ProcessNewTweet(config types.TradogeConfig, matchingKeyword string) {
	for _, tradingPair := range config.TradingPairs {
		for _, keyword := range tradingPair.SearchKeywords {
			if keyword == matchingKeyword {
				trading.TradeForExchangeName(config, config.ExchangeAccount.ExchangeName, tradingPair)
				fmt.Println("Trade", tradingPair.BaseCurrency, tradingPair.QuoteCurrency)
				break
			}
		}
	}
}
