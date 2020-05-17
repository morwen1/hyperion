package main

import (
	"github.com/gorilla/mux"
)

func Router() *mux.Router {
	r := mux.NewRouter().StrictSlash(false)
	r.HandleFunc("/ws/{qty}/{price}", OrderBook).Methods("GET")
	return r
}
