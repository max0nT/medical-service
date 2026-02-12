package app

import (
	"fmt"
	"notifications/config"
	"notifications/internal/controllers"
	"notifications/internal/usecase/smtp_client"
	"notifications/pkg/logger"
	"notifications/pkg/rmq"
	"os"
	"os/signal"
	"syscall"
)

func Run(cfg *config.Config) {
	l := logger.New(cfg.Level)

	smtpClient := smtp_client.NewSMTP(cfg.SmtpURL)
	messageController := controllers.NewControllers(smtpClient, l)

	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt, syscall.SIGTERM)

	rmqServer, err := rmq.NewRMQClient(cfg.RmqURL, "email_exchange")
	if err != nil {
		l.Fatal(fmt.Errorf("app - Run - rmqServer - server.New: %w", err))
	}

	err = rmqServer.AddConsumer("email.sign_up", messageController.SendEmail)
	if err != nil {
		l.Fatal(
			fmt.Errorf("app - Run - rmqServer - server.AddConsumer: %w", err),
		)
	}

	err = rmqServer.AddConsumer("email.reserve", messageController.SendEmail)
	if err != nil {
		l.Fatal(
			fmt.Errorf("app - Run - rmqServer - server.AddConsumer: %w", err),
		)
	}

	rmqServer.Start()

	select {
	case s := <-interrupt:
		l.Info("app - Run - signal: %s", s.String())
	case err = <-rmqServer.Notify():
		l.Error(fmt.Errorf("app - Run - rmqServer.Notify: %w", err))
	}

	err = rmqServer.Shutdown()
	if err != nil {
		l.Error(fmt.Errorf("app - Run - rmqServer.Shutdown: %w", err))
	}

}
