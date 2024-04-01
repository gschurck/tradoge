package main

import (
	"context"
	"fmt"
	"github.com/thrasher-corp/gocryptotrader/config"
	"github.com/thrasher-corp/gocryptotrader/currency"
	"github.com/thrasher-corp/gocryptotrader/engine"
	exchange "github.com/thrasher-corp/gocryptotrader/exchanges"
	"github.com/thrasher-corp/gocryptotrader/exchanges/account"

	//account "github.com/thrasher-corp/gocryptotrader/exchanges/account"
	"github.com/thrasher-corp/gocryptotrader/exchanges/asset"
	"github.com/thrasher-corp/gocryptotrader/exchanges/order"
	"log"
)

func trade(exch exchange.IBotExchange, ctx context.Context) {
	o := &order.Submit{
		Exchange:  exch.GetName(), // or method GetName() if exchange.IBotInterface
		Pair:      currency.NewPair(currency.BTC, currency.USD),
		Side:      order.Sell,
		Type:      order.Limit,
		Price:     1000000,
		Amount:    0.1,
		AssetType: asset.Spot,
	}

	// Context will be intercepted when sending an authenticated HTTP request.
	resp, err := exch.SubmitOrder(ctx, o)
	if err != nil {
		log.Fatalf("Cannot submit order %v", err)
	}
	fmt.Println(resp.OrderID)
}

func setupExchange(ctx context.Context, name string) exchange.IBotExchange {
	em := engine.NewExchangeManager()
	exch, err := em.NewExchangeByName(name)
	if err != nil {
		log.Fatalf("Cannot setup %v NewExchangeByName  %v", name, err)
	}
	//var exchCfg *config.Exchange

	//exchCfg, err = cfg.GetExchangeConfig(name)
	if err != nil {
		log.Fatalf("Cannot setup %v GetExchangeConfig %v", name, err)
	}
	exch.SetDefaults()
	exchangeConfig, err := exch.GetDefaultConfig(ctx)
	exchangeConfig.UseSandbox = true
	exchangeConfig.API.AuthenticatedSupport = true

	for k, v := range map[string]string{
		"RestUSDTMarginedFuturesURL": "https://testnet.binancefuture.com",
		"RestCoinMarginedFuturesURL": "https://testnet.binancefuture.com",
		"RestSpotURL":                "https://testnet.binance.vision/api",
		"RestSpotSupplementaryURL":   "https://testnet.binance.vision/api",
	} {
		/*
			if err := exchangeConfig.API.Endpoints.SetRunning(k.String(), v); err != nil {
				log.Fatalf("Testnet `%s` URL error with `%s`: %s", k, v, err)
			}
		*/
		exchangeConfig.API.Endpoints[k] = v
	}

	exchangeConfig.API.Credentials = config.APICredentialsConfig{
		Key:    "",
		Secret: "",
	}

	ctx = account.DeployCredentialsToContext(ctx, &account.Credentials{
		Key:    "",
		Secret: "",
	})

	err = exch.Setup(exchangeConfig)
	if err != nil {
		log.Fatalf("Cannot setup %v exchange Setup %v", name, err)
	}

	/*
		err = exch.UpdateTradablePairs(ctx, true)
		if err != nil && !errors.Is(err, context.DeadlineExceeded) {
			log.Fatalf("Cannot setup %v UpdateTradablePairs %v", name, err)
		}
		b := exch.GetBase()

		assets := b.CurrencyPairs.GetAssetTypes(false)
		if len(assets) == 0 {
			log.Fatalf("Cannot setup %v, exchange has no assets", name)
		}
		for j := range assets {
			err = b.CurrencyPairs.SetAssetEnabled(assets[j], true)
			if err != nil && !errors.Is(err, currency.ErrAssetAlreadyEnabled) {
				log.Fatalf("Cannot setup %v SetAssetEnabled %v", name, err)
			}
		}
	*/
	//trade(exch, ctx)
	cred, err := exch.GetCredentials(ctx)
	if err != nil {
		log.Fatalf("Cannot get credentials %v", err)
	}
	err = exch.VerifyAPICredentials(cred)
	if err != nil {
		log.Fatalf("Cannot verify credentials %v", err)
	}
	/*
		err = exch.ValidateAPICredentials(ctx, asset.Spot)
		if err != nil {
			log.Fatalf("Cannot validate credentials %v", err)
		}
	*/
	o := &order.Submit{
		Exchange:  exch.GetName(), // or method GetName() if exchange.IBotInterface
		Pair:      currency.NewPair(currency.BTC, currency.USD),
		Side:      order.Buy,
		Type:      order.Limit,
		Price:     1000000,
		Amount:    0.1,
		AssetType: asset.Spot,
	}
	resp, err := exch.SubmitOrder(ctx, o)
	if err != nil {
		log.Fatalf("Cannot submit order %v", err)
	}
	fmt.Println(resp)
	return exch
}

