from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class IndustryIdentifier(BaseModel):
    type: str
    identifier: str


class VolumeInfo(BaseModel):
    title: str
    subtitle: Optional[str] = None
    authors: Optional[List[str]] = None
    industryIdentifiers: Optional[List[IndustryIdentifier]] = None
    language: str
    previewLink: HttpUrl
    infoLink: HttpUrl
    canonicalVolumeLink: HttpUrl


class GoogleBookSchema(BaseModel):
    volumeInfo: VolumeInfo
