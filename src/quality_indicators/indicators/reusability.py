"""Reusability indicators for DCAT-AP-DE metadata.

Validates aspects like license, access rights, publisher info, etc.
"""

from typing import Any, Optional
from rdflib import Graph

from quality_indicators.models.indicator import (
    Indicator,
    IndicatorResult,
    IndicatorStatus,
)
from quality_indicators.models.dimension import QualityDimension
from quality_indicators.validators.dataset_context import DatasetContext


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

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        """Validate license specification.

        Args:
            metadata: rdflib Graph with DCAT metadata
            context: Optional pre-computed dataset facts shared across
                indicators.

        Returns:
            IndicatorResult with score based on license specification
        """
        try:
            self.logger.debug(f"[{self.indicator_id}] Starting validation")
            if context is None:
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
                context = DatasetContext.from_graph(metadata)

            # Licenses are valid on both Dataset and Distribution in
            # DCAT-AP-DE — many catalogs declare the license only on the
            # distribution. Iterate both with source labels so the report
            # makes the structure visible.
            sourced = context.collect_licenses()
            dataset_count = sum(1 for sv in sourced if sv.source_kind == "dataset")
            dist_count = sum(1 for sv in sourced if sv.source_kind == "distribution")
            for sv in sourced:
                self.logger.debug(
                    f"[{self.indicator_id}]   [{sv.source_kind}] {sv.source_uri} = {sv.value}"
                )

            if not sourced:
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
                    details={
                        "license_count": 0,
                        "dataset_count": 0,
                        "distribution_count": 0,
                    },
                )

            from quality_indicators.vocabularies import OPEN_LICENSE_URIS

            open_sourced = [sv for sv in sourced if sv.value in OPEN_LICENSE_URIS]
            self.logger.debug(
                f"[{self.indicator_id}] License validation: {len(open_sourced)} open, "
                f"{len(sourced) - len(open_sourced)} proprietary "
                f"(dataset={dataset_count} distribution={dist_count})"
            )

            if open_sourced:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = "Open-Source Lizenz gefunden"
                message_en = "Open-source license found"
            else:
                status = IndicatorStatus.PARTIAL
                score = 0.5
                message_de = "Lizenz vorhanden, aber nicht offen"
                message_en = "License specified but not open-source"

            self.logger.info(
                f"[{self.indicator_id}] Result: {status.value} | Score: {score:.2f} | "
                f"{message_de} (Dataset: {dataset_count}, Distribution: {dist_count})"
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
                    "license_count": len(sourced),
                    "dataset_count": dataset_count,
                    "distribution_count": dist_count,
                    "open_licenses": [
                        {
                            "value": sv.value,
                            "source_kind": sv.source_kind,
                            "source_uri": sv.source_uri,
                        }
                        for sv in open_sourced
                    ],
                    "licenses": [
                        {
                            "value": sv.value,
                            "source_kind": sv.source_kind,
                            "source_uri": sv.source_uri,
                        }
                        for sv in sourced
                    ],
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

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        """Validate contact point specification.

        Args:
            metadata: rdflib Graph with DCAT metadata
            context: Optional pre-computed dataset facts shared across
                indicators.

        Returns:
            IndicatorResult with score based on contact point presence
        """
        try:
            self.logger.debug(f"[{self.indicator_id}] Starting validation")
            if context is None:
                context = DatasetContext.from_graph(metadata)

            contact_points = context.contact_points
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
