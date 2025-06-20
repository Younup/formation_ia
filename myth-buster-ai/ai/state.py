from __future__ import annotations
from typing import TypedDict
from typing_extensions import Annotated
from ai.configuration import Configuration
from ai.schemas import Segment


class State(TypedDict):
    configuration: Configuration
    original_content: str
    cleaned_content: str
    segments: list[Segment]
    claims: list[str]
    biases: list[str]
    verifications: list[dict[str, str]]
    verdict: dict[str, str]
    report: str