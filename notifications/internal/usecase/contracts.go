package usecase

import "notifications/internal/entities"

type SMTPServer interface {
	SendEmail(entities.BodyMessage, string) error
}
