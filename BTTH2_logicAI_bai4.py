from itertools import product

# Các lớp logic mệnh đề (tương tự code trên)
class Proposition:
    def evaluate(self, **assignments):
        raise NotImplementedError()

class Variable(Proposition):
    def __init__(self, name):
        self.name = name

    def evaluate(self, **assignments):
        return assignments[self.name]

    def __str__(self):
        return self.name

class Not(Proposition):
    def __init__(self, child):
        self.child = child

    def evaluate(self, **assignments):
        return not self.child.evaluate(**assignments)

    def __str__(self):
        return f"¬{self.child}"

class And(Proposition):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, **assignments):
        return self.left.evaluate(**assignments) and self.right.evaluate(**assignments)

    def __str__(self):
        return f"({self.left} ∧ {self.right})"

class Or(Proposition):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, **assignments):
        return self.left.evaluate(**assignments) or self.right.evaluate(**assignments)

    def __str__(self):
        return f"({self.left} ∨ {self.right})"

class Implies(Proposition):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, **assignments):
        return not self.left.evaluate(**assignments) or self.right.evaluate(**assignments)

    def __str__(self):
        return f"({self.left} → {self.right})"

# Hàm phân tích biểu thức logic
operators = {"¬": Not, "∧": And, "∨": Or, "→": Implies}

def parse_expression(expr_str):
    expr_str = expr_str.replace(" ", "")
    stack = []

    i = 0
    while i < len(expr_str):
        if expr_str[i].isalpha():
            stack.append(Variable(expr_str[i]))
        elif expr_str[i] in operators:
            op = operators[expr_str[i]]
            if expr_str[i] == "¬":
                operand = stack.pop()
                stack.append(op(operand))
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(op(left, right))
        elif expr_str[i] == "(" or expr_str[i] == ")":
            pass
        i += 1

    return stack.pop()

# Hàm kiểm tra tính hợp lệ của kết luận bằng bảng chân trị
def prove_by_truth_table(premises, conclusion):
    try:
        # Phân tích các mệnh đề và kết luận
        parsed_premises = [parse_expression(p) for p in premises]
        parsed_conclusion = parse_expression(conclusion)
    except Exception as e:
        return f"Lỗi khi phân tích biểu thức: {e}"

    # Tìm tất cả các biến logic
    all_variables = set()
    for p in parsed_premises + [parsed_conclusion]:
        all_variables.update(str(p))
    variables = sorted(all_variables)

    # Tạo tất cả các tổ hợp giá trị True/False
    truth_values = list(product([True, False], repeat=len(variables)))

    # Kiểm tra từng tổ hợp
    for values in truth_values:
        assignments = dict(zip(variables, values))

        # Đánh giá tất cả các mệnh đề
        premises_result = all(p.evaluate(**assignments) for p in parsed_premises)

        # Đánh giá kết luận
        conclusion_result = parsed_conclusion.evaluate(**assignments)

        # Nếu các mệnh đề đúng nhưng kết luận sai => không chứng minh được
        if premises_result and not conclusion_result:
            return "Sai"

    # Nếu không có trường hợp nào mâu thuẫn => chứng minh được
    return "Đúng"

# Hàm kiểm tra bằng phương pháp dẫn chứng phản chứng
def prove_by_resolution(premises, conclusion):
    # Chuyển đổi: premises ∧ ¬conclusion phải dẫn đến mâu thuẫn
    try:
        parsed_premises = [parse_expression(p) for p in premises]
        negated_conclusion = Not(parse_expression(conclusion))
    except Exception as e:
        return f"Lỗi khi phân tích biểu thức: {e}"

    # Tìm tất cả các biến logic
    all_variables = set()
    for p in parsed_premises + [negated_conclusion]:
        all_variables.update(str(p))
    variables = sorted(all_variables)

    # Tạo tất cả các tổ hợp giá trị True/False
    truth_values = list(product([True, False], repeat=len(variables)))

    # Kiểm tra từng tổ hợp
    for values in truth_values:
        assignments = dict(zip(variables, values))

        # Đánh giá tất cả các mệnh đề
        premises_result = all(p.evaluate(**assignments) for p in parsed_premises)
        negated_conclusion_result = negated_conclusion.evaluate(**assignments)

        # Nếu premises ∧ ¬conclusion đúng trong bất kỳ tổ hợp nào => không mâu thuẫn
        if premises_result and negated_conclusion_result:
            return "Sai"

    # Nếu không có tổ hợp nào mà premises ∧ ¬conclusion đúng => chứng minh được
    return "Đúng"

# Chương trình chính
def main():
    print("Chứng minh logic mệnh đề")

    # Nhập các mệnh đề
    premises = input("Nhập các mệnh đề (cách nhau bởi dấu phẩy): ").split(",")
    conclusion = input("Nhập kết luận cần chứng minh: ")

    # Chứng minh bằng bảng chân trị
    truth_table_result = prove_by_truth_table(premises, conclusion)
    print("Chứng minh bằng bảng chân trị:")
    print(f"Kết quả: {truth_table_result}\n")

    # Chứng minh bằng phương pháp dẫn chứng phản chứng
    resolution_result = prove_by_resolution(premises, conclusion)
    print("Chứng minh bằng phương pháp dẫn chứng phản chứng:")
    print(f"Kết quả: {resolution_result}")

if __name__ == "__main__":
    main()
