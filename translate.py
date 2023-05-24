from translator import *

if __name__ == '__main__':
    try:
        with open('input.txt', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open('input.txt', encoding='ansi') as file:
            lines = file.readlines()
    new_lines = []
    for line in lines:
        new_lines.append(translate(line, german_and=True))
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)