package rmq

import (
	"fmt"
	"log"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

// Config -.
type Config struct {
	URL      string
	WaitTime time.Duration
	Attempts int
}

// Connection -.
type Connection struct {
	Config

	Connection *amqp.Connection
	Channel    *amqp.Channel
}

// NewConn -.
func NewConn(cfg Config) *Connection {
	conn := &Connection{
		Config: cfg,
	}

	return conn
}

// AttemptConnect -.
func (c *Connection) AttemptConnect() error {
	var err error
	for i := c.Attempts; i > 0; i-- {
		if err = c.connect(); err == nil {
			break
		}

		log.Printf("RabbitMQ is trying to connect, attempts left: %d", i)
		time.Sleep(c.WaitTime)
	}

	if err != nil {
		return fmt.Errorf("rmq_rpc - AttemptConnect - c.connect: %w", err)
	}

	return nil
}

func (c *Connection) connect() error {
	var err error

	c.Connection, err = amqp.Dial(c.URL)
	if err != nil {
		return fmt.Errorf("amqp.Dial: %w", err)
	}
	c.Channel, err = c.Connection.Channel()
	if err != nil {
		return fmt.Errorf("c.Connection.Channel: %w", err)
	}
	return nil
}
