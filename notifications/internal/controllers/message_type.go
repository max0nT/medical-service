package controllers

type MessageType string

const (
	SignUp MessageType = "email.sign_up"
)

const UnknownMessageType = "unknown message type: %s"
