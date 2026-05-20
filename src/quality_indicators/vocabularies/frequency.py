"""Controlled vocabulary for frequency (mock subset).

This module provides a small sample of frequency URIs from the
publications.europa.eu authority space for use by indicators.
"""

from enum import Enum


class EUFrequency(str, Enum):
    CONTINUOUS = "http://publications.europa.eu/resource/authority/frequency/CONT"
    DAILY = "http://publications.europa.eu/resource/authority/frequency/DAILY"
    WEEKLY = "http://publications.europa.eu/resource/authority/frequency/WEEKLY"
    MONTHLY = "http://publications.europa.eu/resource/authority/frequency/MONTHLY"
    ANNUAL = "http://publications.europa.eu/resource/authority/frequency/ANNUAL"
    IRREGULAR = "http://publications.europa.eu/resource/authority/frequency/IRREG"
