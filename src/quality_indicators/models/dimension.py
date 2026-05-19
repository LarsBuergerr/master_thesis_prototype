"""Quality dimension definitions."""

from enum import Enum


class QualityDimension(Enum):
    """DCAT-AP-DE quality dimensions."""

    FINDABILITY = "findability"  # Auffindbarkeit
    ACCESSIBILITY = "accessibility"  # Zugänglichkeit
    REUSABILITY = "reusability"  # Nachnutzbarkeit
    EXPRESSIVENESS = "expressiveness"  # Aussagekraft


class Dimension:
    """Represents a quality dimension with its metadata."""

    def __init__(
        self,
        dimension_type: QualityDimension,
        name_de: str,
        name_en: str,
        description_de: str = "",
        description_en: str = "",
    ):
        """Initialize a dimension.

        Args:
            dimension_type: The dimension type
            name_de: German name
            name_en: English name
            description_de: German description
            description_en: English description
        """
        self.type = dimension_type
        self.name_de = name_de
        self.name_en = name_en
        self.description_de = description_de
        self.description_en = description_en

    def __str__(self) -> str:
        return f"{self.name_de} ({self.type.value})"


# Predefined dimensions
FINDABILITY = Dimension(
    QualityDimension.FINDABILITY,
    name_de="Auffindbarkeit",
    name_en="Findability",
    description_de="Können Datensätze durch relevante Metadaten einfach gefunden werden?",
    description_en="Can datasets be easily found through relevant metadata?",
)

ACCESSIBILITY = Dimension(
    QualityDimension.ACCESSIBILITY,
    name_de="Zugänglichkeit",
    name_en="Accessibility",
    description_de="Sind die Daten in verschiedenen Formaten zugänglich und technisch erreichbar?",
    description_en="Are the data accessible in various formats and technically reachable?",
)

REUSABILITY = Dimension(
    QualityDimension.REUSABILITY,
    name_de="Nachnutzbarkeit",
    name_en="Reusability",
    description_de="Können die Daten unter klaren Lizenzbestimmungen wiederverwendet werden?",
    description_en="Can the data be reused under clear license terms?",
)

EXPRESSIVENESS = Dimension(
    QualityDimension.EXPRESSIVENESS,
    name_de="Aussagekraft",
    name_en="Expressiveness",
    description_de="Sind die Metadaten aussagekräftig und widerspruchsfrei?",
    description_en="Are the metadata expressive and consistent?",
)
