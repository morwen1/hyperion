package main

import (
	"log"
	"net/http"
	"sync"
	"time"

	"github.com/gorilla/mux"

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

func OrderBook(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	var cripto = []string{
		"BTC",
		"LTC",
		"BSF",
		"PTR",
		"DSH",
	}
	fiat := []string{
		"BSV",
		"USD",
		"PAR",
		"PCH",
	}
	var QTY = vars["qty"]
	var PRICE = vars["price"]

	client := GetRedisClient()

	ws, err := upgrader.Upgrade(w, r, nil)
	keys := client.GenaratorKeys(PRICE, QTY)

	if err != nil {
		log.Panic("bad request")
	}

	wsClient = ws
	if QTY != PRICE {
		if (InBool(cripto, QTY) || InBool(fiat, QTY)) && (InBool(cripto, PRICE) || InBool(fiat, PRICE)) {
			counter := len(client.Keys("quote*").Val())
			counter_transactions := client.Get(keys["KEY_TRANSACTION"]).Val()
			for {
				var msg Responses
				time.Sleep(100 * time.Millisecond) // descanso de las peticiones

				c := len(client.Keys("quote*").Val())
				c_tr := client.Get(keys["KEY_TRANSACTION"]).Val()
				if c != counter || c_tr != counter_transactions { //validacion de las llaves que hay en redis

					bids := client.GetQuotes(true, 100, "bid", keys)
					asks := client.GetQuotes(true, 100, "ask", keys)
					msg.Asks = asks
					msg.Bids = bids
					msg.MinPriceAsk = client.GetPrices("asc", "ask", keys)
					msg.MinPriceBid = client.GetPrices("asc", "bid", keys)
					msg.MaxPriceAsk = client.GetPrices("desc", "ask", keys)
					msg.MaxPriceBid = client.GetPrices("desc", "bid", keys)
					msg.LastTransaction = client.GetLastTransaction(keys)

					message <- msg
					counter = len(client.Keys("quote*").Val())
					counter_transactions = client.Get(keys["KEY_TRANSACTION"]).Val()

					log.Println("change message...  ", counter)
				}

			}
		} else {
			wsClient.Close()
		}

	} else {
		wsClient.Close()
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
