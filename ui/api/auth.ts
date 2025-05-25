import axios from "axios"

const HOSTNAME = "http://10.0.2.2:8000"
const instance = axios.create({
    baseURL: HOSTNAME,
})

export default async function signUpRequest(data: any): Promise<[number, object]> {
    let result: object = {
        "detail": {
            "detail": "Неизвестная ошибка"
        }
    };
    let status: number = 500;
    await instance.post(
        "/users/sign-up/",
        data,
    )
    .then(
        response => {
            result = response.data
            status = response.status
        }
    )
    .catch(
        error => {
            if (typeof error.response == "object") {
                result = error.response.data
                status = error.response.status
            }
        }
    )
    return [status, result]

}
