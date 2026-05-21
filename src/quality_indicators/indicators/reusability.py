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
            self.logger.debug(f"[{self.indicator_id}] Starting validation")
            if not isinstance(metadata, Graph):
                self.logger.warning(
                    f"[{self.indicator_id}] Invalid metadata format: expected rdflib Graph"
                )
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
            self.logger.debug(
                f"[{self.indicator_id}] Found {len(licenses)} license(s): {[str(lic) for lic in licenses]}"
            )

            if not licenses:
                self.logger.info(
                    f"[{self.indicator_id}] Result: FAIL | No licenses specified"
                )
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
            self.logger.debug(
                f"[{self.indicator_id}] License validation: {len(open_licenses)} open-source, {len(licenses) - len(open_licenses)} proprietary"
            )

            if open_licenses:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = "Open-Source Lizenz gefunden"
                message_en = "Open-source license found"
                self.logger.debug(
                    f"[{self.indicator_id}] Score calculation: PASS (open-source licenses found)"
                )
            else:
                status = IndicatorStatus.PARTIAL
                score = 0.5
                message_de = "Lizenz vorhanden, aber nicht offen"
                message_en = "License specified but not open-source"
                self.logger.debug(
                    f"[{self.indicator_id}] Score calculation: PARTIAL (non-open licenses)"
                )

            self.logger.info(
                f"[{self.indicator_id}] Result: {status.value} | Score: {score:.2f} | {message_de}"
            )

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
            self.logger.exception(
                f"[{self.indicator_id}] Validation failed with exception"
            )
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
            self.logger.debug(f"[{self.indicator_id}] Starting validation")
            if not isinstance(metadata, Graph):
                self.logger.warning(
                    f"[{self.indicator_id}] Invalid metadata format: expected rdflib Graph"
                )
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
            self.logger.debug(
                f"[{self.indicator_id}] Found {len(contact_points)} contact point(s)"
            )

            if not contact_points:
                self.logger.info(
                    f"[{self.indicator_id}] Result: FAIL | No contact points"
                )
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

            self.logger.debug(
                f"[{self.indicator_id}] Score calculation: PASS (contact points found)"
            )
            self.logger.info(
                f"[{self.indicator_id}] Result: PASS | Score: 1.00 | {len(contact_points)} contact point(s) found"
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
            self.logger.exception(
                f"[{self.indicator_id}] Validation failed with exception"
            )
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
