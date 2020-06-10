package main

import (
	"log"
	"net/http"
	"sync"
	"time"

	"github.com/gorilla/mux"
	"github.com/gorilla/websocket"
)

var pooltr sync.Pool
var upgradertr = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	WriteBufferPool: &pooltr,
	Subprotocols:    []string{"binary"},
}

type trModel struct {
	Id              int     `json:"id"`
	Qty             int     `json:"qty"`
	Price           float64 `json:"price"`
	TypeTransaction string  `json:"type_transaction"`
}

var items []trModel

var messagetr = make(chan []trModel)
var wsClientr *websocket.Conn

func OrderbookTransactions(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	upgradertr.CheckOrigin = func(r *http.Request) bool { return true }
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
	//var LIMIT = vars["limit"]
	//var LIMIT, _ = strconv.Atoi(vars["limit"])
	redClient := GetRedisClient()
	keys := redClient.GenaratorKeys(PRICE, QTY)

	client := PsqlClient()
	wstr, err := upgradertr.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
		log.Panic("bad request")

	}
	wsClientr = wstr
	c_tr := ""
	if QTY != PRICE {

		if (InBool(cripto, QTY) || InBool(fiat, QTY)) && (InBool(cripto, PRICE) || InBool(fiat, PRICE)) {
			for {
				counterTransactions := redClient.Get(keys["COUNTER_TRANSACTION"]).Val()
				if c_tr != counterTransactions {
					var msg trModel
					//consulta de sql formada con gorm trae todo lo que esta en la tabla limitando por cant y ordenada de mayor a menro con el crated_at
					rows, err := client.Raw("SELECT id , qty ,price  , type_transaction FROM orderbook_transactions WHERE market_qty='" + QTY + "' and market_price='" + PRICE + "' ORDER BY created_at DESC LIMIT 10 ;").Rows()
					if err != nil {

						log.Panic("Row error")
					}

					for rows.Next() {
						rows.Scan(&msg.Id, &msg.Qty, &msg.Price, &msg.TypeTransaction)
						items = append(items, msg)
					}
					log.Println("new Transactions")
					c_tr = redClient.Get(keys["COUNTER_TRANSACTION"]).Val()
					messagetr <- items

				}
				time.Sleep(100 * time.Millisecond) // descanso de las peticiones

			}
		} else {
			wsClientr.Close()
		}

	} else {
		wsClientr.Close()
	}

}
func HandleMessageTransaction() {

	for {

		msg := <-messagetr
		err := wsClientr.WriteJSON(msg)
		if err != nil {
			wsClientr.Close()
		}

	}
}
