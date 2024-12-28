package trading

import (
	"context"
	"github.com/adshao/go-binance/v2"
	"github.com/gschurck/tradoge/internal/types"
	"github.com/gschurck/tradoge/internal/utils"
	"log"
	"strings"
	"sync"
)

type Trader struct {
	isTrading sync.Mutex
}

func NewTrader() *Trader {
	return &Trader{}
}

func (t *Trader) TradeForExchangeName(config types.TradogeConfig, exchangeId string, pair types.TradingPair) error {
	if exchangeId != "binance-margin" {
		log.Fatalf("Exchange %s is not supported", exchangeId)
	}

	return t.TradeBinanceMargin(config, pair)
}

func (t *Trader) ProcessNewTweet(config types.TradogeConfig, newTweetText string) {
	for _, tradingPair := range config.TradingPairs {
		log.Printf("Process trading pair %s/%s", tradingPair.BaseCurrency, tradingPair.QuoteCurrency)
		for _, keyword := range tradingPair.SearchKeywords {
			if !strings.Contains(strings.ToLower(newTweetText), strings.ToLower(keyword)) {
				log.Println("Tweet does not contain keyword", keyword)
				continue
			}
			log.Println("Tweet contains keyword", keyword)
			log.Println("Trade", tradingPair.BaseCurrency, tradingPair.QuoteCurrency)
			err := t.TradeForExchangeName(config, config.ExchangeAccount.ExchangeName, tradingPair)
			if err != nil {
				log.Println(err)
			}
			break
		}
	}
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
					log.Println("found step size")
					log.Println(filter["stepSize"])
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
