import random
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Union

from mido import Message, MetaMessage, MidiTrack, bpm2tempo

from randsik import constants as const


class RandsikValidationError(Exception):
    pass


@dataclass
class Note:
    """
    Represents a single note to played
    """
    value: int
    velocity: int
    duration: int

    def __post_init__(self):
        """
        Validate the values
        """
        self._validate_velocity()
        self._validate_duration()

    def _validate_velocity(self):
        if self.velocity not in tuple(range(128)):
            raise RandsikValidationError(
                'Attribute "velocity" must be an integer between 0 and 127'
            )

    def _validate_duration(self):
        if self.duration < 0:
            raise RandsikValidationError('Attribute "duration" must be a positive integer')


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
            raise RandsikValidationError('Attribute "duration" must be a positive integer')


def write_note(track: MidiTrack, note: Note, rest_val: Union[Rest, None] = None, channel: int = 0) -> None:
    """
    Writes a note to the provided midi track

    :param track: track to write to
    :param note: note to add to track
    :param rest_val: how long of a rest to how in ticks per quarter note
    :param channel: which channel it takes on MIDI file (possible values 0..15)
    """
    if isinstance(note.value, str):
        note_val = const.NOTE_MIDI_MAP[note.value]
    else:
        note_val = note.value
    time_l = rest_val or 0
    track.append(
        Message(
            "note_on",
            note=note_val,
            velocity=note.velocity,
            time=time_l,
            channel=channel,
        )
    )
    track.append(
        Message(
            "note_off",
            note=note_val,
            velocity=note.velocity,
            time=note.duration,
            channel=channel,
        )
    )


class Pattern:
    """
    A sequence of chords and notes
    """

    track: MidiTrack
    sequence: Iterable[Union[tuple, Note]]
    tempo: float
    program: int
    channel: int

    def __init__(
            self,
            sequence: Iterable[Union[tuple, Note, Rest]],
            tempo: float = 120,
            program: int = 1,
            channel: int = 0,
    ) -> None:
        """
        creates a pattern and attaches it to the provided `midi_file` object.

        For more information on values for `program` see:
            https://en.wikipedia.org/wiki/General_MIDI#Piano
        """
        self.track = MidiTrack()
        self.sequence = sequence
        self.tempo = tempo
        self.program = program  # this controls the instrument
        self.channel = channel

        # build midi track given input
        self._build_midi_track()

    def __repr__(self) -> str:
        return f"Pattern(sequence={self.sequence})"

    def __iter__(self):
        """Iterate over internal `sequence` property"""

    def _build_midi_track(self) -> None:
        """
        Builds a midi track given the arguments provided to __init__
        """
        self.track.append(
            Message("program_change", program=self.program - 1, channel=self.channel)
        )
        self.track.append(MetaMessage("set_tempo", tempo=bpm2tempo(self.tempo)))
        rest_val = None

        for seq in self.sequence:
            if isinstance(seq, tuple):
                for note in seq:
                    write_note(self.track, note, channel=self.channel)
            elif isinstance(seq, Note):
                write_note(self.track, seq, rest_val, channel=self.channel)
                rest_val = None
            elif isinstance(seq, Rest):
                rest_val = seq.duration
                continue


def generate(
        note: str = None,
        mode: str = None,
        octaves: int = 1,
        measures: int = 1,
        time_sig: str = "4/4",
        scale_degrees=None,
        program: const.Instrument = const.Piano.ACOUSTIC_GRAND_PIANO,
        tempo: int = 120,
        velocity: int = 127,
        channel: int = 0,
        note_lengths: Sequence = (const.QUARTER, const.SIXTEENTH, const.EIGHTH),
) -> Pattern:
    """
    Function to generate a random sequence of notes

    :param note: key of pattern, will also determine octave ('C4', 'D3', etc.).
                 if None random note will be selected
    :param mode: which mode to choose from ('ionian', 'mixolydian', 'chromatic').
                 if None random mode will be chosen
    :param octaves: Number of octaves to use (default 1)
    :param measures: Number of measures in given time_sig (default 1)
    :param time_sig: Time signature to use (default '4/4')
    :param program: This is the instrument or program number
        (see: https://en.wikipedia.org/wiki/General_MIDI#Piano)
    :param tempo: tempo in BPM for pattern
    :param velocity: velocity for the notes in the pattern
    :param channel: channel in the MIDI this pattern will occupy
    :param note_lengths: Tuple of available note lengths to use for pattern (default (QUARTER,
                         EIGHTH, SIXTEENTH) )
    :param scale_degrees: Scale degrees a random pattern can use (e.g. 1, 3, 5)
    """
    start_midi_note = None
    if note is None:
        start_midi_note = random.choice(range(40, 80))
    elif note not in const.NOTE_MIDI_MAP:
        raise ValueError('"note" must be a valid note (e.g. "C4", "A5", etc.)')

    if mode is None:
        mode = random.choice(tuple((const.MUSIC_MODES.keys())))

    if start_midi_note is None:
        start_midi_note = const.NOTE_MIDI_MAP[note]
    playable_notes = get_mode_midi_notes(mode, start_midi_note)

    idx = playable_notes.index(start_midi_note)
    end = idx + 12 * octaves
    end_range = end if end < 127 else 127
    note_selection = playable_notes[idx:end_range]

    # This will limit selection to provided scale degrees (e.g. 1, 3, 5, 7)
    if scale_degrees:
        note_selection = [note_selection[x] for x in scale_degrees]

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

        pattern_notes.append(Note(note_val, duration=length, velocity=velocity))
        current_pulses += length

    pattern = Pattern(pattern_notes, program=program, tempo=tempo, channel=channel)

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

    if mode == "chromatic":
        return [x for x in range(128)]
    else:
        steps = const.MUSIC_MODES.get(mode)
        if not steps:
            raise ValueError("Invalid mode supplied")

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
    beats_per_bar, beat_unit = time_sig.split("/")

    beats_in_bar = int(beats_per_bar) / int(beat_unit) * 4

    return const.QUARTER * int(beats_in_bar)


def pulses_to_seconds(pulses: int, tempo: int) -> float:
    """
    This converts pulse values (120 - sixteenth, 240 - eighth, 480 - quarter) to
    second values.

    :param pulses: Number of pulses
    :param tempo: Tempo (beats per minute)

    :return: Length of pulses in seconds
    """
    return (pulses / const.QUARTER) * (60 / tempo)
