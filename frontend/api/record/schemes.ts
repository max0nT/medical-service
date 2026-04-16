export interface RecordRead {
    id: number
    created: string
    modified: string
    created_by_id: number | null
    reserved_by_id: number | null
    start: string
    end: string
}
