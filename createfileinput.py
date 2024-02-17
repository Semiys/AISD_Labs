import random
file = open("input.txt", "w")
odd_digits = ["0","1","2","3","4", "5","6", "7","8", "9","A", "B","C", "D","E", "F"]
while True:
    num = random.randrange(0, 1024, 2)
    hex_num = hex(num)[2:].upper()
    file.write(hex_num + " ")
    file.flush()