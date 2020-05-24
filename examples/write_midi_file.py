"""
This file contains several example usages of randsik
"""
import randsik


def main():
    """
    These are the various supported use cases for the `randsik.generate` function. The
    `randsik.generate` function returns a `randsik.Pattern` object. This object includes
    a save function which allows you to write the midi file to disc. It takes a file
    name as its primary argument.
    """

    # When called with no argument, generate will select a start note and mode randomly
    # combined with several other default arguments for measures, time_sig and note_lengths
    pat = randsik.generate()
    pat.save('test.mid')

    # To have more control over what kind of pattern the generate function generates, you
    # can pass in a number of arguments include, mode (musical mode), octaves (number of
    # octaves the pattern will span) and others.
    pat = randsik.generate(
        mode='lydian', octaves=1, measures=2, time_sig='4/4',
        note_lengths=(randsik.QUARTER, randsik.EIGHTH)
    )
    pat.save('test.mid')


if __name__ == '__main__':
    main()
