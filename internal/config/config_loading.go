package config

import (
	"fmt"
	"github.com/go-playground/validator/v10"
	"github.com/gschurck/tradoge/internal/heartbeat"
	"github.com/gschurck/tradoge/internal/types"
	"github.com/spf13/viper"
	"log"
	"strings"
)

var validate *validator.Validate

func LoadConfig() types.TradogeConfig {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("./config")

	err := viper.ReadInConfig()
	if err != nil {
		panic(fmt.Errorf("Fatal error config file: %s \n", err))
	}

	var config types.TradogeConfig

	err = viper.Unmarshal(&config)
	if err != nil {
		panic(fmt.Errorf("unable to decode into struct, %w", err))
	}
	validate = validator.New(validator.WithRequiredStructEnabled())
	err = validate.Struct(config)
	if err != nil {
		log.Fatalln("Failed to validate config file:", err)
	}
	heartbeat.SetHeartbeatURL(config.HeartbeatURL)
	log.Println("Config file loaded successfully")
	//for _, exchangeAccount := range config.ExchangeAccounts {
	//	fmt.Println("Exchange:", exchangeAccount.AccountName)
	//}
	if config.HeartbeatURL != "" {
		log.Println("Heartbeat URL:", config.HeartbeatURL)
	}

	log.Println("Trading pairs:")
	for id, tradingPair := range config.TradingPairs {
		log.Printf("%d. %s/%s", id+1, tradingPair.BaseCurrency, tradingPair.QuoteCurrency)
		keywords := strings.Join(tradingPair.SearchKeywords, ", ")
		log.Println("   Twitter search keywords:", keywords)
		log.Println("   Sell delay minutes:", tradingPair.SellDelayMinutes)
	}

	return config
}
