from typing import List, Tuple

Matrix = List[List[float]]

# 유틸
def pretty_print(A: Matrix, precision: int = 6, name: str | None = None):
    if name:
        print(f"\n{name}:")
    for row in A:
        print("  [ " + "  ".join(f"{x:.{precision}f}" for x in row) + " ]")

def is_square(A: Matrix) -> bool:
    return len(A) > 0 and all(len(row) == len(A) for row in A)

def deep_copy(A: Matrix) -> Matrix:
    return [row[:] for row in A]

def matrices_equal(A: Matrix, B: Matrix, tol: float = 1e-8) -> bool:
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False
    n, m = len(A), len(A[0])
    for i in range(n):
        for j in range(m):
            if abs(A[i][j] - B[i][j]) > tol:
                return False
    return True

# 입력 
def read_matrix_from_user() -> Matrix:
    
    while True:
        try:
            n = int(input("정방행렬의 크기 n을 입력하세요 : ").strip())
            if n <= 0:
                print("n은 양의 정수여야 합니다. 다시 입력하세요.")
                continue
            break
        except ValueError:
            print("정수를 입력해주세요.")
    A: Matrix = []
    print(f"{n}×{n} 행렬의 각 행을 공백으로 구분해 입력하세요.")
    for i in range(n):
        while True:
            row_str = input(f"{i+1}번째 행: ").strip()
            try:
                row = [float(x) for x in row_str.split()]
                if len(row) != n:
                    print(f"{n}개의 숫자를 입력해야 합니다. 다시 입력하세요.")
                    continue
                A.append(row)
                break
            except ValueError:
                print("실수(또는 정수)를 공백으로 구분하여 입력하세요.")
    return A

# 행렬식(det) & 여인자(adj)
def minor(A: Matrix, r: int, c: int) -> Matrix:
    """A의 (r,c) 원소를 제외한 소행렬"""
    return [row[:c] + row[c+1:] for i, row in enumerate(A) if i != r]

def determinant(A: Matrix) -> float:
    """여인자 전개(재귀)로 det(A) 계산"""
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    # 간단한 행 스왑/스케일링 최적화 없이 첫 행 기준 전개
    det = 0.0
    for j in range(n):
        cofactor = ((-1) ** (0 + j)) * A[0][j] * determinant(minor(A, 0, j))
        det += cofactor
    return det

def adjugate(A: Matrix) -> Matrix:
    """수반행렬 adj(A)"""
    n = len(A)
    if n == 1:
        return [[1.0]]
    Cof = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            Cof[i][j] = ((-1) ** (i + j)) * determinant(minor(A, i, j))
    # 전치
    Adj = [[Cof[j][i] for j in range(n)] for i in range(n)]
    return Adj

def inverse_via_determinant(A: Matrix) -> Tuple[Matrix, float]:
    """행렬식/수반행렬을 이용한 역행렬."""
    if not is_square(A):
        raise ValueError("정방행렬이 아닙니다.")
    detA = determinant(A)
    if abs(detA) < 1e-12:
        raise ValueError("역행렬이 존재하지 않습니다 (det(A)=0).")
    Adj = adjugate(A)
    n = len(A)
    inv = [[Adj[i][j] / detA for j in range(n)] for i in range(n)]
    return inv, detA

# 가우스-조던 소거법 
def inverse_via_gauss_jordan(A: Matrix) -> Matrix:
    """가우스-조던 소거법(부분 피벗팅)으로 역행렬 계산"""
    if not is_square(A):
        raise ValueError("정방행렬이 아닙니다.")
    n = len(A)
    # 확장행렬 [A | I]
    M = [A[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    # 소거
    for col in range(n):
        # 부분 피벗팅: col열에서 절댓값 최대 행 탐색
        pivot_row = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot_row][col]) < 1e-12:
            raise ValueError("역행렬이 존재하지 않습니다 (특이행렬).")
        # 현재 행과 피벗 행 교환
        if pivot_row != col:
            M[col], M[pivot_row] = M[pivot_row], M[col]

        # 피벗을 1로 만듦
        pivot = M[col][col]
        for j in range(2*n):
            M[col][j] /= pivot

        # 다른 모든 행의 col열을 0으로
        for r in range(n):
            if r == col:
                continue
            factor = M[r][col]
            if abs(factor) > 0:
                for j in range(2*n):
                    M[r][j] -= factor * M[col][j]

    inv = [row[n:] for row in M]
    return inv

def main():
    print("=== n×n 정방행렬 역행렬 계산기 (행렬식 & 가우스-조던) ===")
    A = read_matrix_from_user()
    pretty_print(A, name="입력 행렬 A")

    # 1) 행렬식 기반
    try:
        inv_det, detA = inverse_via_determinant(A)
        print(f"\n[행렬식 기반] det(A) = {detA:.12f}")
        pretty_print(inv_det, name="A^{-1} (행렬식/수반행렬)")
    except ValueError as e:
        print(f"\n[행렬식 기반] 오류: {e}")
        inv_det = None

    # 2) 가우스-조던 기반
    try:
        inv_gj = inverse_via_gauss_jordan(A)
        pretty_print(inv_gj, name="A^{-1} (가우스-조던)")
    except ValueError as e:
        print(f"\n[가우스-조던 기반] 오류: {e}")
        inv_gj = None

    # 3) 결과 비교
    if inv_det is not None and inv_gj is not None:
        same = matrices_equal(inv_det, inv_gj, tol=1e-8)
        print("\n[비교 결과]")
        if same:
            print("두 방법으로 계산한 역행렬이 허용 오차 내에서 동일합니다.")
        else:
            print("두 방법의 결과가 다릅니다.")

if __name__ == "__main__":
    main()
