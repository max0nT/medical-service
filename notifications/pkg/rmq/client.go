package rmq

import (
	"context"
	"errors"
	"fmt"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
	"golang.org/x/sync/errgroup"
)

// ErrConnectionClosed -.
var ErrConnectionClosed = errors.New(
	"rmq_rpc client - Client - RemoteCall - Connection closed",
)

const (
	_defaultWaitTime = 5 * time.Second
	_defaultAttempts = 10
	_defaultTimeout  = 2 * time.Second
)

// Consumers -.
type Consumers struct {
	Delivery    <-chan amqp.Delivery
	HandlerFunc func(d *amqp.Delivery) error
}

// Client -.
type Client struct {
	ctx context.Context
	eg  *errgroup.Group

	conn      *Connection
	notify    chan error
	timeout   time.Duration
	consumers []Consumers
}

// NewRMQClient -.
func NewRMQClient(url, clientExchange string) (*Client, error) {
	group, ctx := errgroup.WithContext(context.Background())
	group.SetLimit(1) // Run only one goroutine

	cfg := Config{
		URL:      url,
		WaitTime: _defaultWaitTime,
		Attempts: _defaultAttempts,
	}

	c := &Client{
		ctx:     ctx,
		eg:      group,
		conn:    NewConn(cfg),
		notify:  make(chan error),
		timeout: _defaultTimeout,
	}

	err := c.conn.AttemptConnect()
	if err != nil {
		return nil, fmt.Errorf(
			"rmq_rpc client - NewClient - c.conn.AttemptConnect: %w",
			err,
		)
	}

	return c, nil
}

// Shutdown -.
func (c *Client) Shutdown() error {
	var shutdownErrors []error

	// Wait for all goroutines to finish and get any error
	err := c.eg.Wait()
	if err != nil && !errors.Is(err, context.Canceled) {
		shutdownErrors = append(shutdownErrors, err)
	}

	// Close connection
	err = c.conn.Connection.Close()
	if err != nil {
		shutdownErrors = append(shutdownErrors, err)
	}

	return errors.Join(shutdownErrors...)
}

func (c *Client) Notify() <-chan error {
	return c.notify
}

func (c *Client) Start() {
	for _, el := range c.consumers {
		c.eg.Go(func() error {
			var err error
			for d := range el.Delivery {
				err := el.HandlerFunc(&d)
				if err != nil {
					c.notify <- err
					break
				}
			}
			return err
		})
	}
}

func (c *Client) AddConsumer(
	queueName string,
	consumer func(*amqp.Delivery) error,
) error {
	delivery, err := c.conn.Channel.Consume(
		queueName,
		"",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return err
	}
	c.consumers = append(
		c.consumers,
		Consumers{
			Delivery:    delivery,
			HandlerFunc: consumer,
		},
	)
	return nil
}
