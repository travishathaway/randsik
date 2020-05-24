# TODO

## 2020-05-21

The big thing that I'm thinking of right now is where to draw the line with this library.
Should it also include a CLI with a full featured, "select your MIDI" out device kind of
thing? Or should it just include this "generate" function and that's it.

I'm thinking of jamming a bunch of stuff in to this library, but the cool thing is that it
will still be fairly modular as the only requirement necessary will be the Mido library.

meh.

### Goals

I want to be able to launch a CLI program that will start sending random MIDI notes to 
the device that I select.

## 2020-05-24

I created an example script that just about does what I'd like it to do.

I think it would be cool though if I could figure out a cool way to manipulate the parameters
in real time. This could be at the very least a config file, and maybe move on to something
more complex like a GUI interface for adjusting the parameters.