# 집합 A = {1,2,3,4,5} 에 대한 관계 행렬 프로그램

def input_relation_matrix(n=5):
    """
    n x n 관계 행렬을 사용자로부터 입력받는다.
    각 행마다 0 또는 1을 공백으로 구분하여 n개 입력.
    """
    print(f"{n}x{n} 관계 행렬을 입력하세요 (0 또는 1, 공백으로 구분):")
    mat = []
    for i in range(n):
        while True:
            line = input(f"{i+1}번째 행: ")
            try:
                row = list(map(int, line.split()))
                if len(row) != n or any(x not in (0, 1) for x in row):
                    raise ValueError
                mat.append(row)
                break
            except ValueError:
                print("입력이 잘못되었습니다. 0 또는 1을 공백으로 구분해", n, "개 입력하세요.")
    return mat


def print_matrix(mat, A=None):
    """
    관계 행렬을 보기 좋게 출력
    """
    n = len(mat)
    if A is None:
        A = list(range(1, n + 1))

    print("    ", end="")
    for j in range(n):
        print(f"{A[j]:>2}", end=" ")
    print()
    print("   " + "---" * n)
    for i in range(n):
        print(f"{A[i]:>2}|", end=" ")
        for j in range(n):
            print(f"{mat[i][j]:>2}", end=" ")
        print()
    print()


#새로 추가된 기능: 관계를 쌍 집합 형태로 출력

def relation_to_pairs(mat, A=None):
    """
    관계 행렬을 {(a_i, a_j)} 형태의 쌍 집합으로 변환하여 리스트로 반환.
    mat[i][j] == 1 이면 (A[i], A[j]) 를 포함.
    """
    n = len(mat)
    if A is None:
        A = list(range(1, n + 1))

    pairs = []
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 1:
                pairs.append((A[i], A[j]))
    return pairs


def print_relation_pairs(mat, A=None):
    """
    관계를 R = { (1,1), (1,3), ... } 형태로 출력
    """
    pairs = relation_to_pairs(mat, A)
    print("R = { ", end="")
    pair_strs = [f"({a}, {b})" for (a, b) in pairs]
    print(", ".join(pair_strs), end=" ")
    print("}")


#동치 관계 관련 함수들

def is_reflexive(mat):
    """
    반사성: 모든 i에 대해 (i,i) ∈ R 인지 검사
    """
    n = len(mat)
    for i in range(n):
        if mat[i][i] != 1:
            return False
    return True


def is_symmetric(mat):
    """
    대칭성: (i,j) ∈ R 이면 (j,i) ∈ R 인지 검사
    """
    n = len(mat)
    for i in range(n):
        for j in range(i + 1, n):
            if mat[i][j] != mat[j][i]:
                return False
    return True


def is_transitive(mat):
    """
    추이성: (i,j) ∈ R, (j,k) ∈ R 이면 (i,k) ∈ R 인지 검사
    """
    n = len(mat)
    for i in range(n):
        for j in range(n):
            if mat[i][j]:
                for k in range(n):
                    if mat[j][k] and not mat[i][k]:
                        return False
    return True


def is_equivalence(mat):
    """
    동치 관계인지 (반사, 대칭, 추이 모두 만족하는지) 검사
    """
    return is_reflexive(mat) and is_symmetric(mat) and is_transitive(mat)


def equivalence_classes(mat, A=None):
    """
    각 원소에 대한 동치류를 리스트로 계산
    [i] = { j | (i,j) ∈ R }
    """
    n = len(mat)
    if A is None:
        A = list(range(1, n + 1))

    classes = []
    for i in range(n):
        eq_class = [A[j] for j in range(n) if mat[i][j] == 1]
        classes.append(eq_class)
    return classes


def print_equivalence_classes(mat, A=None):
    """
    동치류를 형식에 맞게 출력
    """
    n = len(mat)
    if A is None:
        A = list(range(1, n + 1))

    classes = equivalence_classes(mat, A)
    for i in range(n):
        print(f"[{A[i]}] = {{ ", end="")
        print(", ".join(map(str, classes[i])), end=" ")
        print("}")


#폐포(closure) 함수들

