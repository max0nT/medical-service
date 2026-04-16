export interface UserRead {
    id: number
    created: string,
    modified: string,
    email: string
    first_name: string | null,
    last_name: string | null,
    sync_with_google_calendar: boolean
    role: string
    avatar?: string | null
}

export interface UserWrite {
    first_name: string | null,
    last_name: string | null,
    sync_with_google_calendar: boolean,
}


export interface UserLogin {
    email: string
    password: string
}

export interface UserSignUp {
    email: string
    password: string
    password_repeat: string
}
