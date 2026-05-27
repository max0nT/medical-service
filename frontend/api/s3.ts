import { GetJwtToken, MakeRequest } from "./core";

export interface UploadedS3File {
  name: string;
}

export async function UploadFileRequest(file: {
  uri: string;
  name: string;
  type: string;
}): Promise<[number, object]> {
  const jwtToken = await GetJwtToken();
  const formData = new FormData();

  formData.append("file", {
    uri: file.uri,
    name: file.name,
    type: file.type,
  } as unknown as Blob);

  return MakeRequest("/s3/upload/", "POST", formData, {
    Authorization: `Bearer ${jwtToken}`,
  });
}
