from src.csp import CSP

if __name__ == "__main__":
    variables = ["X1", "X2", "X3"]

    domains = {
        "X1": [1, 2, 3],
        "X2": [1, 2, 3],
        "X3": [1, 2, 3],
    }

    constraints = [
        (("X1", "X2"), lambda x1, x2: x1 > x2),
        (("X2", "X3"), lambda x2, x3: x2 != x3),
    ]

    csp = CSP(variables, domains, constraints)
    solution = csp.solve()
    print("Solution: ", solution)
