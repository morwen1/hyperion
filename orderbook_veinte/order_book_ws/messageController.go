package main

import (
	"log"

	"github.com/mitchellh/mapstructure"
)

// zrevrange  "prices-BTC-XLT-ask"  0 -1  best price ask
// zrevrange "prices-BTC-XLT-bid" 0 -1 best price bid

//KEY_PRICE_TREE = rama precios moneda-cotizacion-lado(ask,bid)
//KEY_TEMPLATE_QUOTE = rama ordenes  quote-moneda-cotizacion-ordenId
//KEY_TEMPLATE_PRICE_QUOTES = devuelve el id de esa cotizacion aputador para poder obtener las ordenes
//  KEY_PRICE_TREE > KEY_TEMPLATE_PRICE_QUOTES >KEY_TEMPLATE_PRICE_QUOTES = para traerme todas las ordenes
var KEY_PRICE_TREE = "prices-BTC-XLT-"
var KEY_TEMPLATE_QUOTE = "quote-BTC-XLT-"
var KEY_TEMPLATE_PRICE_QUOTES = "-BTC-XLT-"
var KEY_TRANSACTION = "transactions-"

func (red *RedisClient) GetQuotes(reverse bool, depth int, side string) []Order {
	var orders []Order
	var order Order
	price_key := KEY_PRICE_TREE + side
	order_price_key := side + KEY_TEMPLATE_PRICE_QUOTES
	prices, err := red.ZRevRange(price_key, 0, -1).Result()

	if err != nil {
		log.Fatal("eror in tree prices or empty")

	}

	for i := 0; i < len(prices); i++ {
		//fmt.Println(order_price_key+prices[i], "prices")
		ordersId, err := red.LRange(order_price_key+prices[i], 0, -1).Result()

		decoder, err := mapstructure.NewDecoder(&mapstructure.DecoderConfig{Result: &order, WeaklyTypedInput: true})
		for j := 0; j < len(ordersId); j++ {
			item, _ := red.HGetAll(KEY_TEMPLATE_QUOTE + ordersId[j]).Result()

			err = decoder.Decode(item)
			if err != nil {
				log.Println(item, "err into decoding", err)
			}
			orders = append(orders, order)
		}

	}
	return orders
}

func (red *RedisClient) GetPrices(orientation string, side string) string {
	price := make([]string, 0, 1)
	key := KEY_PRICE_TREE + side
	if side == "bid" {
		if orientation == "asc" {
			price = red.ZRange(key, 0, 0).Val()
		} else if orientation == "desc" {

			price = red.ZRevRange(key, 0, 0).Val()
		}
	} else if side == "ask" {
		if orientation == "asc" {
			price = red.ZRange(key, 0, 0).Val()
		} else if orientation == "desc" {
			price = red.ZRevRange(key, 0, 0).Val()
		}
	}

	result := ""
	if len(price) != 0 {
		result = price[0]
	} else {
		result = ""
	}
	return result
}

func (red *RedisClient) GetLastTransaction(coin string) Transaction {
	var tr Transaction
	qry, _ := red.HGetAll(KEY_TRANSACTION + coin).Result()
	decoder, err := mapstructure.NewDecoder(&mapstructure.DecoderConfig{Result: &tr, WeaklyTypedInput: true})

	if err == nil {
		_ = decoder.Decode(qry)

	}

	return tr
}
