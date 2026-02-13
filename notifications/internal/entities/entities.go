package entities

type SignUp struct {
	Email string `json:"email"`
}

type Reserved struct {
	Email      string `json:"email"`
	To         string `json:"to"`
	ReservedAt string `json:"reserved_at"`
	QrCode     string `json:"qr_code"`
}
