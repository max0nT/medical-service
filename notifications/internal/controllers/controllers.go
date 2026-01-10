package controllers

import "notifications/notifications/internal/usecase"

type Controllers struct {
	SMTPServer usecase.SMTPServer
}

func NewControllers(smtpServ usecase.SMTPServer) *Controllers {
	return &Controllers{SMTPServer: smtpServ}
}
