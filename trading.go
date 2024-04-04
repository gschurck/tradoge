package main

import (
	"context"
)

func processNewTweet(config tradogeConfig) {
	for _, exchangeAccount := range config.ExchangeAccounts {
		tradeForExchangeName(config, exchangeAccount.ExchangeName)
	}
}

/*func getExchangeById(exchangeId string) exchange.IBotExchange {
	if exchangeId != "binance" {
		return nil
	}
	emptyExchange := new(exchange.IBotExchange)
	// use func setupExchange from exchange_wrapper_standards_test.go
	return new(binance.Binance)
}*/

func tradeForExchangeName(config tradogeConfig, exchangeId string) {
	ctx := context.Background()
	exchangeInstance := setupExchange(ctx, exchangeId)
	if exchangeInstance == nil {
		return
	}
	// Add your trading code here
	//exchangeInstance.Depl

}

/*
func TestSubmitOrder(t *testing.T) {
	t.Parallel()

	if !mockTests {
		sharedtestvalues.SkipTestIfCannotManipulateOrders(t, b, canManipulateRealOrders)
	}

	var orderSubmission = &order.Submit{
		Exchange: b.Name,
		Pair: currency.Pair{
			Delimiter: "_",
			Base:      currency.LTC,
			Quote:     currency.BTC,
		},
		Side:      order.Buy,
		Type:      order.Limit,
		Price:     1,
		Amount:    1000000000,
		ClientID:  "meowOrder",
		AssetType: asset.Spot,
	}

	_, err := b.SubmitOrder(context.Background(), orderSubmission)
	switch {
	case sharedtestvalues.AreAPICredentialsSet(b) && err != nil:
		t.Error("SubmitOrder() error", err)
	case !sharedtestvalues.AreAPICredentialsSet(b) && err == nil && !mockTests:
		t.Error("SubmitOrder() expecting an error when no keys are set")
	case mockTests && err != nil:
		t.Error("Mock SubmitOrder() error", err)
	}
}
*/
