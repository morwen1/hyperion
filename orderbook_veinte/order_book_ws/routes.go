package main

import (
	"github.com/gorilla/mux"
)

func Router() *mux.Router {
	r := mux.NewRouter().StrictSlash(false)
	r.HandleFunc("/ws/market/{qty}/{price}", OrderBook).Methods("GET")
	r.HandleFunc("/ws/transaction/{qty}/{price}/{limit:[0-9]+}", OrderbookTransactions).Methods("GET")

	return r
}
