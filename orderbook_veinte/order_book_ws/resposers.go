package main

import "time"

type Order struct {
	OrderId   int       `json:"orderId"`
	Qty       int       `json:"qty"`
	TraderId  string    `json:"traderId"`
	Price     float64   `json:"price"`
	Timestamp time.Time `json:"timestamp"`
	Side      string    `json:"side"`
}

type Responses struct {
	MaxPrice float64 `json:"maxPrice"`
	MinPrice float64 `json:"minPrice"`
	Bids     []Order `json:"bids"`
	Asks     []Order `json:"asks"`
}
