"""EU data theme controlled vocabulary (mock subset)."""

from enum import Enum


class EUDataTheme(str, Enum):
    AGRI = "http://publications.europa.eu/resource/authority/data-theme/AGRI"
    ECON = "http://publications.europa.eu/resource/authority/data-theme/ECON"
    EDUC = "http://publications.europa.eu/resource/authority/data-theme/EDUC"
    ENVI = "http://publications.europa.eu/resource/authority/data-theme/ENVI"
    GOVE = "http://publications.europa.eu/resource/authority/data-theme/GOVE"
    HEAL = "http://publications.europa.eu/resource/authority/data-theme/HEAL"
    INTR = "http://publications.europa.eu/resource/authority/data-theme/INTR"
    JUST = "http://publications.europa.eu/resource/authority/data-theme/JUST"
    REGI = "http://publications.europa.eu/resource/authority/data-theme/REGI"
    SOCI = "http://publications.europa.eu/resource/authority/data-theme/SOCI"
    TECH = "http://publications.europa.eu/resource/authority/data-theme/TECH"
    TRAN = "http://publications.europa.eu/resource/authority/data-theme/TRAN"
