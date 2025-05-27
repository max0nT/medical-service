import axios, { AxiosInstance } from "axios"

const HOSTNAME = "http://10.0.2.2:8000"

const api_client: AxiosInstance = axios.create(
    {
        baseURL: HOSTNAME + "/users/",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    }
)
const client_error: object = {
    "detail": {
        "detail": "Неизвестная ошибка"
    }
}
const client_error_status_code: number = 500

async function authRequest(
    url: string,
    data: any = {},
    headers: object = {},
): Promise<[number, object]> {
    let status: number = client_error_status_code;
    let response_body: object = client_error;
    await api_client.post(
        url,
        data,
        {
            headers: headers,
        },
    )
    .then(
        response => {
            status = response.status
            response_body = response.data
        }
    )
    .catch(
        error => {
            if (typeof error.response == "object") {
                status = error.response.status
                response_body = error.response.data
            }
        }
    )
    return [status, response_body]

}


export async function signUpRequest(
    data: any,
): Promise<[number, object]> {
    return await authRequest("sign-up/", data)
}


export async function loginRequest(
    data: any,
): Promise<[number, object]> {
    const [status_code, response_body] = await authRequest("login/", data)
    console.log(status_code)
    console.log(response_body.access_token)
    if (status_code == 200) {
        localStorage.setItem("access_token", response_body.access_token)
    }
    return [status_code, response_body]
}


export async function meRequest(): Promise<[number, object]> {
    return await authRequest(
        "me/",
        {
            "Authorization": localStorage.getItem("access_token"),
        },
    )

}
