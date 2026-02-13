package smtp_client

import (
	"bytes"
	"html/template"
	"net/smtp"
)

func (s *SmtpClient) SendEmail(
	receiver string,
	data any,
	templateMsg string,
) error {

	htmlTmpl, err := template.ParseFiles(
		templateMsg,
	)
	if err != nil {
		return err
	}

	var htmlBuf bytes.Buffer
	err = htmlTmpl.Execute(&htmlBuf, data)
	if err != nil {
		return err
	}

	err = smtp.SendMail(
		s.URL,
		nil,
		"medical.service@gmail.com",
		[]string{receiver},
		htmlBuf.Bytes(),
	)
	return err
}
