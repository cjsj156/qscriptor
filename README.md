### What you can do with runsync

You can simply make a job script by typing below command.
```
runsync_script /path/to/your/project --header_env_setting_name BaseConfig --run_script_name example.py --run_setting_name BaseConfig
```
Then a script is generated at scripts/<timestamp>.sh
```
#!/bin/bash
#$ -cwd
#$ -N
#$ -l gpu_h=1
#$ -l h_rt=24:00:00
#$ -V
. /etc/profile.d/modules.sh
source  ~/.bashrc
module load cuda/12.1 cudnn/9.0.0
conda activate env
cd /path/to/your/project

python example.py \
  --arg1 arg1 \
  --arg2 arg2 \
  --arg3 arg3
```
### Quick start
```
git clone https://github.com/cjsj156/runsync.git
pip install jinja2
```
### Make shell function to call runsync_script on bash
```
cd runsync
./set_shell_function.sh
```
### Test runsync_script with BaseConfig
```
runsync_script . --header_env_setting_name BaseConfig --run_script_name example.py --run_setting_name BaseConfig
```
It will produce a job script at scripts/timestamp.sh based on BaseConfig preset.

### Run example.py directly with BaseConfig
```
python runsync_run.py --run_script_name example.py --run_setting_name BaseConfig
```
This executes example.py with arguments pre-defined in BaseConfig.

### Make a job script to run a program in your project folder

Now you can copy runsync directory to your project folder like below
```
cp runsync /path/to/your/project_folder/
```
Note that you should not copy the whole project folder. Instead you need to just copy runsync direcotory inside this project.

Then, make new configs instead of BaseConfig according to the requirement of your python script. You can add types of settings in header_env_setting and run_setting in runsync/presets/header_env_settings.py and runsync/presets/run_settings.py

```
runsync_script /path/to/your/project_folder --header_env_setting_name <user-defined-config> --run_script_name <user-script>.py --run_setting_name <user-defined-config>
```


### Introduction
In an HPC cluster environment such as TSUBAME, users are required to submit a job script to execute a program. This script must specify the necessary computational resources, execution environment, the program to be run, and its input arguments. In most cases, once a program is determined, this information remains largely unchanged and becomes boilerplate code. This tool allows users to predefine common configurations and easily generate executable scripts. The generated script helps document the settings used during execution and reduces the likelihood of mistakes that may occur when creating such scripts manually. Moreover, the generated configuration is not only suitable for HPC job scripts but can also be reused for local executions, maintaining consistency between local and HPC environments.

### Script Generation Procedure

[[script_part.png]]

We can divide a job script into two parts. Header and environment setting part and part where we specify script to run and arguments. runsync_script makes header and environment setting part using dataclass in runsync/presets/header_ env_settings.py and running script setting with runsync/presets/run _settings.py.

runsync/presets/header_ env_settings.py
```
@dataclass
class BaseConfig:
    node_type: str = "gpu_h"
    running_time: str = "24:00:00"
    env_name: str = "env"
    cuda_version: str = "cuda/12.1"
    cudnn_version: str = "cudnn/9.0.0"
```
runsync/presets/run _settings.py
```
@dataclass
class BaseConfig:
    arg1: str = "arg1"
    arg2: str = "arg2"
    arg3: str = "arg3"
```
When the user called this settings, it renders script with below template.
```
#!/bin/bash
#$ -cwd
#$ -N {{ context.run_setting.setting_name }}
#$ -l {{ context.header_env_setting.node_type }}=1
#$ -l h_rt={{ context.header_env_setting.running_time }}
#$ -V
. /etc/profile.d/modules.sh
source  ~/.bashrc
module load {{ context.header_env_setting.cuda_version }} {{ context.header_env_setting.cudnn_version }}
conda activate {{ context.header_env_setting.env_name }}
cd {{ context.exec_path }}

python {{ context.run_script_name }} \\
{%- for key, value in context.run_setting.items() %}
  --{{ key }} {{ value }} {%- if not loop.last %} \\{%- endif -%}
{% endfor -%}
```
These context.~ are replaced by contents in dataclasses and then saved at scripts/

You can either modify dataclasses in ~_settings.py, or the template accordingly. For example, you can let runsync_script find the latest checkpoint of your deep learning model and make it to arguments to train.py. This logic can be implmeneted in scriptor object in user _defined _scriptor.py

