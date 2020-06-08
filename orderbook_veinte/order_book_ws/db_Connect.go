package main

import (
	"log"
	"sync"

	"github.com/go-redis/redis"
	_ "github.com/jinzhu/gorm/dialects/postgres"
)

type RedisClient struct{ *redis.Client } //redis client strcuture form
var redisClient *RedisClient
var once sync.Once

func GetRedisClient() *RedisClient {
	once.Do(func() {
		url, _ := redis.ParseURL("redis://redisgo:6379/6")
		client := redis.NewClient(&redis.Options{
			Addr:     url.Addr,
			Password: url.Password,
			DB:       url.DB,
		})
		redisClient = &RedisClient{client}
	})
	_, err := redisClient.Ping().Result()
	if err != nil {
		log.Fatal("Could not connect to redis %v", err)

	}
	return redisClient
}
