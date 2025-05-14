from dataclasses import dataclass
from pathlib import Path
from dataclasses import asdict

@dataclass
class BaseConfig:
    arg1: str = "arg1"
    arg2: str = "arg2"
    arg3: str = "arg3"

@dataclass
class ExampleTrainConfig(BaseConfig):
    batch_size: int = 4
    num_epochs: int = 150
    data_path: str = "./dpdd_datasets/dpdd_dataset"
