package main

import (
	"fmt"
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
	Id              int     `json:id`
	Qty             int     `json:qty`
	Price           float64 `json:price`
	TypeTransaction string  `json:type_transaction`
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
	//var LIMIT, _ = strconv.Atoi(vars["limit"])

	client := PsqlClient()
	ws, err := upgradertr.Upgrade(w, r, nil)
	if err != nil {
		log.Panic("bad request")

	}
	wsClientr = ws
	if QTY != PRICE {
		if (InBool(cripto, QTY) || InBool(fiat, QTY)) && (InBool(cripto, PRICE) || InBool(fiat, PRICE)) {
			for {
				var msg trModel
				//consulta de sql formada con gorm trae todo lo que esta en la tabla limitando por cant y ordenada de mayor a menro con el crated_at
				rows, err := client.Raw("select id , qty ,price  , type_transaction from orderbook_transactions where market_qty='BTC'  and market_price='USD' limit 10 ;").Rows()
				if err != nil {
					log.Panic("Row error")
				}

				for rows.Next() {
					rows.Scan(&msg.Id, &msg.Qty, &msg.Price, &msg.TypeTransaction)
					fmt.Println("entro en rows", msg)

				}
				messagetr <- msg

			}
		} else {
			wsClientr.Close()
		}

	} else {
		wsClientr.Close()
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
