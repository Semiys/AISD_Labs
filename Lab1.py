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

with open('input.txt', 'r') as f:
    block = f.read(1024)
    if not block:
        print("\nФайл input.txt пустой.\nДобавьте не пустой файл в директорию или переименуйте существующий *.txt файл")
    while block:
        lexemes = block.split()
        for lexeme in lexemes:
            try:
                num = int(lexeme, 16)
            except ValueError:
                print(" не является шестнадцатеричным числом")
                continue
            if num % 2 == 0 and num <= 0x400 and lexeme[0] in '13579BDF':
                num_str = ''
                for digit in lexeme:
                    if digit in digit_to_word:
                        num_str += digit_to_word[digit] + ' '
                    else:
                        num_str += digit + ' '
                print(lexeme + ': ' + num_str)
            else:
                print(" не удовлетворяет условию задачи")
        block = f.read(1024)