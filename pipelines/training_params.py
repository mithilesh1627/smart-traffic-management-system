from dataclasses import dataclass, asdict
from typing import Dict,Literal


@dataclass(frozen=True)
class YOLOTrainingParams:
    training_name: str = "traffic_yolo"
    epochs: int = 1
    imgsz: int = 640
    batch: int = 16
    device: int = '0'
    device: Literal["cpu", "cuda", "auto", "0", "1"] = "auto"
    lr0: float | None = None
    optimizer: str | None = None
    verbose: bool = True

    def to_dict(self) -> Dict:
        # remove None values to keep signature clean
        return {k: v for k, v in asdict(self).items() if v is not None}
