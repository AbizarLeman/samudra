import datetime
from typing import List

import pydantic as pyd

from samudra.schemas.konsep import KonsepRecord, KonsepCreation


class LemmaBase(pyd.BaseModel):
    nama: str


class LemmaCreation(LemmaBase):
    # --- Relationships
    konsep: List[KonsepCreation]


class LemmaRecord(LemmaCreation):
    # --- Record specific fields
    id: int
    tarikh_masuk: datetime.datetime
    # --- Relationships
    konsep: List[KonsepRecord]

    class Config:
        orm_mode = True