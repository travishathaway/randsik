# TODO

## 2020-05-21

The big thing that I'm thinking of right now is where to draw the line with this library. Should it also include a CLI
with a full featured, "select your MIDI" out device kind of thing? Or should it just include this "generate" function
and that's it.

I'm thinking of jamming a bunch of stuff in to this library, but the cool thing is that it will still be fairly modular
as the only requirement necessary will be the Mido library.

meh.

### Goals

I want to be able to launch a CLI program that will start sending random MIDI notes to the device that I select.

## 2020-05-24

I created an example script that just about does what I'd like it to do.

I think it would be cool though if I could figure out a cool way to manipulate the parameters in real time. This could
be at the very least a config file, and maybe move on to something more complex like a GUI interface for adjusting the
parameters.

```
track1 = [intro, verse, chorus, verse, chorus, bridge, verse, outro]
track2 = [intro, verse, chorus, verse, chorus, bridge, verse, outro]


track = [
]
```

## 2022-01-15

I ran into this error recently with some drum tracks I created myself:

```commandline
OSError: running status without last_status
```

Luckily it only affected two files so I'm concerned about it right now, but it may be worth it to test for these errors
in the future. An easy way to do this is by executing the following:

```python
from mido import MidiFile

m1 = MidiFile('path/to/midi/file.mid')
```

This should immediately raise the error.

## 2022-01-16

A problem I'm having right now is dealing with multiple sections where there may not be the same instruments. This is
super typical in music. The intro of a song may have just bass, drums and piano and then subsequent sections would add
others parts (e.g. guitar or synth). This is something I'd like to be able to support with the song builder.

```
G = Guitar, B = Bass, S = Synth, D = Drums, P = Piano

| Section 1 | Section 2 | Section 3 | Section 4 |
|-----------|-----------|-----------|-----------|
|    G      |     G     |    G      |           |
|    B      |     B     |    B      |     B     |
|    D      |     D     |    D      |     D     |
|           |     P     |    P      |           |
|           |     S     |    S      |     S     | 
```
