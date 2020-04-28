package main

import "fmt"

// zrevrange  "prices-BTC-XLT-ask"  0 -1  best price ask
// zrevrange "prices-BTC-XLT-bid" 0 -1 best price bid
//KEY_PRICE_TREE = rama precios moneda-cotizacion-lado(ask,bid)
//KEY_TEMPLATE_QUOTE = rama ordenes  quote-moneda-cotizacion-ordenId
//KEY_TEMPLATE_PRICE_QUOTES = devuelve el id de esa cotizacion
var KEY_PRICE_TREE = "prices-BTC-XLT-ask"
var KEY_TEMPLATE_QUOTE = "quote-BTC-XLT"

func (red *RedisClient) GetQuotes(reverse bool, depth int) []Order {
	orders := make([]Order, 10)
	price := red.ZRevRange(KEY_PRICE_TREE, 0, -1)
	fmt.Println(price)
	return orders
}
