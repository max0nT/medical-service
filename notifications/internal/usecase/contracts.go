package usecase

type SMTPServer interface {
	SendSignUpMail(map[string]any) error
}
