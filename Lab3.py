# Вариант 25. Формируется матрица F следующим образом: если в Е количество нулей в нечетных столбцах в области 1 больше,
# чем произведение чисел по периметру области 2, то поменять в В симметрично области 1 и 3 местами,
# иначе С и Е поменять местами несимметрично. При этом матрица А не меняется.
# После чего вычисляется выражение: ((К*A T)*(F+А)-K* F T .
# Выводятся по мере формирования А, F и все матричные операции последовательно.
import random

# Функция для создания матрицы с целенаправленным заполнением для тестирования
def create_test_matrix(N):
    return [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]

# Функция для транспонирования матрицы
def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

# Функция для сложения матриц
def add_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

# Функция для умножения матриц
def multiply_matrices(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

# Функция для умножения матрицы на число
def multiply_matrix_by_constant(K, matrix):
    return [[K * matrix[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]

# Функция для подсчета количества нулей в нечетных столбцах левого треугольника подматрицы E
def count_zeros_in_odd_columns_of_left_triangle(matrix):
    count = 0
    for i in range(len(matrix)):
        for j in range(i + 1):
            if j % 2 == 0 and matrix[i][j] == 0:
                count += 1
    return count

# Функция для вычисления произведения чисел по периметру верхнего треугольника подматрицы E
def product_of_perimeter_of_upper_triangle(matrix):
    size = len(matrix)
    product = 1
   
    for j in range(size - 1):
        product *= matrix[0][j]
  
    for i in range(1, size - 1):
        product *= matrix[i][size - 1]
   
    for i in range(1, size):
        product *= matrix[i][size - i - 1]
    return product

# Функция для формирования матрицы F
def create_matrix_F(A, B, C, D, E):
    F = [row[:] for row in A]  # Копирование матрицы A
    zeros_in_E1 = count_zeros_in_odd_columns_of_left_triangle(E)
    product_of_E2_perimeter = product_of_perimeter_of_upper_triangle(E)

    if zeros_in_E1 > product_of_E2_perimeter:
        
        for i in range(N // 2):
            for j in range(i + 1):
                F[i][j], F[N // 2 + i][N - j - 1] = F[N // 2 + i][N - j - 1], F[i][j]
    else:
        
        for i in range(N // 2):
            for j in range(N // 2):
                F[i][j + N // 2], F[i + N // 2][j] = E[i][j], C[i][j]

    return F


# Вывод матрицы
def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))
    print()


K = int(input("Введите число K: "))
N = int(input("Введите размерность N: "))



A = create_test_matrix(N)
print("Матрица A:")
print_matrix(A)


half = N // 2
B = [row[:half] for row in A[:half]]
C = [row[half:] for row in A[:half]]
D = [row[:half] for row in A[half:]]
E = [row[half:] for row in A[half:]]


F = create_matrix_F(A, B, C, D, E)
print("Матрица F:")
print_matrix(F)


A_T = transpose(A)
F_T = transpose(F)
F_plus_A = add_matrices(F, A)
K_mult_A_T = multiply_matrix_by_constant(K, A_T)
K_mult_F_T = multiply_matrix_by_constant(K, F_T)
expr = add_matrices(multiply_matrices(K_mult_A_T, F_plus_A), K_mult_F_T)

print("Результат выражения ((K * A.T) * (F + A)) - (K * F.T):")
print_matrix(expr)
