package smtp_serv

import (
	"bytes"
	"html/template"
	"net/smtp"
	"notifications/notifications/internal/entities"
)

func (s *SMTP) SendSignUpMail(data map[string]any) error {
	serializedData := entities.SignUp{Email: data["email"].(string)}

	htmlTmpl, err := template.ParseFiles(
		"notifications/templates/sign_up.html",
	)
	if err != nil {
		return err
	}

	var htmlBuf bytes.Buffer
	err = htmlTmpl.Execute(&htmlBuf, serializedData)
	if err != nil {
		return err
	}

	wrapperData := map[string]string{
		"Email": serializedData.Email,
		"Body":  htmlBuf.String(),
	}

	textTmpl, err := template.ParseFiles(
		"notifications/templates/core.tmpl",
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
		[]string{serializedData.Email},
		emailBuf.Bytes(),
	)
	return err
}
