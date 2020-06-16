package main

import (
	"log"
	"time"
)

func main() {

	r := Router()
	server := Server(r, "0.0.0.0:8001")
	go server.ListenAndServe()
	log.Println("running server....")
	go HandleMessageMarket()
	go HandleMessageTransaction()
	logsCmd := "listening"
	for {
		log.Println(logsCmd)
		time.Sleep(3 * time.Minute)
		if logsCmd == "listening......" {
			logsCmd = "listening"
		} else {
			logsCmd = logsCmd + "."
		}

	}
}
