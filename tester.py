import randsik


def main():
    pat = randsik.generate()
    pat.save('test.midi')


if __name__ == '__main__':
    main()
