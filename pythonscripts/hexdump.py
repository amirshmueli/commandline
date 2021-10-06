def main():
    try:
        d = input()
        i = 0
        while True:
            for b in d:
                if i == 4:
                    print('\n')
                    i = 0
                if type(b) == str:
                    b = b.encode()
                print(b.hex(), end=' ')
                i += 1
            d = input()
    except Exception as e:
        pass
    print()


main()