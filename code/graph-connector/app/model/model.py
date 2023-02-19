from datetime import datetime
import abc

LANGUAGES = {
    "english": "en",
    "german": "de"
}


def get_field_or_default(dictionary: dict, field_to_get: str, default: any = None):
    if field_to_get not in dictionary.keys():
        return default
    return dictionary[field_to_get]


def get_field_or_exception(dictionary: dict, field_to_get: str):
    if field_to_get not in dictionary.keys():
        raise Exception(f"Field {field_to_get} not provided.")
    return dictionary[field_to_get]


class DictionarySerializableInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, '_from_dict') and
                callable(subclass._from_dict) and
                hasattr(subclass, 'to_dict') and
                callable(subclass.to_dict))


class ValueWithLanguage:
    value: str
    language: str

    def __init__(self, dictionary: dict = None) -> None:
        if dictionary:
            self._from_dict(dictionary)

    def _from_dict(self, dictionary: dict) -> None:
        self.value = get_field_or_exception(dictionary, "value")
        self.language = get_field_or_default(dictionary, "language", LANGUAGES["english"])

    def to_dict(self):
        return {
            "value": self.value,
            "language": self.language
        }


class Keyword:
    values: list[ValueWithLanguage]
    verification_status: int

    def __init__(self, dictionary: dict = None) -> None:
        if dictionary:
            self._from_dict(dictionary)

    def _from_dict(self, dictionary: dict) -> None:
        values = get_field_or_exception(dictionary, "values")
        self.values = [ValueWithLanguage(value) for value in values]
        self.verification_status = get_field_or_default(dictionary, "verification_status", 0)

    def to_dict(self) -> dict:
        return {
            "values": [value.to_dict() for value in self.values],
            "verification_status": self.verification_status
        }


class AdditionalAttribute:
    name: str
    value: str
    verification_status: int

    def __init__(self, dictionary: dict = None) -> None:
        if dictionary:
            self._from_dict(dictionary)

    def _from_dict(self, dictionary: dict) -> None:
        self.name = get_field_or_exception(dictionary, "name")
        self.value = get_field_or_exception(dictionary, "value")
        self.verification_status = get_field_or_default(dictionary, "verification_status", 0)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "value": self.value,
            "verification_status": self.verification_status
        }


class Publication:
    publication_id: str
    authors: list[str]
    title: str
    doi: str
    issued: int
    created: int
    abstract: str
    website: str
    language: str
    keywords: list[Keyword]
    additional_attributes: list[AdditionalAttribute]

    def __init__(self, dictionary: dict = None) -> None:
        if dictionary:
            self._from_dict(dictionary)

    def _from_dict(self, dictionary: dict) -> None:
        self.publication_id = get_field_or_exception(dictionary, "publication_id")
        self.authors = get_field_or_exception(dictionary, "authors")
        self.title = get_field_or_exception(dictionary, "title")
        self.doi = get_field_or_default(dictionary, "doi")
        self.abstract = get_field_or_default(dictionary, "abstract", '-')
        self.website = get_field_or_default(dictionary, "website", '-')
        self.issued = get_field_or_default(dictionary, "issued")
        self.created = get_field_or_default(dictionary, "created", datetime.now().timestamp())
        self.language = get_field_or_default(dictionary, "language", LANGUAGES["english"])
        kw = get_field_or_default(dictionary, "keywords", [])
        self.keywords = []
        for kw_dict in kw:
            self.keywords.append(Keyword(kw_dict))
        aa = get_field_or_default(dictionary, "additional_attributes", [])
        self.additional_attributes = []
        for aa_dict in aa:
            self.additional_attributes.append(AdditionalAttribute(aa_dict))

    def to_dict(self) -> dict:
        return {
            "publication_id": self.publication_id,
            "authors": self.authors,
            "title": self.title,
            "doi": self.doi,
            "issued": self.issued,
            "abstract": self.abstract,
            "website": self.website,
            "created": self.created,
            "language": self.language,
            "keywords": [keyword.to_dict() for keyword in self.keywords],
            "additional_attributes": [attribute.to_dict() for attribute in self.additional_attributes]
        }
