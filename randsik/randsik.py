import time
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

MUSIC_MODES = {
    'ionian': (2, 2, 1, 2, 2, 2, 1),
    'dorian': (2, 1, 2, 2, 2, 1, 2),
    'phrygian': (1, 2, 2, 2, 1, 2, 2),
    'lydian': (2, 2, 2, 1, 2, 2, 1),
    'mixolydian': (2, 2, 1, 2, 2, 1, 2),
    'aeolian': (2, 1, 2, 2, 1, 2, 2),
    'locrian': (1, 2, 2, 1, 2, 2, 2)
}

OCTAVES = (-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

ACCIDENTAL_SHARP = '#'
ACCIDENTAL_FLAT = 'b'

MIDI_NOTES = 128

# Standard for the amount of "ticks per beat note"
WHOLE = 1920
HALF = 960
QUARTER = 480
EIGHTH = 240
SIXTEENTH = 120
THIRTYSECOND = 60

NOTE_LENGTHS = (QUARTER, EIGHTH, SIXTEENTH)


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
    value: Union[int, str]
    velocity: int
    duration: int

    def __post_init__(self):
        """
        Validate the values
        """
        if isinstance(self.value, str):
            if self.value not in NOTE_MIDI_MAP.keys():
                raise ValueError('Attribute "value", when str, must appear in NOTE_MIDI_MAP')
        elif isinstance(self.value, int):
            if self.value > 127 or self.value < 0:
                raise ValueError('Attribute "value", when int, must be in range of 0 to 127')
        else:
            raise ValueError('Attribute "value" wrong type. Please set as int or str')
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
    if isinstance(note.value, str):
        note_val = NOTE_MIDI_MAP[note.value]
    else:
        note_val = note.value
    time_l = rest_val or 0
    track.append(Message('note_on', note=note_val, velocity=note.velocity, time=time_l))
    track.append(Message('note_off', note=note_val, velocity=note.velocity, time=note.duration))


class Pattern:
    """
    A sequence of chords and notes
    """

    def __init__(self, sequence: Iterable[Union[tuple, Note]],
                 tempo: float = None) -> None:
        self.sequence = sequence
        self.tempo = tempo

        # build midi track given input
        self._build_midi_track()

    def __repr__(self) -> str:
        return f'Pattern(sequence={self.sequence})'

    def _build_midi_track(self) -> None:
        """
        Builds a midi track given the arguments provided to __init__
        """
        self.mid = MidiFile()
        track = MidiTrack()
        self.mid.tracks.append(track)
        rest_val = None

        for seq in self.sequence:
            if isinstance(seq, tuple):
                for note in seq:
                    write_note(track, note)
            elif isinstance(seq, Note):
                write_note(track, seq, rest_val)
                rest_val = None
            elif isinstance(seq, Rest):
                rest_val = seq.duration
                continue

    def save(self, filename: AnyStr) -> None:
        """
        Renders the current pattern to a file. File can either be passed in as
        a string or file object.

        :param filename: Location to write file to
        """
        self.mid.save(filename)

    def play(self, port, tempo: int) -> None:
        """
        Provided a valid Midi port, send the notes in sequence to that port in real
        time (i.e. however long the current `sequence` is, is how long this will take
        to run.

        :param port: Open Mido Port object
        :param tempo: Speed to play Midi notes
        """
        for seq in self.sequence:
            if isinstance(seq, Note):
                on = Message('note_on', note=seq.value)
                port.send(on)
                time.sleep(pulses_to_seconds(seq.duration, tempo))
                off = Message('note_off', note=seq.value)
                port.send(off)

            elif isinstance(seq, Rest):
                time.sleep(pulses_to_seconds(seq.duration))


def generate(note: str = None, mode: str = None, octaves: int = 1,
             measures: int = 1, time_sig: str = '4/4',
             note_lengths: tuple = (QUARTER, SIXTEENTH, EIGHTH)) -> Pattern:
    """
    Function to generate a random sequence of notes

    :param note: key of pattern, will also determine octave ('C4', 'D3', etc.).
                 if None random note will be selected
    :param mode: which mode to choose from ('ionian', 'mixolydian', 'chromatic').
                 if None random mode will be chosen
    :param octaves: Number of octaves to use (default 1)
    :param measures: Number of measures in given time_sig (default 1)
    :param time_sig: Time signature to use (default '4/4')
    :param note_lengths: Tuple of available note lengths to use for pattern (default (QUARTER,
                         EIGHTH, SIXTEENTH) )
    """
    start_midi_note = None
    if note is None:
        start_midi_note = random.choice(range(40, 80))
    elif note not in NOTE_MIDI_MAP:
        raise ValueError('"note" must be a valid note (e.g. "C4", "A5", etc.)')

    if mode is None:
        mode = random.choice(tuple((MUSIC_MODES.keys())))

    if start_midi_note is None:
        start_midi_note = NOTE_MIDI_MAP[note]
    playable_notes = get_mode_midi_notes(mode, start_midi_note)

    idx = playable_notes.index(start_midi_note)
    end = idx + 12 * octaves
    end_range = end if end < 127 else 127
    note_selection = playable_notes[idx:end_range]

    # Allowed pulses per measure and total pulses for the track
    ppm = time_sig_to_ppm(time_sig)
    total_pulses = ppm * measures

    pattern_notes = []
    current_pulses = 0
    while current_pulses < total_pulses:
        note_val = random.choice(note_selection)
        length = random.choice(note_lengths)

        # Check if we need to trim the last note to fit in the measure
        if length + current_pulses > total_pulses:
            length = length - ((length + current_pulses) - total_pulses)

        pattern_notes.append(
            Note(note_val, 127, length)
        )
        current_pulses += length

    pattern = Pattern(pattern_notes)

    return pattern


def get_mode_midi_notes(mode: str, start_note: int) -> list:
    """
    Provided a mode ("ionian", "mixolydian", "chromatic", etc.) return all playable
    notes in the mode.

    The idea here is that we have two parameters: a mode and a start note. With the mode
    we can figure out the steps (w-w-h-w-w-w-h or 2-2-1-2-2-2-1 for ionian) and
    with the start note we know where to start at.

    The basic algorithm just walks up until reaching the 127th note and walks down until
    reaching 0.

    :param mode: musical mode ("ionian", "mixolydian", etc.)
    :param start_note: starting note (e.g. "C4")

    :return: set of allowable notes to be played
    """
    playable_notes = []

    if mode == 'chromatic':
        return [x for x in range(128)]
    else:
        steps = MUSIC_MODES.get(mode)
        if not steps:
            raise ValueError('Invalid mode supplied')

        # Let's go up first
        current_note = start_note
        broken = False

        while not broken:
            playable_notes.append(current_note)
            for step in steps:
                current_note += step
                if current_note > 127:
                    broken = True
                    break
                playable_notes.append(current_note)

        # Now let's go down
        current_note = start_note
        broken = False

        while not broken:
            for step in reversed(steps):
                current_note -= step
                if current_note < 20:
                    broken = True
                    break
                playable_notes.append(current_note)

    return playable_notes


def time_sig_to_ppm(time_sig) -> int:
    """
    Converts a string time signature to ppm, "pulses per measure".

    More information about this number here:
    - https://en.wikipedia.org/wiki/Pulses_per_quarter_note
    """
    beats_per_bar, beat_unit = time_sig.split('/')

    beats_in_bar = int(beats_per_bar) / int(beat_unit) * 4

    return QUARTER * int(beats_in_bar)


def pulses_to_seconds(pulses: int, tempo: int) -> float:
    """
    This converts pulse values (120 - sixteenth, 240 - eighth, 480 - quarter) to
    second values.

    :param pulses: Number of pulses
    :param tempo: Tempo (beats per minute)

    :return: Length of pulses in seconds
    """
    return (pulses / QUARTER) * (60 / tempo)
