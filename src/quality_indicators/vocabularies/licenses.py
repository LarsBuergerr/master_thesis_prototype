"""DCAT-AP-DE license controlled vocabulary (mock subset)."""

from enum import Enum


class DcatApDeLicense(str, Enum):
    CC_BY_40 = "http://dcat-ap.de/def/licenses/cc-by/4.0"
    CC_BY_SA_40 = "http://dcat-ap.de/def/licenses/cc-by-sa/4.0"
    CC0_10 = "http://dcat-ap.de/def/licenses/cc0/1.0"
    ODC_ODBL = "http://dcat-ap.de/def/licenses/odc-odbl"
