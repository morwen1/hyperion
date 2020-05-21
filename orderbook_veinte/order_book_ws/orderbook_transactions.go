package main

import (
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/mux"
	"github.com/gorilla/websocket"
)

var pooltr sync.Pool
var upgradertr = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	WriteBufferPool: &pooltr,
}

type trModel struct {
	qty              int
	price            float64
	type_transaction string
}

var messagetr = make(chan trModel)
var wsClientr *websocket.Conn

func OrderbookTransactions(w http.ResponseWriter, r *http.Request) {

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
	var CANT = vars["cant"]

	client := PsqlClient()
	ws, err := upgradertr.Upgrade(w, r, nil)
	if err != nil {
		log.Panic("bad request")

		wsClientr = ws
		if QTY != PRICE {
			if (InBool(cripto, QTY) || InBool(fiat, QTY)) && (InBool(cripto, PRICE) || InBool(fiat, PRICE)) {
				for {
					var msg trModel

					//consulta de sql formada con gorm trae todo lo que esta en la tabla limitando por cant y ordenada de mayor a menro con el crated_at
					client.Table("orderbook_transactions").Select(" qty , price , type_transaction").Where("marquet_qty = ? and marquet_price = ?", QTY, PRICE).Order("crated_at ASC").Limit(CANT).Scan(&msg)
					messagetr <- msg
				}
			} else {
				wsClientr.Close()
			}

		} else {
			wsClientr.Close()
		}
	}

}
func HandleMessageTransactions() {
	for {
		msg := <-messagetr
		err := wsClientr.WriteJSON(msg)
		if err != nil {
			wsClientr.Close()
		}

	}
}
