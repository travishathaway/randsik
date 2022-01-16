import sys

from randsik import constants as con
from randsik.song_builder.song import SongSection, create_song


def main():
    """
    In this example, the create_song function from the song_builder module is used.
    This function accepts a tuple of SongSection config objects. The drum patterns
    are selected manually from patterns available in `randsik/midi/drums`.

    This function writes a randomly named midi file to the current directory.
    """
    if len(sys.argv) < 2:
        print('Please supply file name')
        sys.exit(1)

    sect_1_instruments = (
        con.Bass.SYNTH_BASS_1,
        con.SynthPad.PAD_5_BOWED
    )
    sect_2_instruments = (
        con.Bass.SYNTH_BASS_1,
        con.Guitar.OVERDRIVEN_GUITAR,
        con.Piano.BRIGHT_ACOUSTIC_PIANO
    )

    mode = 'dorian'
    tempo = 92
    key = 'D3'
    octaves = 1

    sect_1 = SongSection(
        measures=4, mode=mode, tempo=tempo, key=key, octaves=octaves, instruments=sect_1_instruments
    )
    sect_2 = SongSection(
        measures=4, mode=mode, tempo=tempo, key=key, octaves=octaves, instruments=sect_2_instruments
    )

    song_file = create_song((sect_1, sect_2))

    with open(sys.argv[1], 'wb') as fp:
        song_file.save(file=fp)


if __name__ == '__main__':
    main()
