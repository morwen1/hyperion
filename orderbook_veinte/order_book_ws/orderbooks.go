package main

import (
	"log"
	"net/http"
	"sync"
	"time"

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
	counter := client.Get("counter:BTC-XLT-orderId").Val()
	for {
		var msg Responses

		c := client.Get("counter:BTC-XLT-orderId").Val()
		if c != counter {

			bids := client.GetQuotes(true, 10, "bid")
			asks := client.GetQuotes(true, 10, "ask")
			msg.Asks = asks
			msg.Bids = bids
			message <- msg
			counter = client.Get("counter:BTC-XLT-orderId").Val()
			time.Sleep(10 * time.Millisecond)

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
