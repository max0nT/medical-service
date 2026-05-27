import { GetJwtToken, MakeRequest } from "../core";
import { UserWrite } from "./schemes";

export async function MeRequest(): Promise<[number, object]> {
    let jwtToken: string = await GetJwtToken()
    return MakeRequest(
        "/users/me/",
        "get",
        {},
        {"Authorization": `Bearer ${jwtToken}`}
    )
}


export async function UpdateProfileRequest(
    userId: number,
    data: UserWrite,
): Promise<[number, object]> {
    const jwtToken: string = await GetJwtToken()
    const payload: UserWrite = {
        first_name: data.first_name ?? "",
        last_name: data.last_name ?? "",
        sync_with_google_calendar: data.sync_with_google_calendar,
        avatar: data.avatar ?? null,
    }

    return MakeRequest(
        `/users/${userId}/`,
        "PUT",
        payload,
        {
            "Authorization": `Bearer ${jwtToken}`,
        },
    )
}
