/*package main

import (
	"log"

	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/postgres"
)

func PsqlClient() *gorm.DB {

	client, err := gorm.Open("postgres", "host=postgres port=5432 dbname=orderbook_veinte user=debug password=debug sslmode=disable ")
	if err != nil {
		log.Panic("postgres conn failed", err)
	}
	return client
}
*/
package main
