from dataclasses import dataclass
from dataclasses import asdict

@dataclass
class BaseConfig:
    node_type: str = "gpu_h"
    running_time: str = "24:00:00"
    env_name: str = "env"
    cuda_version: str = "cuda/12.1"
    cudnn_version: str = "cudnn/9.0.0"

# --- user input ---

@dataclass
class ExampleConfig1(BaseConfig):
    node_type: str = "node_o"
    env_name: str = "/home/8/ua04628/workdir/conda_envs/DPANet"
    ckpt_epoch: int = 0

@dataclass
class ExampleConfig2(BaseConfig):
    running_time: str = "1:00:00"
    env_name: str = "/home/8/ua04628/workdir/conda_envs/DPANet"
    ckpt_epoch: int = 0