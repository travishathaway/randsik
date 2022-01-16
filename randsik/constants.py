from enum import IntEnum

NOTES = (
    ("A",),
    ("A#", "Bb"),
    ("B", "Cb"),
    ("C", "B#"),
    ("C#", "Db"),
    ("D",),
    ("D#", "Eb"),
    ("E", "Fb"),
    ("F", "E#"),
    ("F#", "Gb"),
    ("G",),
    ("G#", "Ab"),
)

MUSIC_MODES = {
    "ionian": (2, 2, 1, 2, 2, 2, 1),
    "dorian": (2, 1, 2, 2, 2, 1, 2),
    "phrygian": (1, 2, 2, 2, 1, 2, 2),
    "lydian": (2, 2, 2, 1, 2, 2, 1),
    "mixolydian": (2, 2, 1, 2, 2, 1, 2),
    "aeolian": (2, 1, 2, 2, 1, 2, 2),
    "locrian": (1, 2, 2, 1, 2, 2, 2),
}

OCTAVES = (-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

ACCIDENTAL_SHARP = "#"
ACCIDENTAL_FLAT = "b"

MIDI_NOTES = 128

# Standard for the amount of "ticks per beat note"
WHOLE: int = 1920
HALF: int = 960
QUARTER: int = 480
EIGHTH: int = 240
SIXTEENTH: int = 120
THIRTYSECOND: int = 60

NOTE_LENGTHS = (QUARTER, EIGHTH, SIXTEENTH)


def note_midi_map() -> dict:
    """Generates a list note to midi value mapping"""
    note_map = {}
    counter = -3

    for ock in OCTAVES:
        for ltrs in NOTES:
            if len(ltrs) == 1:
                key = f"{ltrs[0]}{ock}"
                note_map[key] = counter
            else:
                key_0 = f"{ltrs[0]}{ock}"
                key_1 = f"{ltrs[1]}{ock}"
                note_map[key_0] = counter
                note_map[key_1] = counter

            counter += 1

    return {x: y for x, y in note_map.items() if 127 >= y >= 0}


NOTE_MIDI_MAP = note_midi_map()


# Instrument Groups


class Instrument(IntEnum):
    pass


class Piano(Instrument):
    ACOUSTIC_GRAND_PIANO = 1
    BRIGHT_ACOUSTIC_PIANO = 2
    ELECTRIC_GRAND_PIANO = 3
    HONKY_TONK_PIANO = 4
    ELECTRIC_PIANO_1 = 5
    ELECTRIC_PIANO_2 = 6
    HARPSICHORD = 7
    CLAVI = 8


class ChromaticPercussion(Instrument):
    CELESTA = 9
    GLOCKENSPIEL = 10
    MUSIC_BOX = 11
    VIBRAPHONE = 12
    MARIMBA = 13
    XYLOPHONE = 14
    TUBULAR_BELLS = 15
    DULCIMER = 16


class Organ(Instrument):
    DRAWBAR_ORGAN = 17
    PERCUSSIVE_ORGAN = 18
    ROCK_ORGAN = 19
    CHURCH_ORGAN = 20
    REED_ORGAN = 21
    ACCORDION = 22
    HARMONICA = 23
    TANGO_ACCORDION = 24


class Guitar(Instrument):
    ACOUSTIC_GUITAR_NYLON = 25
    ACOUSTIC_GUITAR_STEEL = 26
    ELECTRIC_GUITAR_JAZZ = 27
    ELECTRIC_GUITAR_CLEAN = 28
    ELECTRIC_GUITAR_MUTED = 29
    OVERDRIVEN_GUITAR = 30
    DISTORTION_GUITAR = 31
    GUITAR_HARMONICS = 32


class Bass(Instrument):
    ACOUSTIC_BASS = 33
    ELECTRIC_BASS_FINGER = 34
    ELECTRIC_BASS_PICK = 35
    FRETLESS_BASS = 36
    SLAP_BASS_1 = 37
    SLAP_BASS_2 = 38
    SYNTH_BASS_1 = 39
    SYNTH_BASS_2 = 40


class Strings(Instrument):
    VIOLIN = 41
    VIOLA = 42
    CELLO = 43
    CONTRABASS = 44
    TREMOLO_STRINGS = 45
    PIZZICATO_STRINGS = 46
    ORCHESTRAL_HARP = 47
    TIMPANI = 48


class Ensemble(Instrument):
    STRING_ENSEMBLE_1 = 49
    STRING_ENSEMBLE_2 = 50
    SYNTH_STRINGS_1 = 51
    SYNTH_STRINGS_2 = 52
    CHOIR_AAHS = 53
    VOICE_OOHS = 54
    SYNTH_VOICE = 55
    ORCHESTRA_HIT = 56


class Brass(Instrument):
    TRUMPET = 57
    TROMBONE = 58
    TUBA = 59
    MUTED_TRUMPET = 60
    FRENCH_HORN = 61
    BRASS_SECTION = 62
    SYNTH_BRASS_1 = 63
    SYNTH_BRASS_2 = 64


class Reed(Instrument):
    SOPRANO_SAX = 65
    ALTO_SAX = 66
    TENOR_SAX = 67
    BARITONE_SAX = 68
    OBOE = 69
    ENGLISH_HORN = 70
    BASSOON = 71
    CLARINET = 72


class Pipe(Instrument):
    PICCOLO = 73
    FLUTE = 74
    RECORDER = 75
    PAN_FLUTE = 76
    BLOWN_BOTTLE = 77
    SHAKUHACHI = 78
    WHISTLE = 79
    OCARINA = 80


class SynthLead(Instrument):
    LEAD_1_SQUARE = 81
    LEAD_2_SAWTOOTH = 82
    LEAD_3_CALLIOPE = 83
    LEAD_4_CHIFF = 84
    LEAD_5_CHARANG = 85
    LEAD_6_VOICE = 86
    LEAD_7_FIFTHS = 87
    LEAD_8_BASS_LEAD = 88


class SynthPad(Instrument):
    PAD_1_NEW_AGE = 89
    PAD_2_WARM = 90
    PAD_3_POLYSYNTH = 91
    PAD_4_CHOIR = 92
    PAD_5_BOWED = 93
    PAD_6_METALLIC = 94
    PAD_7_HALO = 95
    PAD_8_SWEEP = 96


class SynthEffects(Instrument):
    FX_1_RAIN = 97
    FX_2_SOUNDTRACK = 98
    FX_3_CRYSTAL = 99
    FX_4_ATMOSPHERE = 100
    FX_5_BRIGHTNESS = 101
    FX_6_GOBLINS = 102
    FX_7_ECHOES = 103
    FX_8_SCI_FI = 104


class Ethnic(Instrument):
    SITAR = 105
    BANJO = 106
    SHAMISEN = 107
    KOTO = 108
    KALIMBA = 109
    BAG_PIPE = 110
    FIDDLE = 111
    SHANAI = 112


class Percussive(Instrument):
    TINKLE_BELL = 113
    AGOGO = 114
    STEEL_DRUMS = 115
    WOODBLOCK = 116
    TAIKO_DRUM = 117
    MELODIC_TOM = 118
    SYNTH_DRUM = 119
    REVERSE_CYMBAL = 120


class SoundEffects(Instrument):
    GUITAR_FRET_NOISE = 121
    BREATH_NOISE = 122
    SEASHORE = 123
    BIRD_TWEET = 124
    TELEPHONE_RING = 125
    HELICOPTER = 126
    APPLAUSE = 127
    GUNSHOT = 128


ALL_INSTRUMENTS = (
    Piano,
    ChromaticPercussion,
    Organ,
    Guitar,
    Bass,
    Strings,
    Ensemble,
    Brass,
    Reed,
    Pipe,
    SynthLead,
    SynthPad,
    SynthEffects,
    Ethnic,
    Percussive,
    SoundEffects,
)

INT_TO_INSTRUMENT = {
    i.value: i
    for inst in ALL_INSTRUMENTS
    for i in inst
}


class Drums(Instrument):
    HIGH_Q = 27
    SLAP = 28
    SCRATCH_PUSH = 29
    SCRATCH_PULL = 30
    STICKS = 31
    SQUARE_CLICK = 32
    METRONOME_CLICK = 33
    METRONOME_BELL = 34
    ACOUSTIC_BASS_DRUM = 35
    ELECTRIC_BASS_DRUM = 36
    SIDE_STICK = 37
    ACOUSTIC_SNARE = 38
    HAND_CLAP = 39
    ELECTRIC_SNARE = 40
    LOW_FLOOR_TOM = 41
    CLOSED_HI_HAT = 42
    HIGH_FLOOR_TOM = 43
    PEDAL_HI_HAT = 44
    LOW_TOM = 45
    OPEN_HI_HAT = 46
    LOW_MID_TOM = 47
    HI_MID_TOM = 48
    CRASH_CYMBAL_1 = 49
    HIGH_TOM = 50
    RIDE_CYMBAL_1 = 51
    CHINESE_CYMBAL = 52
    RIDE_BELL = 53
    TAMBOURINE = 54
    SPLASH_CYMBAL = 55
    COWBELL = 56
    CRASH_CYMBAL_2 = 57
    VIBRA_SLAP = 58
    RIDE_CYMBAL_2 = 59
    HIGH_BONGO = 60
    LOW_BONGO = 61
    MUTE_HIGH_CONGA = 62
    OPEN_HIGH_CONGA = 63
    LOW_CONGA = 64
    HIGH_TIMBALE = 65
    LOW_TIMBALE = 66
    HIGH_AGOGO = 67
    LOW_AGOGO = 68
    CABASA = 69
    MARACAS = 70
    SHORT_WHISTLE = 71
    LONG_WHISTLE = 72
    SHORT_GUIRO = 73
    LONG_GUIRO = 74
    CLAVES = 75
    HIGH_WOODBLOCK = 76
    LOW_WOODBLOCK = 77
    MUTE_CUICA = 78
    OPEN_CUICA = 79
    MUTE_TRIANGLE = 80
    OPEN_TRIANGLE = 81
    SHAKER = 82
    JINGLE_BELL = 83
    BELLTREE = 84
    CASTANETS = 85
    MUTE_SURDO = 86
    OPEN_SURDO = 87
