package usecase

type SMTPServer interface {
	SendSignUpMail([]byte) error
}
