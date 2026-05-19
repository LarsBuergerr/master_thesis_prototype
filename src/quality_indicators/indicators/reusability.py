"""Reusability indicators for DCAT-AP-DE metadata.

Validates aspects like license, access rights, publisher info, etc.
"""

from typing import Any
from rdflib import Graph
from rdflib.namespace import DCAT, DCTERMS

from quality_indicators.models.indicator import (
    Indicator,
    IndicatorResult,
    IndicatorStatus,
)
from quality_indicators.models.dimension import QualityDimension
from quality_indicators.vocabularies import OPEN_LICENSE_URIS


class LicenseIndicator(Indicator):
    """Validates if dcat:license is set."""

    def __init__(self):
        super().__init__(
            indicator_id="reuse_license",
            name_de="Lizenz angegeben",
            name_en="License specified",
            dimension=QualityDimension.REUSABILITY,
            description_de="Prüft ob dcat:license gesetzt ist",
            description_en="Checks if dcat:license is set",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
        """Validate license specification.

        Args:
            metadata: rdflib Graph with DCAT metadata

        Returns:
            IndicatorResult with score based on license specification
        """
        try:
            self.logger.debug("Running indicator validation")
            if not isinstance(metadata, Graph):
                self.logger.warning("Invalid metadata format: expected rdflib Graph")
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.ERROR,
                    score=0.0,
                    message_de="Metadaten sind kein rdflib Graph",
                    message_en="Metadata is not an rdflib Graph",
                    error="Invalid metadata format",
                )

            licenses = list(metadata.objects(predicate=DCTERMS.license))

            if not licenses:
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine Lizenz angegeben",
                    message_en="No license specified",
                    details={"license_count": 0},
                )

            open_licenses = [
                str(lic) for lic in licenses if str(lic) in OPEN_LICENSE_URIS
            ]

            if open_licenses:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = "Open-Source Lizenz gefunden"
                message_en = "Open-source license found"
            else:
                status = IndicatorStatus.PARTIAL
                score = 0.5
                message_de = "Lizenz vorhanden, aber nicht offen"
                message_en = "License specified but not open-source"

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=score,
                message_de=message_de,
                message_en=message_en,
                details={
                    "license_count": len(licenses),
                    "open_licenses": open_licenses,
                    "licenses": [str(lic) for lic in licenses],
                },
            )

        except Exception as e:
            self.logger.exception("Indicator validation failed")
            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.ERROR,
                score=0.0,
                message_de="Fehler bei der Validierung",
                message_en="Validation error",
                error=str(e),
            )


class ContactPointIndicator(Indicator):
    """Validates if dct:contactPoint is set."""

    def __init__(self):
        super().__init__(
            indicator_id="reuse_contact",
            name_de="Kontaktpunkt angegeben",
            name_en="Contact point specified",
            dimension=QualityDimension.REUSABILITY,
            description_de="Prüft ob dct:contactPoint gesetzt ist",
            description_en="Checks if dct:contactPoint is set",
            weight=0.5,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
        """Validate contact point specification.

        Args:
            metadata: rdflib Graph with DCAT metadata

        Returns:
            IndicatorResult with score based on contact point presence
        """
        try:
            self.logger.debug("Running indicator validation")
            if not isinstance(metadata, Graph):
                self.logger.warning("Invalid metadata format: expected rdflib Graph")
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.ERROR,
                    score=0.0,
                    message_de="Metadaten sind kein rdflib Graph",
                    message_en="Metadata is not an rdflib Graph",
                    error="Invalid metadata format",
                )

            contact_points = list(metadata.objects(predicate=DCAT.contactPoint))

            if not contact_points:
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Kein Kontaktpunkt angegeben",
                    message_en="No contact point specified",
                    details={"contact_count": 0},
                )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.PASS,
                score=1.0,
                message_de=f"Kontaktpunkt vorhanden: {len(contact_points)}",
                message_en=f"Contact point present: {len(contact_points)}",
                details={
                    "contact_count": len(contact_points),
                },
            )

        except Exception as e:
            self.logger.exception("Indicator validation failed")
            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.ERROR,
                score=0.0,
                message_de="Fehler bei der Validierung",
                message_en="Validation error",
                error=str(e),
            )


# Auto-register indicators when imported
_license_indicator = LicenseIndicator()
_contact_point_indicator = ContactPointIndicator()
