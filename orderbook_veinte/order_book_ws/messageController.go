package main

import (
	"fmt"
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

func (red *RedisClient) GetQuotes(reverse bool, depth int, side string) []Order {
	var orders []Order
	var order Order
	price_key := KEY_PRICE_TREE + side
	order_price_key := side + KEY_TEMPLATE_PRICE_QUOTES
	prices, err := red.ZRevRange(price_key, 0, -1).Result()
	fmt.Println("prices", prices, side, price_key)
	if err != nil {
		log.Fatal("eror in tree prices or empty")

	}

	for i := 0; i < len(prices); i++ {
		fmt.Println(order_price_key+prices[i], "prices")
		ordersId, err := red.LRange(order_price_key+prices[i], 0, -1).Result()

		decoder, err := mapstructure.NewDecoder(&mapstructure.DecoderConfig{Result: &order, WeaklyTypedInput: true})
		for j := 0; j < len(ordersId); j++ {
			item, err := red.HGetAll(KEY_TEMPLATE_QUOTE + ordersId[j]).Result()

			err = decoder.Decode(item)
			if err != nil {
				log.Println(item, "err into decoding", err)
			}
			orders = append(orders, order)
		}
		fmt.Println(ordersId, err, "ordersId")
	}
	return orders
}
