package main

import (
	"log"
	"notifications/config"
	"notifications/internal/app"
)

func main() {
	cfg, err := config.NewConfig()
	if err != nil {
		log.Fatalf("Error during config parsing: %s", err.Error())
		return
	}
	app.Run(cfg)
}
