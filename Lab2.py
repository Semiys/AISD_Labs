import re

digit_to_word = {
    '0': 'ноль',
    '2': 'два',
    '4': 'четыре',
    '6': 'шесть',
    '8': 'восемь',
    'A': 'десять',
    'C': 'двенадцать',
    'E': 'четырнадцать'
}


def proc(match):
    lexeme = match.group()
    try:
        num = int(lexeme, 16)
    except ValueError:
        return lexeme + " не является шестнадцатеричным числом"

    if num % 2 == 0 and num <= 0x400 and lexeme[0] in '13579BDF':
        num_str = ' '.join(digit_to_word.get(digit, digit) for digit in lexeme)
        return lexeme + ': ' + num_str
    else:
        return lexeme + " не удовлетворяет условию задачи"


with open('input.txt', 'r') as f:
    block = f.read(1024)
    if not block:
        print("\nФайл input.txt пустой.\nДобавьте не пустой файл в директорию или переименуйте существующий *.txt файл")
    while block:
        for match in re.finditer(r'\b[0-9A-F]+\b', block, re.IGNORECASE):
            print(proc(match))
        block = f.read(1024)