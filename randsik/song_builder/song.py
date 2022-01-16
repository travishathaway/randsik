import random
from collections import defaultdict
from collections.abc import Sequence, Mapping, Iterator
from dataclasses import dataclass

from mido import MidiFile, MidiTrack

from randsik import constants as con
from randsik import generate, Pattern, Note
from randsik.song_builder.drums import drums

Instrument_Seq = Sequence[con.Instrument]


@dataclass(frozen=True)
class SongSection:
    __slots__ = ('measures', 'mode', 'tempo', 'key', 'octaves', 'instruments')
    measures: int
    mode: str
    tempo: int
    key: str
    octaves: int
    instruments: Instrument_Seq


Section_Seq = Sequence[SongSection]


def get_random_scale_degrees(octaves: int) -> Sequence[int]:
    num_notes = random.randint(2, octaves * 7)

    return tuple(random.randint(1, octaves * 7) for _ in range(num_notes))


def get_random_note_lengths() -> Sequence[int]:
    note_lengths = (con.QUARTER, con.EIGHTH, con.WHOLE, con.HALF, con.SIXTEENTH, con.THIRTYSECOND)
    length = len(note_lengths)

    return tuple(random.choices(note_lengths, k=random.randint(2, length)))


def get_section_instrument_map(sections: Section_Seq) -> Mapping[con.Instrument, list[bool]]:
    """
    Returns a mapping showing all the instruments in the song based on the provided section and
    whether the instrument is in that section.
    """
    instrument_map = defaultdict(list)
    instruments = {i for sect in sections for i in sect.instruments}

    for inst in instruments:
        for sect in sections:
            instrument_map[inst].append(inst in sect.instruments)

    return instrument_map


def get_rest_measures(measures: int, instrument: con.Instrument, tempo: int, channel: int) -> Pattern:
    """
    Returns a pattern with whole notes for every measure.
    The notes have a 0 velocity and therefore should not be audible.
    These are the messages sent when the instrument is not playing.

    TODO: This feels a little hacky. It might be worth it to come back and change.
    """
    sequence = [Note(velocity=1, duration=con.WHOLE, value=1)] * measures
    pattern = Pattern(sequence, program=instrument.value, tempo=tempo, channel=channel)

    return pattern


def create_song(sections: Section_Seq) -> MidiFile:
    """
    Function that returns a song based on the passed in configuration.
    """
    midi_file = MidiFile()
    instrument_map = get_section_instrument_map(sections)

    for idx, (instrument, incl_sect) in enumerate(instrument_map.items()):
        midi_file.tracks.append(track(instrument, idx, zip(incl_sect, sections)))

    measures = sum(sect.measures for sect in sections)
    midi_file.tracks.append(drums(measures))

    return midi_file


def track(inst: con.Instrument, channel: int, sections: Iterator) -> MidiTrack:
    """
    Returns a randomly programmed track.
    """
    full_track = MidiTrack()

    for include, section in sections:
        if include is False:
            pattern = get_rest_measures(section.measures, inst, section.tempo, channel)
        else:
            note_lengths = get_random_note_lengths()
            pattern = generate(
                section.key,
                mode=section.mode,
                octaves=section.octaves,
                measures=section.measures,
                time_sig='4/4',
                tempo=section.tempo,
                scale_degrees=get_random_scale_degrees(section.octaves),
                channel=channel,
                note_lengths=note_lengths,
                program=inst,
                velocity=80
            )
        full_track += pattern.track

    return full_track
