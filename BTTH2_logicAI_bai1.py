# Các lớp và hàm định nghĩa logic mệnh đề
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

# Hàm phân tích biểu thức logic từ chuỗi
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

# Hàm tính giá trị biểu thức với các giá trị đầu vào
def evaluate_expression(expr_str, assignments):
    try:
        expr = parse_expression(expr_str)
        return expr.evaluate(**assignments)
    except Exception as e:
        return f"Lỗi khi đánh giá biểu thức: {e}"

# Chương trình chính
def main():
    # Nhập biểu thức logic
    expr_str = input("Nhập biểu thức logic (ví dụ: (A ∧ B) → ¬C): ")

    # Phân tích và hiển thị biểu thức
    try:
        expression = parse_expression(expr_str)
        print(f"Biểu thức đã phân tích: {expression}")
    except Exception as e:
        print(f"Lỗi khi phân tích biểu thức: {e}")
        return

    # Nhập các giá trị cho biến logic
    variables = sorted({char for char in expr_str if char.isalpha()})  # Sắp xếp thứ tự chữ cái
    print(f"Các biến trong biểu thức: {variables}")
    assignments = {}
    for var in variables:
        value = input(f"Nhập giá trị cho {var} (True/False): ")
        assignments[var] = value.lower() == "true"

    # Tính giá trị của biểu thức
    result = evaluate_expression(expr_str, assignments)
    print(f"Kết quả biểu thức với giá trị đầu vào {assignments}: {result}")

if __name__ == "__main__":
    main()
