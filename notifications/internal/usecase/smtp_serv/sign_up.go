package smtp_serv

import (
	"encoding/json"
	"fmt"
	"net/smtp"
	"notifications/notifications/internal/entities"
)

func (s *SMTP) SendSignUpMail(body []byte) error {
	var data entities.SignUp
	err := json.Unmarshal(body, &data)
	if err != nil {
		return err
	}
	message := fmt.Sprintf(
		"From: Medical Service <medical.service@gmail.com>\r\n"+
			"To: %s\r\n"+
			"Subject: Успешная регистрация\r\n"+
			"MIME-Version: 1.0\r\n"+
			"Content-Type: text/plain; charset=\"UTF-8\"\r\n"+
			"\r\n"+
			"Здравствуйте, %s!\r\n"+
			"Вы успешно зарегистрировались в MedicalService.\r\n"+
			"Ваш email: %s\r\n"+
			"\r\n"+
			"С уважением,\r\n"+
			"Команда MedicalService",
		data.Email, data.Email, data.Email,
	)
	err = smtp.SendMail(
		s.URL,
		nil,
		"medical.service@gmail.com",
		[]string{data.Email},
		[]byte(message),
	)
	return err
}
