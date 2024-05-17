from typing import TypeAlias, TypedDict

from beanie import Document, View

DocumentModel: TypeAlias = type[Document] | type[View] | str


class BeanieParams(TypedDict):
    database: str
    document_models: list[DocumentModel]
