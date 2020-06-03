package main

type Order struct {
	OrderId   string `json:"orderId"`
	Qty       string `json:"qty"`
	TraderId  string `json:"traderId"`
	Price     string `json:"price"`
	Timestamp string `json:"timestamp"`
	Side      string `json:"side"`
}

type Transaction struct {
	Price string `json:"price" ; gorm:type:integer`
	Qty   string `json:"qty"; gorm:type:double`
}

type Responses struct {
	LastTransaction Transaction `json:"lastTransaction"`
	MaxPriceBid     string      `json:"maxPriceBid"`
	MinPriceBid     string      `json:"minPriceBid"`
	MaxPriceAsk     string      `json:"maxPriceAsk"`
	MinPriceAsk     string      `json:"minPriceAsk"`
	Bids            []Order     `json:"bids"`
	Asks            []Order     `json:"asks"`
}
