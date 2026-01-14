package controllers

import (
	"encoding/json"
	"log"

	"github.com/wagslane/go-rabbitmq"
)

func (c *Controllers) SendEmail(d rabbitmq.Delivery) rabbitmq.Action {
	var err error
	var data map[string]any
	err = json.Unmarshal(d.Body, &data)
	if err != nil {
		log.Printf(
			"Error during parsing %v: %s",
			data,
			err.Error(),
		)
		return rabbitmq.NackDiscard
	}

	switch data["email_type"] {
	case "SIGN_UP":
		err = c.SMTPServer.SendSignUpMail(data)
	default:
		log.Printf("Invalid data for email sending: %v", data)
		return rabbitmq.NackDiscard
	}

	if err != nil {
		log.Printf(
			"Error during send email with data %v: %s",
			data,
			err.Error(),
		)
		return rabbitmq.NackDiscard
	}
	return rabbitmq.Ack
}
