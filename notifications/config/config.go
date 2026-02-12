package config

import (
	"github.com/caarlos0/env/v11"
	"github.com/joho/godotenv"
)

type (
	RMQ struct {
		RmqURL string `env:"RABBITMQ_URL,required"`
	}
	SMTP struct {
		SmtpURL string `env:"SMTP_URL,required"`
	}
	Log struct {
		Level string `env:"LOG_LEVEL,required"`
	}
	Config struct {
		RMQ
		SMTP
		Log
	}
)

func NewConfig() (*Config, error) {
	cfg := &Config{}
	err := godotenv.Load("./config/.env")
	if err != nil {
		return cfg, err
	}
	err = env.Parse(cfg)
	return cfg, err
}
