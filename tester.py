import randsik


def main():
    pat = randsik.generate(note='B4', mode='lydian', octaves=1, length=24)
    pat.save('test.midi')


if __name__ == '__main__':
    main()
