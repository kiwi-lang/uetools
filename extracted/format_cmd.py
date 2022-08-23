


def main():

    with open('editor_cmd.txt', 'r') as file:
        for line in file.readlines():

            if ':' not in line:
                if line != '\n':
                    print(line, end='')
                continue

            name, help = line.split(':', maxsplit=1)
            name = name.replace('-', '')
            print(f'{name.lower()}: Optional[bool] = None # {help}', end='')


if __name__ == '__main__':
    main()

