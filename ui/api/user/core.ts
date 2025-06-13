import axios, { AxiosInstance } from "axios"

const HOSTNAME = "http://10.0.2.2:8000"

export const api_client: AxiosInstance = axios.create(
    {
        baseURL: HOSTNAME + "/users/",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    }
)

export const client_error: object = {
    "detail": {
        "detail": "Неизвестная ошибка"
    }
}
export const client_error_status_code: number = 500
