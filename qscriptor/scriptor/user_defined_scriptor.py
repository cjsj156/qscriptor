from scriptor.base_scriptor import BaseScriptor
from dataclasses import asdict
from glob import glob
import argparse
import os
import re
from scriptor.presets import get_run_setting, get_header_env_setting
from pathlib import Path


class ExampleScriptor(BaseScriptor):
    def __init__(self):
        super().__init__()

    def get_args(self): # Required
        parser = argparse.ArgumentParser('Script Composer')
        parser.add_argument('exec_path', help="execution path") # Required argument

        # header_env setting
        parser.add_argument('--header_env_setting_name',default='BaseConfig',help="header_env_setting name")

        # run_script path
        parser.add_argument('--run_script_name',default='train.py',help=".py file to run")
 
        # run setting
        parser.add_argument('--run_setting_name',default='BaseConfig',help="arguments to run script")

        self.args = parser.parse_args()

    def set_context(self): # Required
        self.args.header_env_setting = get_header_env_setting(self.args.header_env_setting_name)
        self.args.run_setting = get_run_setting(self.args.run_setting_name)

        self.context = {
            "header_env_setting":asdict(self.args.header_env_setting),
            "run_setting":asdict(self.args.run_setting),
            "run_script_name":self.args.run_script_name,
            "exec_path":self.args.exec_path,
        }

    def make_script_template(self): # Required
        self.script_template = \
'''#!/bin/bash
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
{% endfor -%}'''


# --- user defined Scriptor ---

class DPANetScriptor(BaseScriptor):
    def __init__(self):
        super().__init__() 
        self.get_settings()
        
        self.job_script_path = Path(self.args.exec_path) / "scripts" / f"{self.args.run_setting_name}_{self.timestamp}.sh"
        log_dir = Path(self.args.exec_path)  / "scripts" / f"{self.args.run_setting_name}_{self.timestamp}_logs"
        log_dir.mkdir(exist_ok=True)
        self.top_log_path = log_dir / "top.log"
        self.nvidia_smi_log_path = log_dir / "nvidia_smi.log"
        self.set_ckpt() # Set the checkpoint path in exp_args
    
    def get_settings(self):
        self.args.header_env_setting = asdict(get_header_env_setting(self.args.header_env_setting_name))
        self.args.run_setting = asdict(get_run_setting(self.args.run_setting_name))

    def get_args(self): # Required
        parser = argparse.ArgumentParser('Script Composer')
        parser.add_argument('exec_path', help="execution path") # Required argument

        # header_env setting
        parser.add_argument('--header_env_setting_name',default='DPANetConfig',help="header_env_setting name")

        # run_script path
        parser.add_argument('--run_script_name',default='train.py',help=".py file to run")
 
        # run setting
        parser.add_argument('--run_setting_name',default='BaseConfig',help="arguments to run script")

        # custom arguments
        parser.add_argument('--ckpt_epoch',default=None,type=int,help="checkpoint epoch to evaluate or train with")

        self.args = parser.parse_args()


    def set_ckpt(self):
        def get_ckpt_num(ckpt_path):
            # epoch_130_G_0.131_P_12.039
            ckpt_path = os.path.basename(ckpt_path)
            match = re.search(r"epoch_(\d+)_G_\d+\.\d*_P_\d+\.\d*", ckpt_path)
            if match:
                return int(match.group(1))
            else:
                return -1

        if self.args.run_script_name == "train.py":
            pat = os.path.join(self.args.run_setting['save_path'], "checkpoint", "*.pth")
            ckpt_paths = sorted(glob(pat))
            if self.args.ckpt_epoch:

                if len(ckpt_paths) == 0:
                    raise ValueError(f"Checkpoint not found in {pat}")
                else:
                    for ckpt_path in ckpt_paths:
                        ckpt_num = get_ckpt_num(ckpt_path)
                        if ckpt_num == self.args.ckpt_epoch:
                            self.args.run_setting['resume_file'] = ckpt_path
                            break
            elif self.args.ckpt_epoch is None:
                if len(ckpt_paths) != 0:
                    self.args.run_setting['resume_file'] = sorted(ckpt_paths, key=lambda x: get_ckpt_num(x))[-1]
                
                    
        elif self.args.run_setting['script_path'] == "test.py":
            if self.args.ckpt_epoch:
                pat = os.path.join(self.args.run_setting['save_result_path'], "checkpoint", "*.pth")
                ckpt_paths = sorted(glob(pat))

                if len(ckpt_paths) == 0:
                    raise ValueError(f"Checkpoint not found in {pat}")
                else:
                    for ckpt_path in ckpt_paths:
                        ckpt_num = get_ckpt_num(ckpt_path)
                        if ckpt_num == self.args.ckpt_epoch:
                            self.args.run_setting['checkpoint_path'] = ckpt_path
                            break

    def set_context(self): # Required
        self.context = {
            "header_env_setting":self.args.header_env_setting,
            "run_setting":self.args.run_setting,
            "run_setting_name":self.args.run_setting_name,
            "run_script_name":self.args.run_script_name,
            "exec_path":self.args.exec_path,
            "top_log_path":self.top_log_path,
            "nvidia_smi_log_path":self.nvidia_smi_log_path,
        }

    def make_script_template(self):
        self.script_template = \
'''#!/bin/bash
#$ -cwd
#$ -N {{ context.run_setting_name }}
#$ -l {{ context.header_env_setting.node_type }}=1
#$ -l h_rt={{ context.header_env_setting.running_time }}
#$ -V
. /etc/profile.d/modules.sh
source  ~/.bashrc
module load {{ context.header_env_setting.cuda_version }} {{ context.header_env_setting.cudnn_version }}
conda activate {{ context.header_env_setting.env_name }}
cd {{ context.exec_path }}

(
  while true; do
    nvidia-smi >> {{ context.nvidia_smi_log_path }}
  sleep 5
  done
) &

(
  while true; do
    top -b -1 >> {{ context.top_log_path }}
  sleep 5
  done
) &

python {{ context.run_script_name }} \\
{%- for key, value in context.run_setting.items() %}
  --{{ key }} {{ value }} {%- if not loop.last %} \\{%- endif -%}
{% endfor -%}'''