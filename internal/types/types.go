package types

type TradogeConfig struct {
	Version string `validate:"required"`
	Twitter struct {
		Tokens TwitterTokens `validate:"required"`
	} `validate:"required"`
	ExchangeAccount struct {
		AccountName    string         `validate:"required"`
		ExchangeName   string         `validate:"oneof=binance-margin"`
		ApiCredentials ApiCredentials `validate:"required"`
	} `validate:"required"`
	TradingPairs []TradingPair `validate:"required,min=1,max=1,dive"`
}

type TradingPair struct {
	BaseCurrency        string   `validate:"required,min=2"`
	QuoteCurrency       string   `validate:"required,min=2"`
	ExchangeAccountName string   `validate:"required"`
	SearchKeywords      []string `validate:"required,min=1,unique,dive,min=2"`
	IncludeReplies      bool
}

type ApiCredentials struct {
	Key    string `validate:"required"`
	Secret string `validate:"required"`
}

type TwitterTokens struct {
	AuthToken string `validate:"required"`
	CT0       string `validate:"required"`
}
