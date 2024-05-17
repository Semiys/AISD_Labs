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
import random

"""
Определяем функцию для генерации всех возможных меню (алгоритмический подход)
"""
def generate_menus_alg(fruits, N):
    if N == 0:
        yield []
    else:
        for m in fruits:
            for rest_of_menu in generate_menus_alg(fruits, N - 1):
                if not rest_of_menu or m != rest_of_menu[-1]:
                    yield [m] + rest_of_menu

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
    max_diversity = 0
    optimal_menus = []

    for menu in generator_function(fruits, N):
        if is_valid_menu(menu):
            diversity = diversity_score(menu)
            if diversity > max_diversity:
                max_diversity = diversity
                optimal_menus = [menu]
            elif diversity == max_diversity:
                optimal_menus.append(menu)

    return optimal_menus
def print_menus(title, menus):
    print(f"{title}:")
    sample_menus = random.sample(menus, min(5, len(menus)))
    for menu in sample_menus:
        print(', '.join(menu))
    print(f"Всего меню: {len(menus)}\n")
"""
Запрашиваем у пользователя количество разных фруктов
"""
K = int(input("Введите общее количество различных фруктов (K): "))
"""
Устанавливаем количество фруктов в меню, равное 7 (на неделю)
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


menus_alg = list(generate_menus_alg(fruits, N))
menus_func = generate_menus_func(fruits, N)
print_menus("Меню (алгоритмический подход)", menus_alg)
print_menus("Меню (функциональный подход)", menus_func)


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
max_diversity_alg = max(map(diversity_score, optimal_menus_alg), default=0)
max_diversity_func = max(map(diversity_score, optimal_menus_func), default=0)
print(f"Максимальное разнообразие фруктов в оптимальных меню (алгоритмический подход): {max_diversity_alg}")
print(f"Максимальное разнообразие фруктов в оптимальных меню (функциональный подход): {max_diversity_func}")
print("Пример оптимального меню (алгоритмический подход):", optimal_menus_alg[0] if optimal_menus_alg else "Нет оптимальных меню")
print("Пример оптимального меню (функциональный подход):", optimal_menus_func[0] if optimal_menus_func else "Нет оптимальных меню")
