from dataclasses import dataclass
from typing import Optional


@dataclass
class Paragraph:
    volume: str = None
    text: str = None
    originalIndex: int = None
    type: Optional[str] = None
