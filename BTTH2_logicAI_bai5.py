import itertools

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

def parse_expression(expr_str):
    expr_str = expr_str.replace(" ", "")  # Xóa khoảng trắng
    stack = []
    operators = {"¬": Not, "∧": And, "∨": Or, "→": Implies}

    i = 0
    while i < len(expr_str):
        if expr_str[i].isalpha():  # Biến logic (A, B, C, ...)
            stack.append(Variable(expr_str[i]))
        elif expr_str[i] in operators:  # Toán tử logic
            op = operators[expr_str[i]]
            if expr_str[i] == "¬":  # Toán tử một ngôi
                operand = stack.pop()
                stack.append(op(operand))
            else:  # Toán tử hai ngôi
                right = stack.pop()
                left = stack.pop()
                stack.append(op(left, right))
        elif expr_str[i] == "(" or expr_str[i] == ")":
            pass  # Bỏ qua dấu ngoặc (đã xử lý trong chuỗi)
        i += 1
    return stack.pop()

def find_model(expr_str):
    try:
        expression = parse_expression(expr_str)
    except Exception as e:
        return f"Lỗi khi phân tích biểu thức: {e}"

    variables = sorted({char for char in expr_str if char.isalpha()})

    for values in itertools.product([False, True], repeat=len(variables)):
        assignments = dict(zip(variables, values))
        if expression.evaluate(**assignments):
            return assignments

    return "Không có mẫu giá trị nào thỏa mãn."

def main():
    expr_str = input("Nhập biểu thức logic (ví dụ: (A ∨ B) ∧ (¬A ∨ C)): ")

    result = find_model(expr_str)
    if isinstance(result, dict):
        print(f"Mẫu giá trị thỏa mãn: {result}")
    else:
        print(result)

if __name__ == "__main__":
    main()
