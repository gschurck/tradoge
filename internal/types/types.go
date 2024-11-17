package types

import (
	"github.com/thrasher-corp/gocryptotrader/config"
)

type TradogeConfig struct {
	Version string `validate:"required"`
	Twitter struct {
		AuthToken AuthToken `validate:"required"`
	} `validate:"required"`
	ExchangeAccount struct {
		AccountName    string                      `validate:"required"`
		ExchangeName   string                      `validate:"oneof=binance-margin"`
		ApiCredentials config.APICredentialsConfig `validate:"required"`
	} `validate:"required"`
	TradingPairs []TradingPair `validate:"required,min=1,max=1,dive"`
}

type TradingPair struct {
	BaseCurrency        string   `validate:"required,min=2"`
	QuoteCurrency       string   `validate:"required,min=2"`
	ExchangeAccountName string   `validate:"required"`
	SearchKeywords      []string `validate:"required,min=1,unique,dive,min=2"`
}

type AuthToken struct {
	Token     string `validate:"required"`
	CSRFToken string `validate:"required"`
}
