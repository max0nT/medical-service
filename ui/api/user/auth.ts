import { MakeRequest } from "../core"


export async function signUpRequest(
    data: any,
): Promise<[number, object]> {
    return await MakeRequest(
        "/users/sign-up/",
        "POST",
        data,
        {},
    )
}


export async function loginRequest(
    data: any,
): Promise<[number, object]> {
    return await MakeRequest(
        "/users/login/",
        "POST",
        data,
        {},
    )
}
