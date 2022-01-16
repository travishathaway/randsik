import math
import os
import pathlib
import random

from mido import MidiTrack, MidiFile

DRUM_MIDI_FOLDER = pathlib.Path(os.path.dirname(__file__)) / '..' / 'midi' / 'drums'


def select_random_child(path: pathlib.Path) -> pathlib.Path:
    """
    Selects child of the provided Path object. Raises an error if now children found
    """
    folders = list(path.iterdir())
    length = len(folders) - 1
    random_child = folders[random.randint(0, length)]

    if random_child.is_file():
        return random_child
    else:
        return select_random_child(random_child)


def drums(measures: int) -> MidiTrack:
    """
    Returns random drum track to use. Right this is very basic. It will be improved upon.

    TODO: refactor later to reflect different time signatures other than 4/4
    """
    drum_loops = math.ceil(measures / 4)
    drum_track = MidiTrack()

    for _ in range(drum_loops):
        midi_file_name = select_random_child(DRUM_MIDI_FOLDER)
        midi_file = MidiFile(midi_file_name)
        drum_track += midi_file.tracks[0]

    return drum_track
