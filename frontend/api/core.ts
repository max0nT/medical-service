import AsyncStorage from "@react-native-async-storage/async-storage";
import axios, { AxiosInstance, Axios } from "axios";


const HOSTNAME = process.env.EXPO_PUBLIC_API_URL
console.log(HOSTNAME)
export const internalError: object = {
    "detail": {
        "detail": "Internal Error. Don't Worry our best specialists are already working on this"
    }
}

export const apiClient: AxiosInstance = axios.create(
    {
        baseURL: HOSTNAME,
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    }
)

export async function MakeRequest(
    url: string,
    method: string,
    data: object | null = null,
    headers: object,

): Promise<[number, object]> {
    let status: number = 500;
    let content: object = internalError;

    if (data == null) {
        data = {}
    }
    await apiClient.request(
        {
            url: url,
            method: method,
            data: data,
            headers: headers,
        }
    ).then(
        response => {
            status = response.status
            content = response.data
        }
    )
    .catch(
        error => {
            console.log(error)
            if ( error.response &&typeof error.response == "object") {
                status = error.response.status
                content = error.response.data
            }
        }
    )
    return [status, content] as [number, object]
}


export async function GetJwtToken(): Promise<string> {
    let jwtToken: string = ""
    await AsyncStorage.getItem("access_token")
    .then((value: string | null) => {
        if (value != null) {
            jwtToken = value
        }
    }).catch( e => {
        console.log("Error during get jwt token: " + e)
    })
    return jwtToken
}
