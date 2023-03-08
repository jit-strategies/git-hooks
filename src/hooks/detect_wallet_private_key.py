import re
import argparse
from typing import Optional
from typing import Sequence

WHITELIST = ['mock', 'documentation']

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    filename_pattern = re.compile(r"\.(py|pyx|ts|js)$", re.I)

    private_key_files = []

    for filename in args.filenames:
        # Only scan Python, Cython, Typescript and Javascript files.
        if filename_pattern.search(filename) is None:
            continue
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if re.search("[0-9A-Fa-f]{64}", line):
                    whitelisted = [f"noqa: {allowed}" in line for allowed in WHITELIST]
                    if not any(whitelisted):
                        private_key_files.append(filename)
                        break
                    

    if private_key_files:
        for private_key_file in private_key_files:
            print(f'{private_key_file} contains line(s) that include same pattern as a wallet private key.')
        print('Either remove those line(s) or add a "noqa: {REASON}" tag on such lines.')
        print(f'REASON can be one of the following: {WHITELIST}.')
        return 1
    else:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
