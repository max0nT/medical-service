package app

import (
	"fmt"
	"log"
	"notifications/notifications/config"
	"notifications/notifications/internal/controllers"
	"notifications/notifications/internal/usecase/smtp_serv"
	"notifications/notifications/pkg/rmq"

	"github.com/wagslane/go-rabbitmq"
)

func Run(cfg *config.Config) {
	smtpServer := smtp_serv.NewSMTP(
		"0.0.0.0:" + cfg.SmtpPort,
	)
	controllers := controllers.NewControllers(smtpServer)

	rmqClient, err := rmq.NewRmqServer(
		fmt.Sprintf(
			"amqp://%s:%s@0.0.0.0:%s",
			cfg.User,
			cfg.Password,
			cfg.Port,
		),
	)
	if err != nil {
		log.Fatalf(
			"Error during rmq connection start: %s", err.Error(),
		)
		return
	}
	defer rmqClient.Conn.Close()

	consumer, err := rabbitmq.NewConsumer(
		rmqClient.Conn,
		"email_notifications",
	)
	if err != nil {
		log.Fatalf(
			"Error during email notification consumer init: %s", err.Error(),
		)
		return
	}
	err = consumer.Run(controllers.SendEmail)
	if err != nil {
		return
	}

}
