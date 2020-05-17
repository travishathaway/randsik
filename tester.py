from pprint import pprint
from randsik import randsik


WHOLE = 480  # Standard for the amount of "ticks per quarter note"
QUARTER = 240
EIGHTH = 120
SIXTEENTH = 60


def main():
    pattern = (
        randsik.Note('C4', 127, SIXTEENTH),
        randsik.Rest(SIXTEENTH),
        randsik.Note('C5', 127, SIXTEENTH),
        randsik.Rest(SIXTEENTH),
        randsik.Note('C4', 127, SIXTEENTH),
        randsik.Rest(SIXTEENTH),
        randsik.Note('C5', 127, SIXTEENTH),
        randsik.Rest(SIXTEENTH),
        randsik.Note('C4', 127, SIXTEENTH),
        randsik.Rest(SIXTEENTH),
        randsik.Note('C5', 127, SIXTEENTH),
        randsik.Rest(SIXTEENTH),
        randsik.Note('C4', 127, SIXTEENTH),
        randsik.Rest(SIXTEENTH),
        randsik.Note('C5', 127, SIXTEENTH),
        randsik.Rest(SIXTEENTH),
    )

    pat = randsik.Pattern(pattern, tempo=120)

    pat.save('test.midi')


if __name__ == '__main__':
    main()
