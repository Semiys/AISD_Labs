# Лабораторная работа №3
# 25 Вариант. Формируется матрица F следующим образом: если в Е количество нулей в нечетных столбцах в области 1 больше, 
# чем произведение чисел по периметру области 2, то поменять в В симметрично области 1 и 3 местами, 
# иначе С и Е поменять местами несимметрично. При этом матрица А не меняется. 
# После чего вычисляется выражение: ((К*A T)*(F+А)-K* F T . 
# Выводятся по мере формирования А, F и все матричные операции последовательно.
def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

def fill_matrix(N):
    matrix = [[0]*N for _ in range(N)]
    half = N // 2
    for i in range(N):
        for j in range(N):
            if i < half and j < half:
                matrix[i][j] = 1
            elif i < half and j >= half:
                matrix[i][j] = 2
            elif i >= half and j < half:
                matrix[i][j] = 3
            else:
                matrix[i][j] = 4
    return matrix

def create_matrix_F(A, N):
    F = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if j % 2 == 1 and A[i][j] == 0:
                F[i][j] = A[i][j] + 3
            else:
                F[i][j] = A[i][j] - 1
    return F

def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]

def add_matrices(matrix1, matrix2):
    return [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]

def multiply_matrix_by_number(matrix, number):
    return [[number * matrix[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]

def multiply_matrices(matrix1, matrix2):
    return [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*matrix2)] for X_row in matrix1]

N = int(input("Введите размер матрицы N (кратный 4): "))
K = int(input("Введите число K: "))

A = fill_matrix(N)
F = create_matrix_F(A, N)

A_T = transpose_matrix(A)
F_T = transpose_matrix(F)

K_A_T = multiply_matrix_by_number(A_T, K)
F_plus_A = add_matrices(F, A)
K_F_T = multiply_matrix_by_number(F_T, K)

temp_result = multiply_matrices(K_A_T, F_plus_A)
final_result = add_matrices(temp_result, multiply_matrix_by_number(K_F_T, -1))

print("Матрица A:")
print_matrix(A)

print("\nМатрица F:")
print_matrix(F)

print("\nРезультат выражения ((K*A^T)*(F+A)-K*F^T):")
print_matrix(final_result)
