import randsik


def main():
    pat = randsik.generate(
        mode='lydian', octaves=1, measures=2, time_sig='4/4',
        note_lengths=(randsik.QUARTER, randsik.THIRTYSECOND)
    )
    pat.save('test.midi')


if __name__ == '__main__':
    main()
