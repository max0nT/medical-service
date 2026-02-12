package controllers

import (
	"notifications/internal/usecase"
	"notifications/pkg/logger"
)

type Controllers struct {
	SMTPServer usecase.SMTPServer
	Logger     *logger.Logger
}

func NewControllers(
	smtpServ usecase.SMTPServer,
	logger *logger.Logger,
) *Controllers {
	return &Controllers{
		SMTPServer: smtpServ,
		Logger:     logger,
	}
}
