"""Standalone MQA (data.europa.eu Metadata Quality Assessment) baseline scorer.

Used to compare the prototype's scores against the original MQA metric on the
same RDF input. See ``docs/evaluation_vs_mqa.md``.
"""

from mqa.scorer import MQA_MAX, MqaOptions, score_dataset

__all__ = ["score_dataset", "MqaOptions", "MQA_MAX"]
