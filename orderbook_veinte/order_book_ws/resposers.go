package main

type Order struct {
	OrderId   string `json:"orderId"`
	Qty       string `json:"qty"`
	TraderId  string `json:"traderId"`
	Price     string `json:"price"`
	Timestamp string `json:"timestamp"`
	Side      string `json:"side"`
}

type Responses struct {
	MaxPrice float64 `json:"maxPrice"`
	MinPrice float64 `json:"minPrice"`
	Bids     []Order `json:"bids"`
	Asks     []Order `json:"asks"`
}
