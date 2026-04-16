import { GetJwtToken, MakeRequest } from "../core"
import { UserLogin, UserSignUp } from "./schemes";


export async function signUpRequest(
    data: UserSignUp,
): Promise<[number, object]> {
    return await MakeRequest(
        "/users/sign-up/",
        "POST",
        data,
        {},
    )
}


export async function loginRequest(
    data: UserLogin,
): Promise<[number, object]> {
    return await MakeRequest(
        "/users/login/",
        "POST",
        data,
        {},
    )
}


export async function logoutRequest(): Promise<[number, object]> {
    const jwtToken: string = await GetJwtToken()
    return await MakeRequest(
        "/users/logout/",
        "POST",
        {},
        { "Authorization": `Bearer ${jwtToken}` },
    )
}
