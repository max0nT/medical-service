package smtp_client

import (
	"bytes"
	"html/template"
	"net/smtp"
	"notifications/internal/entities"
)

func (s *SmtpClient) SendEmail(
	data entities.BodyMessage,
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

	wrapperData := map[string]string{
		"Email": data.Email,
		"Body":  htmlBuf.String(),
	}

	textTmpl, err := template.ParseFiles(
		"templates/core.tmpl",
	)
	if err != nil {
		return err
	}

	var emailBuf bytes.Buffer
	err = textTmpl.Execute(&emailBuf, wrapperData)
	if err != nil {
		return err
	}

	err = smtp.SendMail(
		s.URL,
		nil,
		"medical.service@gmail.com",
		[]string{data.Email},
		emailBuf.Bytes(),
	)
	return err
}
