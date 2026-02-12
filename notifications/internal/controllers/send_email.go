package controllers

import (
	"encoding/json"
	"fmt"
	"notifications/internal/entities"

	amqp "github.com/rabbitmq/amqp091-go"
)

func (c *Controllers) SendEmail(d *amqp.Delivery) error {

	var data entities.BodyMessage
	var err error
	var template string

	defer func() {
		if err != nil {
			err = d.Reject(false)
		}
		err = d.Ack(true)
	}()

	switch d.RoutingKey {
	case string(SignUp):
		err = json.Unmarshal(d.Body, &data)
		template = "templates/sign_up.html"
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

	err = c.SMTPServer.SendEmail(data, template)
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
