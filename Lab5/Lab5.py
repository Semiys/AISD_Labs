import timeit
import matplotlib.pyplot as plt
"""
Кэш для значений факториалов
"""
factorial_cache = {0: 1, 1: 1}

"""
Функция вычисляет значение F(n) рекурсивно. Для n > 2 использует предыдущие значения
и кешированный факториал для ускорения вычислений.
"""
def recursive_F(n):
    if n == 1:
        return 4
    elif n == 2:
        return 5
    else:
        return (-1)**n * (recursive_F(n-1) - recursive_F(n-2)) / dynamic_factorial(2*n)

"""
Функция вычисляет факториал числа n без использования кеширования.
"""
def plain_factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

"""
Функция вычисляет значение F(n) итеративно без использования кеширования факториала.
"""
def iterative_F(n):
    if n == 1:
        return 4
    elif n == 2:
        return 5
    else:
        fn_minus_1 = 5
        fn_minus_2 = 4
        fn = 0
        for i in range(3, n + 1):
            fn = (-1)**i * (fn_minus_1 - fn_minus_2) / plain_factorial(2*i)
            fn_minus_2, fn_minus_1 = fn_minus_1, fn
        return fn

"""
Функция вычисляет факториал числа n, используя кеширование для ускорения вычислений.
"""
def dynamic_factorial(n):
    if n not in factorial_cache:
        factorial_cache[n] = n * dynamic_factorial(n-1)
    return factorial_cache[n]

"""
Функция вычисляет значение F(n) итеративно, используя кеширование факториала.
"""
def dynamic_F(n):
    if n == 1:
        return 4
    elif n == 2:
        return 5
    else:
        fn_minus_1 = 5
        fn_minus_2 = 4
        fn = 0
        for i in range(3, n+1):
            fn = (-1)**i * (fn_minus_1 - fn_minus_2) / dynamic_factorial(2*i)
            fn_minus_2, fn_minus_1 = fn_minus_1, fn
        return fn

"""
Функция измеряет время выполнения заданной функции для заданного значения n.
"""
def measure_time(func, n):
    times = timeit.repeat(lambda: func(n), repeat=5, number=1)
    return sum(times) / len(times)
"""
Основной блок кода, где происходит вычисление и построение графиков
"""
n_values = range(1, 10)
recursive_times = []
iterative_times = []
dynamic_times = []

for n in n_values:
    recursive_times.append(measure_time(recursive_F, n))
    iterative_times.append(measure_time(iterative_F, n))
    dynamic_times.append(measure_time(dynamic_F, n))

print(f"{'n':<10}{'Рекурсивное время (с)':<25}{'Итерационное время (с)':<25}{'Динамическое время (с)':<25}")
for i, n in enumerate(n_values):
    print(f"{n:<10}{recursive_times[i]:<25}{iterative_times[i]:<25}{dynamic_times[i]:<25}")

plt.figure(figsize=(10, 5))
plt.plot(n_values, recursive_times, label='Рекурсивно', marker='o')
plt.plot(n_values, iterative_times, label='Итерационно', marker='x')
plt.plot(n_values, dynamic_times, label='Динамическое', marker='^')
plt.xlabel('Значение n')
plt.ylabel('Времение выполнения (секунды)')
plt.legend()
plt.title('Сравнение времени вычисления функции F(n)')
plt.grid(True)
plt.show()