package main

type tradogeConfig struct {
	Version string `validate:"required"`
	Twitter struct {
		Username string `validate:"required"`
		Password string `validate:"required"`
		Email    string
	} `validate:"required"`
	ExchangeAccounts []struct {
		AccountName  string `validate:"required"`
		ExchangeName string `validate:"oneof=binance"`
		//ApiCredentials gocryptotraderConfig.APICredentialsConfig
	} `validate:"required,min=1,unique,dive"`
	TradingPairs []struct {
		BaseCurrency        string   `validate:"required,min=2"`
		QuoteCurrency       string   `validate:"required,min=2"`
		ExchangeAccountName string   `validate:"required"`
		SearchKeywords      []string `validate:"required,min=1,unique,dive,min=2"`
	} `validate:"required,min=1,max=1,dive"`
}
