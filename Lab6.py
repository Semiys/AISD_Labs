"""
Задание состоит из двух частей.
1 часть – написать программу в соответствии со своим вариантом задания.
Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.
2 часть – усложнить написанную программу,
введя по своему усмотрению в условие минимум одно ограничение на характеристики объектов (которое будет сокращать количество переборов)
и целевую функцию для нахождения оптимального  решения.
Вариант 25. У няни неограниченное количество  фруктов К разных названий (ф1,…фК).
Сформировать (вывести) все возможные варианты меню полдника (N фруктов) для ребенка на неделю.

"""
import itertools
import timeit

"""
Определяем функцию для генерации всех возможных меню (алгоритмический подход)
"""
def generate_menus_alg(fruits, N):
    if N == 0:
        return [[]]
    all_combinations = []
    for m in fruits:
        for rest_of_menu in generate_menus_alg(fruits, N - 1):
            all_combinations.append([m] + rest_of_menu)
    return all_combinations

"""
Определяем функцию для генерации всех возможных меню (функциональный подход с использованием itertools)
"""
def generate_menus_func(fruits, N):
    return list(itertools.product(fruits, repeat=N))

"""
Функция для проверки, что в меню нет одинаковых фруктов подряд
"""
def is_valid_menu(menu):
    return all(menu[i] != menu[i + 1] for i in range(len(menu) - 1))

"""
Функция для расчета количества уникальных фруктов
"""
def diversity_score(menu):
    return len(set(menu))

"""
Функция для генерации меню с учетом ограничений и оптимизации
"""
def generate_menus_with_constraints(fruits, N, generator_function):
    all_combinations = generator_function(fruits, N)
    valid_menus = list(filter(is_valid_menu, all_combinations))
    max_diversity = max(map(diversity_score, valid_menus), default=0)
    optimal_menus = [menu for menu in valid_menus if diversity_score(menu) == max_diversity]
    return optimal_menus

"""
Запрашиваем у пользователя количество разных фруктов
"""
K = int(input("Введите общее количество различных фруктов (K): "))
"""
Устанавливаем количество фруктов в меню, равное 7 (на неделю)ё
"""
N = 7
fruits = [f'ф{i+1}' for i in range(K)]


alg_time = timeit.timeit(lambda: generate_menus_alg(fruits, N), number=1)


func_time = timeit.timeit(lambda: generate_menus_func(fruits, N), number=1)


alg_time_with_constraints = timeit.timeit(
    lambda: generate_menus_with_constraints(fruits, N, generate_menus_alg),
    number=1
)


func_time_with_constraints = timeit.timeit(
    lambda: generate_menus_with_constraints(fruits, N, generate_menus_func),
    number=1
)


menus_alg = generate_menus_alg(fruits, N)
menus_func = generate_menus_func(fruits, N)
optimal_menus_alg = generate_menus_with_constraints(fruits, N, generate_menus_alg)
optimal_menus_func = generate_menus_with_constraints(fruits, N, generate_menus_func)
"""
Вывод результатов
"""
print(f"Алгоритмический подход сгенерировал {len(menus_alg)} меню.")
print(f"Время выполнения: {alg_time:.6f} секунд")
print(f"Функциональный подход сгенерировал {len(menus_func)} меню.")
print(f"Время выполнения: {func_time:.6f} секунд")
print(f"Алгоритмический подход с ограничениями сгенерировал {len(optimal_menus_alg)} оптимальных меню.")
print(f"Время выполнения: {alg_time_with_constraints:.6f} секунд")
print(f"Функциональный подход с ограничениями сгенерировал {len(optimal_menus_func)} оптимальных меню.")
print(f"Время выполнения: {func_time_with_constraints:.6f} секунд")
"""
Проверки
"""
assert len(set(map(tuple, menus_alg))) == len(menus_alg), "Не все алгоритмически сгенерированные меню уникальны."
assert len(set(map(tuple, menus_func))) == len(menus_func), "Не все функционально сгенерированные меню уникальны."
assert all(is_valid_menu(menu) for menu in optimal_menus_alg), "Не все алгоритмические оптимальные меню валидны."
assert all(is_valid_menu(menu) for menu in optimal_menus_func), "Не все функциональные оптимальные меню валидны."
