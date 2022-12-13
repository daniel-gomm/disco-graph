export interface Publication {
    publication_id: string,
    author: string,
    title: string,
    doi?: string,
    issued: number,
    created?: number,
    language: string,
    keywords?: Keyword[],
    additional_attributes?: AdditionalAttribute[]
}

export interface Keyword {
    values: ValueWithLanguage[],
    verification_status: number
}

export interface AdditionalAttribute {
    name: string,
    value: string,
    verification_status: number
}

export interface ValueWithLanguage {
    value: string,
    language: string
}