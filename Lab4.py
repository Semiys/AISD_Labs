import numpy as np
from matplotlib import pyplot as plt


n = int(input("Введите размер матрицы N : "))
while n < 6:
    n = int(input("Введите размер: "))
k = int(input("Введите коэффициент K: "))

# Создание матрицы A
A = np.random.randint(-10, 11, size=(n, n))
F = A.copy()
print("Матрица A:\n", A, "\n")


# Вспомогательные функции для вывода матрицы
def print_mat(mat, description):
    plt.matshow(mat, cmap='inferno')
    plt.title(description)
    plt.colorbar()
    plt.show()
def print_mat1(mat, description):
    plt.figure(figsize=(10, 4))
    plt.plot(mat[0, :], 'o-', color='purple')
    plt.title(description)
    plt.xlabel('Индекс столбца')
    plt.ylabel('Значение элемента')
    plt.grid(True)
    plt.show()
def print_mat2(F, description):

    column_sums = np.sum(F, axis=0)
    plt.bar(range(len(column_sums)), column_sums)
    plt.title('Столбчатая диаграмма сумм значений столбцов матрицы F')
    plt.xlabel('Индекс столбца')
    plt.ylabel('Сумма значений')
    plt.show()
def print_mat3(F, description):
    column_sums = np.sum(np.abs(F), axis=0)
    labels = [f'Столбец {i + 1}' for i in range(F.shape[1])]
    plt.pie(column_sums, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(description)
    plt.show()
# Функция для подсчета количества нулей в нечетных столбцах матрицы
def count_zeros_in_odd_columns(mat):
    return np.sum(mat[:, 1::2] == 0)


# Функция для подсчета произведения чисел в матрице
def product_of_elements(mat):
    return np.prod(mat[mat != 0])


# Функция для формирования матрицы F
def form_matrix_F(A, B, C, D, E):
    size = len(A) // 2
    zeros = count_zeros_in_odd_columns(E)
    product = product_of_elements(E)

    # Определение, какие подматрицы менять местами
    if zeros > product:

        B, C = np.fliplr(C), np.fliplr(B)
    else:

        C, E = E, C

    # Формирование матрицы F из подматриц
    F[:size, :size] = B
    F[:size, size:] = C
    F[size:, :size] = D
    F[size:, size:] = E
    return F


# Деление матрицы A на подматрицы B, C, D, E
size = n // 2
B, C, D, E = A[:size, :size], A[:size, size:], A[size:, :size], A[size:, size:]


print_mat(A, "Матрица A")
print_mat(B, "Матрица B")
print_mat(C, "Матрица C")
print_mat(D, "Матрица D")
print_mat(E, "Матрица E")

# Формирование матрицы F
F = form_matrix_F(A, B, C, D, E)
print("Матрица F после перестановки:\n", F, "\n")
print_mat(F, "Матрица F")
print_mat1(F, "Матрица F")
print_mat2(F, "Матрица F")
print_mat3(F, "Матрица F")

# Вычисление результата в зависимости от условия
if np.linalg.det(A) > np.trace(F):
    result = np.linalg.inv(A).dot(A.T) - k * np.linalg.inv(F)
else:
    G = np.tril(A)
    result = (A + G - F.T) * k

# Вывод итоговой матрицы
print("Результат:\n", result)
print_mat(result, "Результат")
