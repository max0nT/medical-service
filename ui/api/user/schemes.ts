export interface User {
    id?: number
    created?: string,
    modified?: string,
    email?: string
    first_name?: string,
    last_name?: string,
    sync_with_google_calendar?: boolean
    role?: string
}

export interface UserWrite {
    email?: string
    first_name?: string
    last_name?: string
    sync_with_google_calendar?: boolean
}
