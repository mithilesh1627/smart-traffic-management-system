from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class YOLOTrainingParams:
    epochs: int = 50
    imgsz: int = 640
    batch: int = 16
    device: int = 0

    # Optional future params
    lr0: float | None = None
    optimizer: str | None = None

    def to_dict(self) -> Dict:
        # remove None values to keep signature clean
        return {k: v for k, v in asdict(self).items() if v is not None}
