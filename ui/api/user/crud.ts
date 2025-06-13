import {api_client, client_error_status_code, client_error} from "./core"
import { UserWrite } from "./schemes";
import AsyncStorage from '@react-native-async-storage/async-storage';

export async function meRequest(): Promise<[number, object]> {
    let status: number = client_error_status_code;
    let response_body: object = client_error;
    await api_client.get(
        "me/",
        {
            headers: {
                Authorization: `Bearer ${await AsyncStorage.getItem("access_token")}`
            }
        }
    )
    .then(
        response => {
            status = response.status;
            response_body = response.data;
        }
    )
    .catch(
        error => {
            console.log(error);
        }
    )
    return [status, response_body]
}


export async function updateUserRequest(user: UserWrite, id: number): Promise<[number, object]>{
    let status: number = client_error_status_code;
    let response_body: object = client_error;
    await api_client.put(
        `${id}/`,
        user,
        {
            headers: {
                Authorization: `Bearer ${await AsyncStorage.getItem("access_token")}`
            }
        }
    )
    .then(
        response => {
            status = response.status;
            response_body = response.data;
        }
    )
    .catch(
        error => {
            console.log(error);
        }
    )
    return [status, response_body]
}
