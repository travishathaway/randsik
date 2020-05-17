import random
from dataclasses import dataclass
from typing import Union, Iterable, AnyStr

from mido import Message, MidiFile, MidiTrack

NOTES = (
    ('A',),
    ('A#', 'Bb'),
    ('B', 'Cb'),
    ('C', 'B#'),
    ('C#', 'Db'),
    ('D',),
    ('D#', 'Eb'),
    ('E', 'Fb'),
    ('F', 'E#'),
    ('F#', 'Gb'),
    ('G',),
    ('G#', 'Ab'),
)

OCTAVES = (-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

ACCIDENTAL_SHARP = '#'
ACCIDENTAL_FLAT = 'b'

MIDI_NOTES = 128


def note_midi_map() -> dict:
    """Generates a list note to midi value mapping"""
    note_map = {}
    counter = -3

    for ock in OCTAVES:
        for ltrs in NOTES:
            if len(ltrs) == 1:
                key = f'{ltrs[0]}{ock}'
                note_map[key] = counter
            else:
                key_0 = f'{ltrs[0]}{ock}'
                key_1 = f'{ltrs[1]}{ock}'
                note_map[key_0] = counter
                note_map[key_1] = counter

            counter += 1

    return {x: y for x, y in note_map.items() if 127 >= y >= 0}


NOTE_MIDI_MAP = note_midi_map()


@dataclass
class Note:
    """
    Represents a single note to played
    """
    value: str
    velocity: int
    duration: int

    def __post_init__(self):
        """
        Validate the values
        """
        if self.value not in NOTE_MIDI_MAP.keys():
            raise ValueError('Attribute "value" must appear in NOTE_MIDI_MAP')
        if self.velocity > 127 or self.velocity < 0:
            raise ValueError('Attribute "velocity" must be an integer between 0 and 127')
        if self.duration < 0:
            raise ValueError('Attribute "duration" must be a positive integer')


@dataclass
class Rest:
    """
    Represents a rest
    """
    duration: int

    def __post_init__(self):
        """
        Validates the rest object values
        """
        if self.duration < 0:
            raise ValueError('Attribute "duration" must be a positive integer')


def write_note(track, note, rest_val=None) -> None:
    """
    Writes a note to the provided midi track

    :param track: midi track
    :param note: note object
    :param rest_val: how long of a rest to how in ticks per quarter note
    """
    note_val = NOTE_MIDI_MAP[note.value]
    time = rest_val or 0
    track.append(Message('note_on', note=note_val, velocity=note.velocity, time=time))
    track.append(Message('note_off', note=note_val, velocity=note.velocity, time=note.duration))


class Pattern:
    """
    A sequence of chords and notes
    """

    def __init__(self, sequence: Iterable[Union[tuple, Note]],
                 tempo: float = None) -> None:
        self.sequence = sequence
        self.tempo = tempo

    def __repr__(self) -> str:
        return f'Pattern(sequence={self.sequence})'

    def save(self, filename: AnyStr) -> None:
        """
        Renders the current pattern to a file. File can either be passed in as
        a string or file object.

        :param filename: Location to write file to
        """
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        rest_val = None

        for seq in self.sequence:
            if isinstance(seq, tuple):
                for note in seq:
                    write_note(track, note)
            elif isinstance(seq, Note):
                print((track, seq, rest_val))
                write_note(track, seq, rest_val)
                rest_val = None
            elif isinstance(seq, Rest):
                rest_val = seq.duration
                continue

        mid.save(filename)


class Song:
    """
    A collection of patterns, chords and notes
    """

    def __init__(self, *args: Union[Pattern, Note]):
        self.items = args
