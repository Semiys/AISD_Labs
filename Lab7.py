import tkinter as tk
from tkinter import scrolledtext, ttk
import itertools
import timeit


def generate_menus_alg(fruits, N):
    if N == 0:
        return [[]]
    all_combinations = []
    for m in fruits:
        for rest_of_menu in generate_menus_alg(fruits, N - 1):
            all_combinations.append([m] + rest_of_menu)
    return all_combinations

def generate_menus_func(fruits, N):
    return list(itertools.product(fruits, repeat=N))

def is_valid_menu(menu):
    return all(menu[i] != menu[i + 1] for i in range(len(menu) - 1))

def diversity_score(menu):
    return len(set(menu))

def generate_menus_with_constraints(fruits, N, generator_function):
    all_combinations = generator_function(fruits, N)
    valid_menus = list(filter(is_valid_menu, all_combinations))
    max_diversity = max(map(diversity_score, valid_menus), default=0)
    optimal_menus = [menu for menu in valid_menus if diversity_score(menu) == max_diversity]
    return optimal_menus

# Функция вызываемая при нажатии кнопки
def generate_and_display_menus():
    global menus
    try:
        K = int(entry_k.get())
    except ValueError:
        text_area.insert(tk.INSERT, "Пожалуйста, введите целое число для K.\n")
        return  # Прерываем выполнение функции, если ввод невалиден
    N = 7  # Количество фруктов в меню (на неделю)
    fruits = [f'ф{i+1}' for i in range(K)]
    selected_method = method_var.get()

    # Очистка текстового поля
    text_area.delete('1.0', tk.END)

    # Выбор метода генерации
    if selected_method == 'Алгоритмический':
        generator_function = generate_menus_alg
    elif selected_method == 'Функциональный':
        generator_function = generate_menus_func
    else:
        generator_function = None

    # Генерация меню
    start_time = timeit.default_timer()
    if generator_function is not None:
        menus = generator_function(fruits, N)
    else:
        if selected_method == 'Строго ограниченный':
            menus = generate_strictly_optimal_menus(fruits, N, generate_menus_alg)
        elif selected_method == 'Сбалансированный':
            menus = generate_balanced_menus(fruits, N, generate_menus_func)
    time_taken = timeit.default_timer() - start_time

    # Генерация меню с ограничениями, если выбран один из первых двух методов
    if generator_function is not None:
        start_time_constraints = timeit.default_timer()
        optimal_menus = generate_menus_with_constraints(fruits, N, generator_function)
        time_constraints_taken = timeit.default_timer() - start_time_constraints
    else:
        optimal_menus = menus  # Если выбран строго ограниченный или сбалансированный метод
        time_constraints_taken = time_taken

    # Вывод результатов
    text_area.insert(tk.INSERT, f"Метод: {selected_method}\n")
    text_area.insert(tk.INSERT, f"Сгенерировано {len(menus)} меню.\n")
    text_area.insert(tk.INSERT, f"Время выполнения: {time_taken:.6f} секунд\n\n")
    text_area.insert(tk.INSERT, f"Сгенерировано {len(optimal_menus)} оптимальных меню с ограничениями.\n")
    text_area.insert(tk.INSERT, f"Время выполнения с ограничениями: {time_constraints_taken:.6f} секунд\n")





def generate_strictly_optimal_menus(fruits, N, generator_function):
    all_combinations = generator_function(fruits, N)
    # Здесь вы должны применить свои строгие ограничения
    # Для примера, я просто возвращаю все комбинации
    return all_combinations

def generate_balanced_menus(fruits, N, generator_function):
    all_combinations = generator_function(fruits, N)
    # Здесь вы должны применить свои балансированные ограничения
    # Для примера, я просто возвращаю все комбинации
    return all_combinations
# Создание основного окна
root = tk.Tk()
root.title("Генератор меню полдника")

# Определение стилей
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TButton', background='#FF5733', foreground='black', font=('Helvetica', 12, 'bold'))
style.configure('TEntry', font=('Helvetica', 12))

# Создание фреймов для разделения интерфейса
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(padx=10, pady=10, fill='x', expand=True)

output_frame = tk.Frame(root, padx=10, pady=10)
output_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Ввод количества фруктов K
label_k = ttk.Label(input_frame, text="Введите общее количество различных фруктов (K):")
label_k.pack(side='left', padx=5, pady=5)

entry_k = ttk.Entry(input_frame, width=30)
entry_k.pack(side='left', padx=5, pady=5)

# Выбор метода генерации
method_var = tk.StringVar()
method_label = ttk.Label(input_frame, text="Выберите метод генерации:")
method_label.pack(side='left', padx=5, pady=5)

method_dropdown = ttk.Combobox(input_frame, textvariable=method_var, values=[
    'Алгоритмический',
    'Функциональный',
    'Строго ограниченный',
    'Сбалансированный'
], state="readonly", width=20)
method_dropdown.pack(side='left', padx=5, pady=5)
method_dropdown.current(0)

# Кнопка для генерации меню
generate_button = ttk.Button(input_frame, text="Сгенерировать меню", command=generate_and_display_menus)
generate_button.pack(side='left', padx=5, pady=5)

# Текстовое поле с прокруткой для отображения результатов
text_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=('Helvetica', 12), width=60, height=10)
text_area.pack(padx=10, pady=10, fill='both', expand=True)

# Запуск главного цикла Tkinter
root.mainloop()
