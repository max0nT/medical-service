package controllers

import (
	"log"

	"github.com/wagslane/go-rabbitmq"
)

func (c *Controllers) SignUp(d rabbitmq.Delivery) rabbitmq.Action {
	err := c.SMTPServer.SendSignUpMail(d.Body)
	if err != nil {
		log.Fatalf("Error during send message %s", err.Error())
		return rabbitmq.NackDiscard
	}
	return rabbitmq.Ack
}
