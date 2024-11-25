from collections import defaultdict
from typing import Callable


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, list[int]],
        constraints: list[tuple[tuple[str, ...], Callable]],
    ) -> None:
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.neighbors = defaultdict(list)
        self._build_neighbors()

    def _build_neighbors(self) -> None:
        """Будує граф обмежень для кожної змінної."""
        for vars_, _ in self.constraints:
            for var in vars_:
                self.neighbors[var].extend([v for v in vars_ if v != var])

    def is_consistent(self, var, value, assignment) -> bool:
        """Перевіряє, чи значення змінної узгоджене з поточним присвоєнням.
        
        Returns
        -------
        bool
            True if assignment is consisten with its value.
        """
        assignment[var] = value
        for vars_, condition in self.constraints:
            if var in vars_:
                values = [assignment.get(v, None) for v in vars_]
                if None not in values and not condition(*values):
                    del assignment[var]
                    return False
        del assignment[var]
        return True

    def select_unassigned_variable(self, assignment):
        """Вибирає наступну змінну за евристиками MRV і Degree."""
        unassigned = [v for v in self.variables if v not in assignment]
        # Евристика MRV
        min_domain_vars = sorted(unassigned, key=lambda v: len(self.domains[v]))
        # Евристика Degree
        return max(min_domain_vars, key=lambda v: len(self.neighbors[v]))

    def order_domain_values(self, var, assignment):
        """Сортує значення для змінної за найменш обмежувальним значенням."""

        def conflicts(value) -> int:
            assignment[var] = value
            count = 0
            for neighbor in self.neighbors[var]:
                if neighbor not in assignment:
                    count += sum(
                        not self.is_consistent(neighbor, val, assignment)
                        for val in self.domains[neighbor]
                    )
            del assignment[var]
            return count

        return sorted(self.domains[var], key=conflicts)

    def backtrack(self, assignment) -> dict[str, float] | None:
        """Алгоритм пошуку з поверненням."""
        if len(assignment) == len(self.variables):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result:
                    return result
                del assignment[var]
        return None

    def solve(self) -> dict[str, float]:
        """Запускає CSP з використанням пошуку з поверненням."""
        return self.backtrack({})
