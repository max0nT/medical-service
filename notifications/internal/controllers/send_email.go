package controllers

import (
	"encoding/json"
	"fmt"
	"notifications/internal/entities"

	amqp "github.com/rabbitmq/amqp091-go"
)

func (c *Controllers) SendEmail(d *amqp.Delivery) error {

	var data any
	var err error
	var template, receiver string

	defer func() {
		if err != nil {
			err = d.Reject(false)
		}
		err = d.Ack(true)
	}()

	switch d.RoutingKey {
	case string(SignUp):
		var signUp entities.SignUp
		err = json.Unmarshal(d.Body, &signUp)
		data = signUp
		receiver = signUp.Email
		template = "templates/sign_up.html"
	case string(Reserved):
		var reserved entities.Reserved
		err = json.Unmarshal(d.Body, &reserved)
		data = reserved
		receiver = reserved.Email
		template = "templates/reserved.html"
	default:
		err = fmt.Errorf(UnknownMessageType, d.RoutingKey)
	}

	if err != nil {
		err = fmt.Errorf(
			"error during parsing %s: %s",
			string(d.Body),
			err.Error(),
		)
		c.Logger.Error(err)
		return nil
	}

	err = c.SMTPServer.SendEmail(receiver, data, template)
	if err != nil {
		err = fmt.Errorf(
			"error email sending %s: %s",
			string(d.Body),
			err.Error(),
		)
		return err
	}
	return nil
}
