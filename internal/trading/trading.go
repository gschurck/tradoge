package trading

import (
	"context"
	"fmt"
	"github.com/adshao/go-binance/v2"
	"github.com/gschurck/tradoge/internal/types"
	"github.com/gschurck/tradoge/internal/utils"
	"log"
)

/*func getExchangeById(exchangeId string) exchange.IBotExchange {
	if exchangeId != "binance" {
		return nil
	}
	emptyExchange := new(exchange.IBotExchange)
	// use func setupExchange from exchange_wrapper_standards_test.go
	return new(binance.Binance)
}*/

func TradeForExchangeName(config types.TradogeConfig, exchangeId string, pair types.TradingPair) {
	if exchangeId != "binance-margin" {
		log.Fatalf("Exchange %s is not supported", exchangeId)
	}
	/*
		ctx := context.Background()
			exchangeInstance := setupExchange(ctx, exchangeId, config)
			if exchangeInstance == nil {
				return
			}
	*/
	TradeBinanceMargin(config, pair)
}

func GetStepInfo(client *binance.Client, symbol string) float64 {
	info, err := client.NewExchangeInfoService().Do(context.Background())
	if err != nil {
		log.Fatal(err)
	}

	for _, symbolInfo := range info.Symbols {
		if symbolInfo.Symbol == symbol {
			for _, filter := range symbolInfo.Filters {
				if filter["filterType"] == "LOT_SIZE" {
					fmt.Println("found step size")
					fmt.Println(filter["stepSize"])
					stepSize, ok := filter["stepSize"].(string)
					if !ok {
						log.Fatal("stepSize is not of type string")
					}
					return utils.ParseFloat(stepSize)
				}
			}
		}
	}
	log.Fatal("Cannot find step size for symbol", symbol)
	return 0
}

func GetBinanceMarginAccountAsset(client *binance.Client, symbol string) (asset binance.IsolatedMarginAsset) {
	isolatedMarginAccount, err := client.NewGetIsolatedMarginAccountService().Do(context.Background())
	if err != nil {
		log.Fatalf("Cannot get margin account %v", err)
	}

	//log.Println(isolatedMarginAccount)
	for _, asset := range isolatedMarginAccount.Assets {
		if asset.Symbol == symbol {
			log.Println(asset)
			return asset
		}
	}
	log.Fatalf("Cannot find asset %s in isolated margin account", symbol)
	return
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
