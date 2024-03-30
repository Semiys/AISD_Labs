# Вариант 25. Формируется матрица F следующим образом: если в Е количество нулей в нечетных столбцах в области 1 больше,
# чем произведение чисел по периметру области 2, то поменять в В симметрично области 1 и 3 местами,
# иначе С и Е поменять местами несимметрично. При этом матрица А не меняется.
# После чего вычисляется выражение: ((К*A T)*(F+А)-K* F T .
# Выводятся по мере формирования А, F и все матричные операции последовательно.
import random

def create_matrix(n):
    return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))
    print()

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def add_matrices(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def multiply_matrix_by_number(matrix, number):
    return [[number * matrix[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]

def count_zeros_in_odd_columns_in_area1(matrix):
    count = 0
    n = len(matrix)
    for i in range(n//2):
        for j in range(i):
            if matrix[i][j] == 0:
                count += 1
    for i in range(n//2, n):
        for j in range(n - (i + 1)):
            if matrix[i][j] == 0:
                count += 1
    return count

def product_of_elements_in_area2(matrix):
    product = 1
    n = len(matrix)
    for i in range(n//2):
        for j in range(n//2, n):
            product *= matrix[i][j]
    return product

def swap_symmetrically_areas_1_and_3(matrix):
    n = len(matrix)
    for i in range(n//2):
        for j in range(i):
            matrix[i][j], matrix[n-j-1][n-i-1] = matrix[n-j-1][n-i-1], matrix[i][j]

def swap_matrices_c_and_e(c, e):
    return e, c



K = int(input("Введите K: "))
N = int(input("Введите N: "))


A = create_matrix(N)
B = [row[:N//2] for row in A[:N//2]]
C = [row[N//2:] for row in A[:N//2]]
D = [row[:N//2] for row in A[N//2:]]
E = [row[N//2:] for row in A[N//2:]]

print("Матрица A:")
print_matrix(A)


def form_matrix_f(b, c, d, e, condition):
    n = len(b) * 2
    f = [[0] * n for _ in range(n)]
    if condition:

        for i in range(n//2):
            f[i][:n//2] = b[i]
            f[i + n//2][:n//2] = d[i]

        for i in range(n//2):
            f[i][n//2:] = c[i]
            f[i + n//2][n//2:] = e[i]
    else:

        for i in range(n//2):
            f[i][:n//2] = b[i]
            f[i + n//2][:n//2] = d[i]

        for i in range(n//2):
            f[i][n//2:] = e[i]
            f[i + n//2][n//2:] = c[i]
    return f



zeros_in_E = count_zeros_in_odd_columns_in_area1(E)
product_in_E = product_of_elements_in_area2(E)

condition = zeros_in_E > product_in_E
if condition:
    swap_symmetrically_areas_1_and_3(B)
F = form_matrix_f(B, C, D, E, condition)

print("Матрица F:")
print_matrix(F)


AT = transpose(A)
F_plus_A = add_matrices(F, A)
F_transposed = transpose(F)

expr = add_matrices(multiply_matrix_by_number(AT, K), F_plus_A)
expr = add_matrices(expr, multiply_matrix_by_number(F_transposed, -K))

print("Результат:")
print_matrix(expr)
