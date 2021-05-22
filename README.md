# randsik

![Build Status](https://github.com/travishathaway/randsik/.github/workflows/python-app.yml/badge.svg)

Randsik (random + musik) is a library for generating generative music in Python. In order
to do this, this library relies on writing MIDI files to disk. These MIDI files can then
be imported to a DAW software capable of working with them (e.g. Reaper, Ableton, Reason, Logic, etc.).

## Underlying data types
The library itself relies on some data type primitives for constructing the musical patterns such as
`randsik.Note`, `randsik.Rest` and `randsik.Pattern`. These data types themselves wrap several data types
provided by the the [Mido lirbary](https://mido.readthedocs.io/en/latest/), including `mido.MidiTrack`,
`mido.Message` and `mido.MidiFile`.

## Creating random patterns
In order to generate patterns, the `randsik.generate` function can be used. These function takes
a number of configuration parameters, but it also be called with no paramters to create something
completely random.

Here are a couple examples of invoking this function:

```python
import randsik
pat = randsik.generate(
    note='D4', mode='dorian', octaves=2, measures=2, time_sig='3/4',
    note_lengths=(randsik.QUARTER, randsik.EIGHTH)
)
pat.save('test.mid')
```

The example above will create a two measure long pattern in 3/4 using quarter notes and eighth notes. 
The start note or tone, is "D4" and the musical mode is "dorian". When note and mode are left blank,
they will be chosen randomly.

This is what it sounds like when played with a piano (click link to play audio):

[Listen to audio](https://raw.githubusercontent.com/travishathaway/randsik/master/examples/example_1_audio.mp3)

*Remember that this is random and will change every time.*

The available notes span from C-1 to G9 (please be aware these highs and lows must likely reside outside
the audible range).

The available modes are as follows:

- chromatic (all notes)
- ionian
- dorian
- phrygian
- lydian
- mixolydian
- aeolian
- locrian

More information on musical modes can be found at: [Mode (music)](https://en.wikipedia.org/wiki/Mode_\(music\))

