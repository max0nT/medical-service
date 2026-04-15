import { GetJwtToken, MakeRequest } from "../core";

export async function MeRequest(): Promise<[number, object]> {
    let jwtToken: string = await GetJwtToken()
    return MakeRequest(
        "/users/me/",
        "get",
        {},
        {"Authorization": `Bearer ${jwtToken}`}
    )
}
