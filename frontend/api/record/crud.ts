import { GetJwtToken, MakeRequest } from "../core";


export async function ListRecordsRequest(): Promise<[number, object]> {
    const jwtToken: string = await GetJwtToken()
    return MakeRequest(
        "/records/",
        "GET",
        {},
        { "Authorization": `Bearer ${jwtToken}` },
    )
}


export async function ReserveRecordRequest(
    recordId: number,
): Promise<[number, object]> {
    const jwtToken: string = await GetJwtToken()
    return MakeRequest(
        `/records/reserve/${recordId}/`,
        "PUT",
        {},
        { "Authorization": `Bearer ${jwtToken}` },
    )
}
