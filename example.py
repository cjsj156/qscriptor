import argparse

parser = argparse.ArgumentParser('Script Composer')
parser.add_argument('--batch_size', default=1, help="")
parser.add_argument('--num_epochs', default=1, help="")
parser.add_argument('--data_path', default="/default", help="")
parser.add_argument('--arg1', default=1, help="")
parser.add_argument('--arg2', default=1, help="")
parser.add_argument('--arg3', default=1, help="")
args = parser.parse_args()

args = vars(args)

for key, value in args.items():
    print(f'--{key} {value}')