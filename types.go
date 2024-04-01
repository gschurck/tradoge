package main

import (
	gocryptotraderConfig "github.com/thrasher-corp/gocryptotrader/config"
)

type tradogeConfig struct {
	Twitter struct {
		Username string
		Password string
		Email    string
	}
	ExchangeAccounts []struct {
		AccountName    string
		ExchangeName   string
		ApiCredentials gocryptotraderConfig.APICredentialsConfig
	}
}
