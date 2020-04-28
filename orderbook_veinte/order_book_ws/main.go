package main

import "fmt"

func main() {
	c := GetRedisClient()
	x := c.GetQuotes(true, 10)
	fmt.Println(x)

}
