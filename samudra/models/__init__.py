"""
MODEL RELATIONSHIP REPRESENTATION
Lemma  <== Konsep <==> Cakupan
                  <==> KataAsing

--- Legend ---
One  <==   Many
Many <==>  Many
"""
# Ordered by table hierarchy
from .lemma import Lemma
from .konsep import Konsep
from .cakupan import Cakupan, CakupanXKonsep
from .kata_asing import KataAsing, KataAsingXKonsep
from .pengguna import Pengguna

# Imported for type hints
from .base import BaseTable

TABLES = [
    Lemma,
    Konsep,
    Cakupan,
    KataAsing,
    Pengguna
]

JOIN_TABLES = [
    CakupanXKonsep,
    KataAsingXKonsep
]