/*

func setupExchange(ctx context.Context, t *testing.T, name string, cfg *config.Config) (exchange.IBotExchange, []assetPair) {
	t.Helper()
	em := engine.NewExchangeManager()
	exch, err := em.NewExchangeByName(name)
	if err != nil {
		log.Fatalf("Cannot setup %v NewExchangeByName  %v", name, err)
	}
	var exchCfg *config.Exchange
	exchCfg, err = cfg.GetExchangeConfig(name)
	if err != nil {
		log.Fatalf("Cannot setup %v GetExchangeConfig %v", name, err)
	}
	exch.SetDefaults()
	exchCfg.API.AuthenticatedSupport = true
	exchCfg.API.Credentials = config.APICredentialsConfig{
		Key: "test",
	}

	err = exch.Setup(exchCfg)
	if err != nil {
		log.Fatalf("Cannot setup %v exchange Setup %v", name, err)
	}

	err = exch.UpdateTradablePairs(ctx, true)
	if err != nil && !errors.Is(err, context.DeadlineExceeded) {
		log.Fatalf("Cannot setup %v UpdateTradablePairs %v", name, err)
	}
	b := exch.GetBase()

	assets := b.CurrencyPairs.GetAssetTypes(false)
	if len(assets) == 0 {
		log.Fatalf("Cannot setup %v, exchange has no assets", name)
	}
	for j := range assets {
		err = b.CurrencyPairs.SetAssetEnabled(assets[j], true)
		if err != nil && !errors.Is(err, currency.ErrAssetAlreadyEnabled) {
			log.Fatalf("Cannot setup %v SetAssetEnabled %v", name, err)
		}
	}

	// Add +1 to len to verify that exchanges can handle requests with unset pairs and assets
	assetPairs := make([]assetPair, 0, len(assets)+1)
assets:
	for j := range assets {
		var pairs currency.Pairs
		pairs, err = b.CurrencyPairs.GetPairs(assets[j], false)
		if err != nil {
			log.Fatalf("Cannot setup %v asset %v GetPairs %v", name, assets[j], err)
		}
		var p currency.Pair
		p, err = getPairFromPairs(t, pairs)
		if err != nil {
			if errors.Is(err, currency.ErrCurrencyPairsEmpty) {
				continue
			}
			log.Fatalf("Cannot setup %v asset %v getPairFromPairs %v", name, assets[j], err)
		}
		err = b.CurrencyPairs.EnablePair(assets[j], p)
		if err != nil && !errors.Is(err, currency.ErrPairAlreadyEnabled) {
			log.Fatalf("Cannot setup %v asset %v EnablePair %v", name, assets[j], err)
		}
		p, err = b.FormatExchangeCurrency(p, assets[j])
		if err != nil {
			log.Fatalf("Cannot setup %v asset %v FormatExchangeCurrency %v", name, assets[j], err)
		}
		for x := range unsupportedAssets {
			if assets[j] == unsupportedAssets[x] {
				// this asset cannot handle disrupt formatting
				continue assets
			}
		}
		p, err = disruptFormatting(t, p)
		if err != nil {
			log.Fatalf("Cannot setup %v asset %v disruptFormatting %v", name, assets[j], err)
		}
		assetPairs = append(assetPairs, assetPair{
			Pair:  p,
			Asset: assets[j],
		})
	}
	assetPairs = append(assetPairs, assetPair{})

	return exch, assetPairs
}

*/
