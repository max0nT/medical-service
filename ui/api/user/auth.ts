import {api_client, client_error_status_code, client_error} from "./core"


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
    return await authRequest("login/", data)
}
