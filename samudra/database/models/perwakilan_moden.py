from peewee import AutoField, ForeignKeyField, TextField, BlobField

from .base import Base
from .. import Lemma


class JenisPerwakilanModen(Base):
    id = AutoField()
    nama = TextField(null=False)
    keterangan = BlobField(null=True)


class PerwakilanModen(Base):
    id = AutoField()
    lemma = ForeignKeyField(model=Lemma, backref='perwakilan_moden')
    jenis = ForeignKeyField(model=JenisPerwakilanModen, backref='item')
    keterangan = TextField(null=False)