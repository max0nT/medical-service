package config

import (
	"github.com/spf13/viper"
)

type (
	Config struct {
		User     string `mapstructure:"rabbitmq_user"`
		Password string `mapstructure:"rabbitmq_password"`
		Port     string `mapstructure:"rabbitmq_port"`
		SmtpPort string `mapstructure:"smtp_port"`
	}
)

func NewConfig() (cfg *Config, err error) {

	viper.SetConfigType("env")
	viper.SetConfigFile("./config/.env")

	viper.AutomaticEnv()

	err = viper.ReadInConfig()
	if err != nil {
		return
	}

	err = viper.Unmarshal(&cfg)
	return
}
