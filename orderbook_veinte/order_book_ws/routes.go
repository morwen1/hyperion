package main

import (
	"github.com/gorilla/mux"
)

func Router() *mux.Router {
	r := mux.NewRouter().StrictSlash(false)
	r.HandleFunc("/ws/{qty}/{price}", OrderBook).Methods("GET")
	r.HandleFunc("/ws/{qty}/{price}/{cant:(?:[1-9]+)", OrderbookTransactions).Methods("GET")

	return r
}
