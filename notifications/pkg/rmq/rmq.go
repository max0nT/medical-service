package rmq

import (
	"github.com/wagslane/go-rabbitmq"
)

type RmqServer struct {
	Conn *rabbitmq.Conn
}

func NewRmqServer(url string) (*RmqServer, error) {
	conn, err := rabbitmq.NewConn(url)
	return &RmqServer{Conn: conn}, err
}
