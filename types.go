package main

import (
	gocryptotraderConfig "github.com/thrasher-corp/gocryptotrader/config"
)

type tradogeConfig struct {
	TwitterAuthToken string
	ExchangeAccounts []struct {
		AccountName    string
		ExchangeName   string
		ApiCredentials gocryptotraderConfig.APICredentialsConfig
	}
}
