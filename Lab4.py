# Формируется матрица F следующим образом: скопировать в нее А и  если в Е количество нулей в нечетных столбцах больше,
# чем произведение чисел, то поменять в местами  С и В симметрично, иначе С и Е поменять местами несимметрично.
# При этом матрица А не меняется. 
# После чего если определитель матрицы А больше суммы диагональных элементов матрицы F,
# то вычисляется выражение: A-1*AT – K * F-1, иначе вычисляется выражение (A +G-FТ)*K, 
# где G-нижняя треугольная матрица, полученная из А. 
# Выводятся по мере формирования А, F и все матричные операции последовательно.
import numpy as np
import matplotlib.pyplot as plt

def create_submatrix(size):
    return np.random.randint(-10, 11, size=(size, size))

def create_matrix_F(A, B, C, D, E):
    N = A.shape[0] // 2
    F = A.copy()
    count_zeros = np.sum(E[:, ::2] == 0)
    product_of_numbers = np.prod(E[E != 0])

    if count_zeros > product_of_numbers:

        F[:N, :N], F[N:, N:] = C, B
    else:

        F[:N, :N], F[N:, :N] = E, C

    return F

def plot_matrix(matrix, title):
    plt.matshow(matrix)
    plt.colorbar()
    plt.title(title)
    plt.show()

def main():
    K = int(input("Введите число K: "))
    N = int(input("Введите размер N (четное число): "))

    if N % 2 != 0:
        raise ValueError("N должно быть четным числом.")

    size = N // 2
    B = create_submatrix(size)
    C = create_submatrix(size)
    D = create_submatrix(size)
    E = create_submatrix(size)

    A = np.block([[B, C], [D, E]])
    print("Матрица A:")
    print(A)
    plot_matrix(A, "Матрица A")

    F = create_matrix_F(A, B, C, D, E)
    print("Матрица F:")
    print(F)
    plot_matrix(F, "Матрица F")

    det_A = np.linalg.det(A)
    trace_F = np.trace(F)

    if det_A > trace_F:
        result = np.linalg.inv(A).dot(A.T) - K * np.linalg.inv(F)
    else:
        G = np.tril(A)
        result = (A + G - F.T) * K

    print("Результат:")
    print(result)
    plot_matrix(result, "Результат")

if __name__ == "__main__":
    main()
