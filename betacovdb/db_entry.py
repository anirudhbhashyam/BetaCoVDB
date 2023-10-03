from dataclasses import dataclass

import enum

import typing


class Virus(enum.StrEnum):
    SARS_COV_2 = "sars-cov-2"
    SARS_COV_2_D614G = "sars-cov-2-d614g"
    SARS_COV_2_VICTORIA = "sars-cov-2-victoria"
    SARS_COV_2_B_1_1_7 = "sars-cov-2-b-1-1-7"
    SARS_COV_2_B_1_351 = "sars-cov-2-b-1-351"
    SARS_COV_2_P_1 = "sars-cov-2-p-1"
    SARS_COV_2_B_1_617_2 = "sars-cov-2-b-1-617-2"
    SARS_COV_2_BA_1 = "sars-cov-2-ba-1"
    SARS_COV_2_BA_1_1 = "sars-cov-2-ba-1-1"
    SARS_COV_2_BA_2 = "sars-cov-2-ba-2"
    SARS_COV_2_BA_3 = "sars-cov-2-ba-3"
    SARS_COV_2_BA_4 = "sars-cov-2-ba-4"
    SARS_COV_2_BA_5 = "sars-cov-2-ba-5"
    SARS_COV_2_XBB = "sars-cov-2-xbb"
    SARS_COV_2_XBB_1 = "sars-cov-2-xbb-1"
    SARS_COV_2_XBB_1_5 = "sars-cov-2-xbb-1-5"
    SARS_COV_1 = "sars-cov-1"
    MERS_COV = "mers-cov"
    HCOV_OC43 = "hcov-oc43"
    HCOV_HKU1 = "hcov-hku1"


class VirusState(enum.StrEnum):
    PSEUDO = "pseudovirus"
    LIVE = "livevirus"


@dataclass
class DOILink:
    prefix: str
    suffix: str
    _header: str = "https://doi.org"

    def __post_init__(self) -> None:
        self._validate()

    @classmethod
    def from_string(cls, s: str) -> typing.Self:
        prefix, suffix = s.split("/")[-2 :]
        return cls(prefix, suffix)

    def _validate(self):
        if not self.prefix.startswith("10."):
            raise ValueError(f"Invalid DOI.")
        
    def __str__(self) -> str:
        return "/".join((self._header, self.prefix, self.suffix))


@dataclass
class IC50Entry:
    name: str
    virus: Virus
    ic50: float
    source: DOILink
    virus_state: VirusState

    def __post_init__(self) -> None:
        if isinstance(self.source, str):
            self.source = DOILink.from_string(self.source)

    def get_source_link(self) -> str:
        return str(self.source)
    