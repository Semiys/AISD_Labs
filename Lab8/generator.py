import random

"""Список имен менеджеров для генерации данных"""
managers = ['Алиса', 'Сергей', 'Дмитрий', 'Диана', 'Иван', 'Олег', 'Мария', 'Анна']

"""Функция для генерации случайных данных о кредитных договорах"""
def generate_contracts(filename, num_contracts=100):
    with open(filename, 'w') as file:
        for i in range(num_contracts):
            contract_id = f"C{i:04d}"
            amount = random.uniform(1000, 105000)
            manager = random.choice(managers)
            file.write(f"{contract_id},{amount:.2f},{manager}\n")

"""Генерация файла с данными о кредитных договорах"""
generate_contracts('contracts.txt')
