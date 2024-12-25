from itertools import product

# Lớp đại diện cho các công thức logic
class Formula:
    def evaluate(self, domain, predicates):
        raise NotImplementedError()

class Predicate(Formula):
    def __init__(self, name, variable):
        self.name = name
        self.variable = variable

    def evaluate(self, domain, predicates, assignments):
        func = predicates[self.name]
        value = assignments[self.variable]
        return func(value)

    def __str__(self):
        return f"{self.name}({self.variable})"

class Not(Formula):
    def __init__(self, child):
        self.child = child

    def evaluate(self, domain, predicates, assignments):
        return not self.child.evaluate(domain, predicates, assignments)

    def __str__(self):
        return f"¬{self.child}"

class And(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, domain, predicates, assignments):
        return self.left.evaluate(domain, predicates, assignments) and self.right.evaluate(domain, predicates, assignments)

    def __str__(self):
        return f"({self.left} ∧ {self.right})"

class Or(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, domain, predicates, assignments):
        return self.left.evaluate(domain, predicates, assignments) or self.right.evaluate(domain, predicates, assignments)

    def __str__(self):
        return f"({self.left} ∨ {self.right})"

class Implies(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, domain, predicates, assignments):
        return not self.left.evaluate(domain, predicates, assignments) or self.right.evaluate(domain, predicates, assignments)

    def __str__(self):
        return f"({self.left} → {self.right})"

class ForAll(Formula):
    def __init__(self, variable, child):
        self.variable = variable
        self.child = child

    def evaluate(self, domain, predicates, assignments):
        for value in domain:
            assignments[self.variable] = value
            if not self.child.evaluate(domain, predicates, assignments):
                return False
        return True

    def __str__(self):
        return f"∀{self.variable} {self.child}"

class Exists(Formula):
    def __init__(self, variable, child):
        self.variable = variable
        self.child = child

    def evaluate(self, domain, predicates, assignments):
        for value in domain:
            assignments[self.variable] = value
            if self.child.evaluate(domain, predicates, assignments):
                return True
        return False

    def __str__(self):
        return f"∃{self.variable} {self.child}"

# Hàm phân tích công thức từ chuỗi
def parse_formula(formula_str):
    formula_str = formula_str.replace(" ", "")
    stack = []
    operators = {"¬": Not, "∧": And, "∨": Or, "→": Implies}
    quantifiers = {"∀": ForAll, "∃": Exists}

    i = 0
    while i < len(formula_str):
        if formula_str[i].isalpha() and formula_str[i + 1] == "(":
            j = i + 2
            while formula_str[j] != ")":
                j += 1
            stack.append(Predicate(formula_str[i], formula_str[i + 2:j]))
            i = j
        elif formula_str[i] in operators:
            op = operators[formula_str[i]]
            if formula_str[i] == "¬":
                child = stack.pop()
                stack.append(op(child))
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(op(left, right))
        elif formula_str[i] in quantifiers:
            var = formula_str[i + 1]
            child = stack.pop()
            stack.append(quantifiers[formula_str[i]](var, child))
            i += 1
        elif formula_str[i] == "(" or formula_str[i] == ")":
            pass
        i += 1
    return stack.pop()

# Hàm kiểm tra tính đúng/sai của công thức
def evaluate_formula(formula_str, domain, predicates):
    try:
        formula = parse_formula(formula_str)
        assignments = {}
        return formula.evaluate(domain, predicates, assignments)
    except Exception as e:
        return f"Lỗi khi đánh giá công thức: {e}"

# Chương trình chính
def main():
    formula_str = input("Nhập công thức logic vị từ (ví dụ: ∀x (P(x) → Q(x)) ∧ ∃y P(y)): ")
    domain = eval(input("Nhập miền giá trị (ví dụ: {1, 2, 3}): "))
    predicates = {}
    print("Nhập định nghĩa vị từ (ví dụ: P = lambda x: x > 1):")
    while True:
        predicate_input = input("Nhập tên vị từ và định nghĩa (hoặc bấm Enter để dừng): ")
        if not predicate_input.strip():
            break
        try:
            name, definition = predicate_input.split("=", 1)  # Tách tại dấu '=' đầu tiên
            predicates[name.strip()] = eval(definition.strip())
        except ValueError:
            print("Lỗi: Vui lòng nhập định dạng 'TênVịTừ = ĐịnhNghĩa', ví dụ: P = lambda x: x > 1")
        except Exception as e:
            print(f"Lỗi khi xử lý định nghĩa vị từ: {e}")
    result = evaluate_formula(formula_str, domain, predicates)
    print("Kết quả xác minh công thức:", "Đúng" if result else "Sai")

if __name__ == "__main__":
    main()
