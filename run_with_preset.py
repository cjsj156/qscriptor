import runpy
import sys
import argparse
from qscriptor.scriptor.presets import get_run_setting

def dataclass_to_argv(dclass):
    """
    Convert a dataclass to a list of command line arguments.
    """
    args = []
    for field in dclass.__dataclass_fields__.keys():
        value = getattr(dclass, field)
        args.append(f'--{field}')
        args.append(str(value))
    return args

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Script Composer')

    # run_script path
    parser.add_argument('--run_script_name',default='train.py',help=".py file to run")

    # run setting
    parser.add_argument('--run_setting_name',default='BaseConfig',help="arguments to run script")

    # custom arguments
    args = parser.parse_args()

    run_setting = get_run_setting(args.run_setting_name)
    sys.argv[1:] = dataclass_to_argv(run_setting)

    runpy.run_path(args.run_script_name, run_name="__main__")