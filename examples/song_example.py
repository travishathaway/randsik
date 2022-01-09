import sys

from mido import MidiFile

from randsik import (
    Note, Pattern, generate, Rest, EIGHTH, QUARTER, HALF, SIXTEENTH, WHOLE
)
from randsik.constants import SynthLead, Bass, Drums, Strings


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

    four_to_the_floor = [
        Note(Drums.ACOUSTIC_BASS_DRUM, 127, EIGHTH),
        Rest(EIGHTH),
        Note(Drums.ACOUSTIC_SNARE, 127, EIGHTH),
        Rest(EIGHTH),
        Note(Drums.ACOUSTIC_BASS_DRUM, 127, EIGHTH),
        Rest(EIGHTH),
        Note(Drums.ACOUSTIC_SNARE, 127, EIGHTH),
        Rest(EIGHTH),
        Note(Drums.ACOUSTIC_BASS_DRUM, 127, EIGHTH),
        Note(Drums.ACOUSTIC_BASS_DRUM, 127, EIGHTH),
        Note(Drums.ACOUSTIC_SNARE, 127, EIGHTH),
        Rest(EIGHTH),
        Note(Drums.ACOUSTIC_BASS_DRUM, 127, EIGHTH),
        Rest(EIGHTH),
        Note(Drums.ACOUSTIC_SNARE, 127, EIGHTH),
        Note(Drums.ACOUSTIC_SNARE, 127, EIGHTH),
    ]

    tempo = int(sys.argv[2])
    mode = 'mixolydian'
    key = 'A'

    midi_file = MidiFile(type=2)
    sequence = four_to_the_floor * 2

    pat1 = Pattern(sequence, program=119, tempo=tempo, channel=9)

    pat2 = generate(
        f'{key}3', mode=mode, octaves=2, measures=4, time_sig='4/4',
        scale_degrees=(1, 5, 7, 8, 11), tempo=tempo, velocity=60, channel=2,
        note_lengths=(EIGHTH, SIXTEENTH,), program=SynthLead.LEAD_7_FIFTHS
    )

    pat3 = generate(
        f'{key}2', mode=mode, octaves=1, measures=4, time_sig='4/4', tempo=tempo,
        scale_degrees=(1, 5, 6, 7), channel=0,
        note_lengths=(HALF, ), program=Bass.ACOUSTIC_BASS, velocity=100
    )

    pat4 = generate(
        f'{key}5', mode=mode, octaves=2, measures=4, time_sig='4/4', tempo=tempo,
        scale_degrees=(3, 7, 8), channel=1,
        note_lengths=(HALF, WHOLE), program=Strings.VIOLIN, velocity=100
    )

    midi_file.tracks.append(pat1.track)
    midi_file.tracks.append(pat2.track)
    midi_file.tracks.append(pat3.track)
    # midi_file.tracks.append(pat4.track)

    midi_file.save(sys.argv[1])


if __name__ == '__main__':
    main()
