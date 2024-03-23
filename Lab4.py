# Вариант 25. Формируется матрица F следующим образом: скопировать в нее А и  если в Е количество нулей в нечетных столбцах больше,
# чем произведение чисел, то поменять в местами  С и В симметрично, иначе С и Е поменять местами несимметрично.
# При этом матрица А не меняется. 
# После чего если определитель матрицы А больше суммы диагональных элементов матрицы F,
# то вычисляется выражение: A-1*AT – K * F-1, иначе вычисляется выражение (A +G-FТ)*K, 
# где G-нижняя треугольная матрица, полученная из А. 
# Выводятся по мере формирования А, F и все матричные операции последовательно.
import numpy as np
from matplotlib import pyplot as plt


n = int(input("Введите размер матрицы N : "))
while n < 6:
    n = int(input("Введите размер матрицы больше 5: "))
k = int(input("Введите коэффициент K: "))

# Создание матрицы A
A = np.random.randint(-10, 11, size=(n, n))
F = A.copy()
print("Матрица A:\n", A, "\n")


# Вспомогательная функция для вывода матрицы
def print_mat(mat, description):
    plt.matshow(mat)
    plt.title(description)
    plt.colorbar()
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

# Вычисление результата в зависимости от условия
if np.linalg.det(A) > np.trace(F):
    result = np.linalg.inv(A).dot(A.T) - k * np.linalg.inv(F)
else:
    G = np.tril(A)
    result = (A + G - F.T) * k

# Вывод итоговой матрицы
print("Результат:\n", result)
print_mat(result, "Результат")
