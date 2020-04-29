package main

import (
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

func Server(r *mux.Router, address string) http.Server {

	Server := http.Server{
		Addr:              address,
		Handler:           r,
		ReadTimeout:       1 * time.Minute,
		ReadHeaderTimeout: 1 * time.Minute,
		MaxHeaderBytes:    1 << 20,
	}
	return Server
}
