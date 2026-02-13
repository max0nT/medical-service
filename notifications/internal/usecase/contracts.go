package usecase

type SMTPServer interface {
	SendEmail(string, any, string) error
}
