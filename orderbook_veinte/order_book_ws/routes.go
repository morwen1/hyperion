package main

import (
	"github.com/gorilla/mux"
)

func Router() *mux.Router {
	r := mux.NewRouter().StrictSlash(false)
	r.HandleFunc("/ws/btc/", BtcOrderBook).Methods("GET")
	return r
}
