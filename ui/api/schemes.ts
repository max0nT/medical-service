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

export interface Record {
    id: number;
    created_by_id: number | null;
    reserved_by_id: number | null;
    start: string;
    end: string;
}

export interface RecordWrite {
    start: string;
    end: string;
}
