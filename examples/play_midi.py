import sys

import randsik
import mido


def main():
    """
    Play a random set of notes
    """
    if len(sys.argv) > 1:
        portname = sys.argv[1]
    else:
        portname = None  # Use default port

    try:
        with mido.open_output(portname, autoreset=True) as port:
            while True:
                pat = randsik.generate(
                    mode='dorian', note='D4',
                    note_lengths=(randsik.QUARTER, )
                )
                pat.play(port, 92)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