def reflexive_closure(mat):
    """
    반사 폐포: 모든 (i,i)를 1로 만든다.
    """
    n = len(mat)
    new = [row[:] for row in mat]
    for i in range(n):
        new[i][i] = 1
    return new


def symmetric_closure(mat):
    """
    대칭 폐포: (i,j) 또는 (j,i)가 1이면 둘 다 1로 만든다.
    """
    n = len(mat)
    new = [row[:] for row in mat]
    for i in range(n):
        for j in range(i + 1, n):
            if new[i][j] == 1 or new[j][i] == 1:
                new[i][j] = new[j][i] = 1
    return new


def transitive_closure(mat):
    """
    추이 폐포: Warshall 알고리즘 사용
    new[i][j] = new[i][j] or (new[i][k] and new[k][j])
    """
    n = len(mat)
    new = [row[:] for row in mat]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if new[i][k] and new[k][j]:
                    new[i][j] = 1
    return new


def check_and_print_properties(mat):
    """
    반사/대칭/추이/동치 여부를 한 번에 출력
    """
    r = is_reflexive(mat)
    s = is_symmetric(mat)
    t = is_transitive(mat)

    print("반사적(reflexive):", "예" if r else "아니오")
    print("대칭적(symmetric):", "예" if s else "아니오")
    print("추이적(transitive):", "예" if t else "아니오")
    print("=> 동치 관계:", "맞음" if (r and s and t) else "아님")
    return r, s, t


def main():
    A = [1, 2, 3, 4, 5]
    n = len(A)

    # 1. 관계 행렬 입력
    mat = input_relation_matrix(n)

    print("\n입력한 관계 행렬:")
    print_matrix(mat, A)

    # 추가기능: 관계를 쌍 집합 형태로 출력
    print("입력한 관계의 쌍 집합 표현:")
    print_relation_pairs(mat, A)
    print()

    # 2. 동치 관계 판별
    print("=== 원래 관계의 성질 판별 ===")
    r, s, t = check_and_print_properties(mat)

    if r and s and t:
        print("\n이 관계는 동치 관계입니다.")
        print("동치류는 다음과 같습니다.")
        print_equivalence_classes(mat, A)
    else:
        print("\n이 관계는 동치 관계가 아닙니다.")

    # 4. 각 폐포 계산 및 출력

    # (1) 반사 폐포
    print("\n=== 반사 폐포 (reflexive closure) ===")
    r_cl = reflexive_closure(mat)
    print("변환 전 행렬:")
    print_matrix(mat, A)
    print("변환 후 행렬:")
    print_matrix(r_cl, A)
    print("변환 후 관계의 쌍 집합 표현:")
    print_relation_pairs(r_cl, A)
    print("반사 폐포에 대한 성질 판별:")
    check_and_print_properties(r_cl)
    if is_equivalence(r_cl):
        print("동치류:")
        print_equivalence_classes(r_cl, A)

    # (2) 대칭 폐포
    print("\n=== 대칭 폐포 (symmetric closure) ===")
    s_cl = symmetric_closure(mat)
    print("변환 전 행렬:")
    print_matrix(mat, A)
    print("변환 후 행렬:")
    print_matrix(s_cl, A)
    print("변환 후 관계의 쌍 집합 표현:")
    print_relation_pairs(s_cl, A)
    print("대칭 폐포에 대한 성질 판별:")
    check_and_print_properties(s_cl)
    if is_equivalence(s_cl):
        print("동치류:")
        print_equivalence_classes(s_cl, A)

    # (3) 추이 폐포
    print("\n=== 추이 폐포 (transitive closure) ===")
    t_cl = transitive_closure(mat)
    print("변환 전 행렬:")
    print_matrix(mat, A)
    print("변환 후 행렬:")
    print_matrix(t_cl, A)
    print("변환 후 관계의 쌍 집합 표현:")
    print_relation_pairs(t_cl, A)
    print("추이 폐포에 대한 성질 판별:")
    check_and_print_properties(t_cl)
    if is_equivalence(t_cl):
        print("동치류:")
        print_equivalence_classes(t_cl, A)


if __name__ == "__main__":
    main()
