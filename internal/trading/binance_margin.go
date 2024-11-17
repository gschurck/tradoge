package trading

import (
	"context"
	"fmt"
	"github.com/adshao/go-binance/v2"
	"github.com/gschurck/tradoge/internal/types"
	"github.com/gschurck/tradoge/internal/utils"
	"log"
	"strconv"
	"strings"
	"time"
)

func TradeBinanceMargin(config types.TradogeConfig, pair types.TradingPair) {
	symbol := strings.ToUpper(pair.BaseCurrency + pair.QuoteCurrency)
	//binance.UseTestnet = true
	client := binance.NewClient(config.ExchangeAccount.ApiCredentials.Key, config.ExchangeAccount.ApiCredentials.Secret)

	preBuyAsset := GetBinanceMarginAccountAsset(client, symbol)
	leverage := utils.ParseFloat(preBuyAsset.MarginRatio)
	price := utils.ParseFloat(preBuyAsset.IndexPrice)
	preBuyQuoteAssetQuantity := utils.ParseFloat(preBuyAsset.QuoteAsset.Free)

	log.Println("price", price)
	quoteOrderQty := preBuyQuoteAssetQuantity * leverage
	log.Println("quoteOrderQty", quoteOrderQty)
	quoteOrderQtyStr := fmt.Sprintf("%f", quoteOrderQty)
	log.Println("Symbol", symbol)

	buyOrder, err := client.NewCreateMarginOrderService().IsIsolated(true).Symbol(symbol).
		Side(binance.SideTypeBuy).Type(binance.OrderTypeMarket).SideEffectType(binance.SideEffectTypeMarginBuy).
		QuoteOrderQty(quoteOrderQtyStr).Do(context.Background())
	if err != nil {
		log.Fatal("Cannot buy : ", err)
	}
	log.Println(buyOrder)
	log.Printf("Bought for %s %s of %s\n", quoteOrderQtyStr, pair.QuoteCurrency, pair.BaseCurrency)

	time.Sleep(1 * time.Minute)

	log.Println("Selling")
	refreshedBuyOrder, err := client.NewGetMarginOrderService().IsIsolated(true).Symbol(symbol).
		OrderID(buyOrder.OrderID).Do(context.Background())
	if err != nil {
		log.Fatal("Cannot get refreshed buy order", err)
	}
	log.Printf("Refreshed buy order: %s %s at price %s %s\n", refreshedBuyOrder.ExecutedQuantity, pair.BaseCurrency, refreshedBuyOrder.Price, pair.QuoteCurrency)

	preSaleAsset := GetBinanceMarginAccountAsset(client, symbol)
	preSaleBaseAssetQuantityStr := preSaleAsset.BaseAsset.Free
	preSaleBaseAssetQuantityRoundedDown := utils.RoundDown(utils.ParseFloat(preSaleBaseAssetQuantityStr))
	preSaleBaseAssetQuantityRoundedDownStr := strconv.Itoa(preSaleBaseAssetQuantityRoundedDown)

	log.Printf("Selling %s %s\n", preSaleBaseAssetQuantityRoundedDownStr, pair.BaseCurrency)
	sellOrder, err := client.NewCreateMarginOrderService().IsIsolated(true).Symbol(symbol).
		Side(binance.SideTypeSell).Type(binance.OrderTypeMarket).SideEffectType(binance.SideEffectTypeAutoRepay).
		Quantity(preSaleBaseAssetQuantityRoundedDownStr).Do(context.Background())
	if err != nil {
		if strings.Contains(err.Error(), "insufficient balance") {
			step := GetStepInfo(client, symbol)

			log.Printf("Insufficient balance on first try, trying to sell %f less", step)

			newSellOrderQty := utils.ParseFloat(refreshedBuyOrder.ExecutedQuantity) - step
			newSellOrderQtyStr := fmt.Sprintf("%f", newSellOrderQty)
			log.Printf("Selling %s %s\n", newSellOrderQtyStr, pair.BaseCurrency)

			sellOrder2, err := client.NewCreateMarginOrderService().IsIsolated(true).Symbol(symbol).
				Side(binance.SideTypeSell).Type(binance.OrderTypeMarket).SideEffectType(binance.SideEffectTypeAutoRepay).
				QuoteOrderQty(newSellOrderQtyStr).Do(context.Background())
			if err != nil {
				log.Fatal("Cannot sell", err)
			}
			sellOrder = sellOrder2
		} else {
			log.Fatal("Cannot sell", err)
		}
	}
	log.Println(sellOrder)
	//log.Println("Origin Quantity", sellOrder.OrigQuantity)
	//log.Println("Executed Quantity", sellOrder.ExecutedQuantity)
	//log.Println("Cummulative Quantity", sellOrder.CummulativeQuoteQuantity)
	log.Printf("Sold %s %s for %s %s\n", sellOrder.ExecutedQuantity, pair.BaseCurrency, sellOrder.CummulativeQuoteQuantity, pair.QuoteCurrency)

	time.Sleep(10 * time.Second)
	postSaleAsset := GetBinanceMarginAccountAsset(client, symbol)
	refreshedBaseAssetQuantity := utils.ParseFloat(postSaleAsset.BaseAsset.Free)
	refreshedQuoteAssetQuantity := utils.ParseFloat(postSaleAsset.QuoteAsset.Free)
	profit := refreshedQuoteAssetQuantity - preBuyQuoteAssetQuantity
	log.Printf("Profit: %f %s\n", profit, pair.QuoteCurrency)
	log.Printf("Base Asset Quantity still in account: %f %s\n", refreshedBaseAssetQuantity, pair.BaseCurrency)
}
