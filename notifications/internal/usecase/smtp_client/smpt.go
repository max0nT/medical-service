package smtp_client

type SmtpClient struct {
	URL string
}

func NewSMTP(url string) *SmtpClient {
	return &SmtpClient{URL: url}
}
