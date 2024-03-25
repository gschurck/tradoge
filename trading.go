package main

import (
	"github.com/thrasher-corp/gocryptotrader/exchanges/binance"
)

func trade(config viperConfig) {
	for _, exchange := range config.Exchanges {
		createExchange(exchange.Name)
	}
}

func createExchange(exchangeName string) {
	if exchangeName != "binance" {
		return
	}
	var _ = new(binance.Binance)
}
