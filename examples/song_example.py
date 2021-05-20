import sys

from mido import MidiFile

from randsik import (
    Note, Pattern, generate, Rest, EIGHTH, QUARTER
)
from randsik.constants import SynthLead


def main():
    """
    These are the various supported use cases for the `randsik.generate` function. The
    `randsik.generate` function returns a `randsik.Pattern` object. This object includes
    a save function which allows you to write the midi file to disc. It takes a file
    name as its primary argument.
    """
    # To have more control over what kind of pattern the generate function generates, you
    # can pass in a number of arguments include, mode (musical mode), octaves (number of
    # octaves the pattern will span) and others.

    four_to_floor = [
        Note(36, 127, EIGHTH),
        Note(36, 127, EIGHTH),
        Note(40, 127, EIGHTH),
        Rest(EIGHTH),
        Note(36, 127, EIGHTH),
        Note(36, 127, EIGHTH),
        Note(40, 127, EIGHTH),
        Rest(EIGHTH),
        Note(36, 127, EIGHTH),
        Rest(EIGHTH),
        Note(40, 127, EIGHTH),
        Rest(EIGHTH),
        Note(36, 127, EIGHTH),
        Rest(EIGHTH),
        Note(40, 127, EIGHTH),
        Rest(EIGHTH),
    ]

    tempo = int(sys.argv[2])

    midi_file = MidiFile(type=2)
    sequence = four_to_floor * 2
    pat1 = Pattern(sequence, program=119, tempo=tempo, channel=9)

    pat2 = generate(
        'F2', mode='ionian', octaves=1, measures=4, time_sig='4/4',
        scale_degrees=(1, 5, 7), tempo=tempo, velocity=50,
        note_lengths=(EIGHTH,), program=SynthLead.LEAD_1_SQUARE
    )

    ## pat3 = randsik.generate(
    ##     'C2', mode='lydian', octaves=1, measures=4, time_sig='4/4',
    ##     note_lengths=(randsik.QUARTER, ), program=96
    ## )
    midi_file.tracks.append(pat1.track)
    midi_file.tracks.append(pat2.track)
    # midi_file.tracks.append(pat3.track)
    midi_file.save(sys.argv[1])


if __name__ == '__main__':
    main()
