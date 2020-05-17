package main

import "fmt"

//KEY_PRICE_TREE = rama precios moneda-cotizacion-lado(ask,bid)
//KEY_TEMPLATE_QUOTE = rama ordenes  quote-moneda-cotizacion-ordenId
//KEY_TEMPLATE_PRICE_QUOTES = devuelve el id de esa cotizacion aputador para poder obtener las ordenes
//  KEY_PRICE_TREE > KEY_TEMPLATE_PRICE_QUOTES >KEY_TEMPLATE_PRICE_QUOTES = para traerme todas las ordenes

var KEY_PRICE_TREE = "prices-BTC-XLT-"
var KEY_TEMPLATE_QUOTE = "quote-BTC-XLT-"
var KEY_TEMPLATE_PRICE_QUOTES = "-BTC-XLT-"
var KEY_TRANSACTION = "transactions-"

func (red *RedisClient) GenaratorKeys(price string, qty string) map[string]string {
	var keys = make(map[string]string)

	keys["KEY_PRICE_TREE"] = fmt.Sprint("prices-", qty, "-", price, "-")
	keys["KEY_TEMPLATE_QUOTE"] = fmt.Sprint("quote-", qty, "-", price, "-")
	keys["KEY_TEMPLATE_PRICE_QUOTES"] = fmt.Sprint("-", qty, "-", price, "-")
	keys["KEY_TRANSACTION"] = fmt.Sprint("transactions-", qty, "-", price)
	return keys

}
