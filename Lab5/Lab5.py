"""
Задана рекуррентная функция. Область определения функции – натуральные числа.
Написать программу сравнительного вычисления данной функции рекурсивно и итерационно. Определить границы применимости рекурсивного и итерационного подхода.
Результаты сравнительного исследования времени вычисления представить в табличной и графической форме.
F(1) = 4; F(2) = 5; F(n) = (-1)n*(F(n-1)- F(n-2) /(2n)!) при n > 2. 
"""
import timeit
import matplotlib.pyplot as plt

"""
Кэш для хранения вычисленных значений факториалов
"""
cache_F = {1: 4, 2: 5}
"""
Динамическая функция для вычисления F(n)
"""
def dynamic_F(n, k=1, cache=cache_F):
    if n in cache:
        return cache[n]
    else:
        k *= -1
        result = k * ((dynamic_F(n-1, k, cache) - dynamic_F(n-2, k, cache)) / dynamic_factorial(2*n))
        cache[n] = result
        return result

"""
Рекурсивная функция для вычисления факториала
"""
def recursive_factorial(n):
    if n == 0:
        return 1
    else:
        return n * recursive_factorial(n-1)


"""
Динамическая функция для вычисления факториала
"""
def dynamic_factorial(n):
    if n in cache_F:
        return cache_F[n]

    for i in range(2, n + 1):
        cache_F[i] = cache_F[i - 1] * i

    return cache_F[n]
"""
Итеративная функция для вычисления факториала
"""
def iterative_factorial(n):
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

"""
Функция для измерения времени выполнения
"""
def score_time(func, n):
    return timeit.timeit(lambda: func(n), number=1000)

"""
Значения n для которых мы хотим измерить время выполнения
"""
n_values = range(1, 10)
recursive_times = []
iterative_times = []
dynamic_times = []

"""
Измерение времени выполнения для каждого значения n
"""
for n in n_values:
    recursive_times.append(score_time(recursive_factorial, n))
    iterative_times.append(score_time(iterative_factorial, n))
    dynamic_times.append(score_time(dynamic_F, n))

"""
Вывод результатов в табличной форме
"""
print(f"{'n':<10}{'Рекурсивное время (мс)':<25}{'Итерационное время (мс)':<25}{'Динамическое время (мс)':<25}")
for i, n in enumerate(n_values):
    print(f"{n:<10}{recursive_times[i]:<25}{iterative_times[i]:<25}{dynamic_times[i]:<25}")

"""
Построение и вывод графика результатов
"""
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(n_values, recursive_times, label='Рекурсивно', marker='o', linewidth=2)
ax.plot(n_values, iterative_times, label='Итерационно', marker='o', linewidth=2)
ax.plot(n_values, dynamic_times, label='Динамическое', marker='o', linewidth=2)
ax.set_xlabel('n', fontsize=14)
ax.set_ylabel('Время (в миллисекундах)', fontsize=14)
ax.legend(fontsize=12)
ax.set_title('Сравнение времени вычисления функции F(n)', fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=12)
plt.grid(True)
plt.show()
