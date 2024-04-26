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
import time
"""
Определение функции для генерации меню с использованием алгоритмического подхода.
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
Определение функции для генерации меню с использованием функционального подхода.
"""
def generate_menus_func(fruits, N):
    return list(itertools.product(fruits, repeat=N))

"""
Определение функции для проверки, что меню является допустимым (не содержит соседних одинаковых фруктов).
"""
def is_valid_menu(menu):
    return all(menu[i] != menu[i + 1] for i in range(len(menu) - 1))

"""
Определение функции для расчета "разнообразия" меню, т.е. количества уникальных фруктов в нем.
"""
def diversity_score(menu):
    return len(set(menu))

"""
Определение функции для генерации меню с учетом ограничений.
"""
def generate_menus_with_constraints(fruits, N, generator_function):
    all_combinations = generator_function(fruits, N)
    valid_menus = list(filter(is_valid_menu, all_combinations))
    max_diversity = max(map(diversity_score, valid_menus), default=0)
    optimal_menus = [menu for menu in valid_menus if diversity_score(menu) == max_diversity]
    return optimal_menus
"""
Определение переменных для количества фруктов и размера меню.
"""
K = 10
N = 7
fruits = [f'ф{i+1}' for i in range(K)]
"""
Измерение времени выполнения алгоритмического подхода.
"""
start_time = time.time()
menus_alg = generate_menus_alg(fruits, N)
alg_time = time.time() - start_time
"""
Измерение времени выполнения функционального подхода.
"""
start_time = time.time()
menus_func = generate_menus_func(fruits, N)
func_time = time.time() - start_time
"""
Измерение времени выполнения алгоритмического подхода с учетом ограничений.
"""
start_time = time.time()
optimal_menus_alg = generate_menus_with_constraints(fruits, N, generate_menus_alg)
alg_time_with_constraints = time.time() - start_time
"""
Измерение времени выполнения функционального подхода с учетом ограничений.
"""
start_time = time.time()
optimal_menus_func = generate_menus_with_constraints(fruits, N, generate_menus_func)
func_time_with_constraints = time.time() - start_time
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
Проверка уникальности сгенерированных меню.
"""
assert len(set(map(tuple, menus_alg))) == len(menus_alg)
assert len(set(map(tuple, menus_func))) == len(menus_func)
assert all(is_valid_menu(menu) for menu in optimal_menus_alg)
assert all(is_valid_menu(menu) for menu in optimal_menus_func)

if optimal_menus_alg:
    print("Пример оптимального меню (алгоритмический подход):", optimal_menus_alg[0])
else:
    print("Не найдено ни одного оптимального меню (алгоритмический подход).")

if optimal_menus_func:
    print("Пример оптимального меню (функциональный подход):", optimal_menus_func[0])
else:
    print("Не найдено ни одного оптимального меню (функциональный подход).")
