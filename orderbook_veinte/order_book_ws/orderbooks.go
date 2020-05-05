package main

import (
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

var pool sync.Pool
var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	WriteBufferPool: &pool,
}

var message = make(chan Responses)
var wsClient *websocket.Conn

func BtcOrderBook(w http.ResponseWriter, r *http.Request) {
	client := GetRedisClient()
	ws, err := upgrader.Upgrade(w, r, nil)

	if err != nil {
		log.Panic("bad request")
	}
	wsClient = ws
	counter := len(client.Keys("quote*").Val())
	for {
		var msg Responses

		c := len(client.Keys("quote*").Val())
		if c != counter {

			bids := client.GetQuotes(true, 100, "bid")
			asks := client.GetQuotes(true, 100, "ask")
			msg.Asks = asks
			msg.Bids = bids
			msg.MinPriceAsk = client.GetPrices("asc", "ask")
			msg.MinPriceBid = client.GetPrices("asc", "bid")
			msg.MaxPriceAsk = client.GetPrices("desc", "ask")
			msg.MaxPriceBid = client.GetPrices("desc", "bid")
			msg.LastTransaction = client.GetLastTransaction("BTC")

			message <- msg
			counter = len(client.Keys("quote*").Val())
			log.Println("change message...  ", counter)
		}

	}
}
func HandleMessage() {
	for {
		msg := <-message
		err := wsClient.WriteJSON(msg)
		if err != nil {
			wsClient.Close()
		}

	}
}
