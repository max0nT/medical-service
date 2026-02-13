package controllers

type MessageType string

const (
	SignUp   MessageType = "email.sign_up"
	Reserved MessageType = "email.reserve"
)

const UnknownMessageType = "unknown message type: %s"
