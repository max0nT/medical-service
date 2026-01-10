package smtp_serv

type SMTP struct {
	URL string
}

func NewSMTP(url string) *SMTP {
	return &SMTP{URL: url}
}
