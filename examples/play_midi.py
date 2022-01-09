import sys
import time
import json

import randsik
import mido


def main():
    """
    Play a random set of notes
    """
    if len(sys.argv[1]) > 1:
        config_file = sys.argv[1]
    else:
        print('Please specify config file (json format)')
        sys.exit(1)
    print('Select output to use')
    for idx, output in enumerate(mido.get_output_names(), 1):
        print(f'{idx}: {output}')
    output = input('Output [1]:') or 1

    print(output, type(output))

    try:
        portname = mido.get_output_names()[int(output) - 1]
    except (IndexError, ValueError):
        print('Not found')
        sys.exit(1)
    print('Playing... (Ctrl-C to exit)')

    try:
        with mido.open_output(portname, autoreset=True) as port:
            while True:
                with open(sys.argv[1]) as f:
                    config = json.loads(f.read())
                    pat = randsik.generate(**config['generate'])
                    for msg in pat.track:
                        if isinstance(msg, mido.Message):
                            port.send(msg)
                            time.sleep(config['tempo'])

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
