# def expression_search(value):
#     """
#     Given a target `value`, find an expression that evaluates to it using only four 1's with the operations of addition, subtraction, multiplicationm, division, exponentiation (with any kind of exponent), factorial (fact), and summorial (summ(n) = 1+2+3+...+n = n(n+1)/2).

#     Will dynamic programming work? Will other searching algorithms work? What is the best way of going about solving this problem? Recursion? Depth first search? Breadth first search?

#     Unary ops: exponentiation, factorial, summorial
#     Binary ops: addition, subtraction, multiplication, division

#     EXAMPLES:
#         1+1+1+1 = sum(1+1)+1*1 = fact()
#     """

#     summ = lambda n: n * (n + 1) // 2
#     fact = lambda n: 1 if n < 1 else n * fact(n - 1)

#     constants = ["1"]
#     binary_ops = ["+", "-", "*", "/"]
#     unary_ops = ["summ", "fact", "**0", "**2", "**3", "**0.5"]

#     def calc(expr: str):
#         stack = []

#         for token in expr.split(" "):
#             if token.isnumeric():
#                 stack.append(int(token))
#             elif token in binary_ops:
#                 if len(stack) < 2:
#                     raise Exception(f"stack empty: {expr}")
#                 else:
#                     a, b = stack.pop(), stack.pop()
#                     stack.append(eval(f"{a}{token}{b}"))
#             elif token in unary_ops:
#                 if len(stack) < 1:
#                     raise Exception(f"stack empty: {expr}")
#                 else:
#                     a = stack.pop()
#                     if "**" in token:
#                         stack.append(eval(f"{a}{token}"))
#                     else:
#                         stack.append(
#                             eval(f"{token}({a})", globals={"summ": summ, "fact": fact})
#                         )
#             else:
#                 raise Exception(f"Invalid expression: {expr}")

#         if len(stack) > 0:
#             return stack[-1]
#         else:
#             raise Exception("Empty expression")

#     def helper(curr_expr: str):
#         try:
#             val = calc(curr_expr.strip(" "))
#             print(f"{curr_expr}, {val}")
#             if curr_expr.count("1") == 4:
#                 return (curr_expr, val)
#         except Exception as e:
#             print(f"Invalid expression: {e}")
#             return ("", 0)

#         for const in constants:
#             new_expr, rslt = helper(curr_expr + " " + const)
#             if rslt == value:
#                 return new_expr

#         for op in binary_ops:
#             new_expr, rslt = helper(curr_expr + " " + op)
#             if rslt == value:
#                 return new_expr

#         for op in unary_ops:
#             new_expr, rslt = helper(curr_expr + " " + op)
#             if rslt == value:
#                 return new_expr

#     return helper("1")


# if __name__ == "__main__":
#     import sys

#     sys.setrecursionlimit(50000)

#     print(expression_search(10))

import math
from collections import deque
from typing import List, Optional


class TargetFound(Exception):
    """Custom exception used to instantly halt the DP algorithm when the target is found."""

    def __init__(self, expr: str):
        self.expr = expr


def solve_four_ones(
    target: int, max_val: int = 1_000_000, free_exponents: List[float] = None
) -> Optional[str]:
    """
    Finds a mathematical expression using exactly four 1's that evaluates to the target.
    Uses Bottom-Up Dynamic Programming and BFS for Unary operations.

    Args:
        target: The integer value to reach.
        max_val: The maximum allowed intermediate value (prevents memory/time explosion).
        free_exponents: A list of rational numbers that can be used as free exponents
                        without consuming any '1's.
    """
    if free_exponents is None:
        # Default free exponents: Square, Cube, Square Root, Cube Root, Reciprocal
        free_exponents = [2.0, 3.0, 0.5, 1 / 3, -1.0]

    # memo[k] maps a computed numerical value to its string representation.
    # k represents the exact number of 1's used.
    memo = {1: {}, 2: {}, 3: {}, 4: {}}

    def is_int(v: float) -> bool:
        """Checks if a float is effectively an integer, bypassing floating-point drift."""
        if math.isnan(v) or math.isinf(v):
            return False
        return abs(round(v) - v) < 1e-8

    def add_val(k: int, val: float, expr: str) -> bool:
        """
        Attempts to add a new value/expression pair to our memo dictionary.
        Returns True if it was a new value and successfully added, False otherwise.
        """
        if math.isnan(val) or abs(val) > max_val:
            return False

        # Round the key to 8 decimal places to handle float precision issues safely
        key = round(val, 8)

        # If we hit the target during the 4th phase, we can stop the entire program!
        if k == 4 and key == round(target, 8):
            raise TargetFound(expr)

        if key not in memo[k]:
            memo[k][key] = expr
            return True
        else:
            # If the value exists, update it if the new expression is shorter/cleaner
            if len(expr) < len(memo[k][key]):
                memo[k][key] = expr
                return True
        return False

    def apply_unary(k: int):
        """
        Applies unary operations (Negation, Factorial, Summorial, Free Exponents).
        Uses a double-ended queue (deque) for O(1) pops, preventing infinite chaining loops.
        """
        queue = deque(memo[k].items())

        while queue:
            v, expr = queue.popleft()

            # 1. Unary Negation
            if add_val(k, -v, f"(-{expr})"):
                queue.append((-v, f"(-{expr})"))

            # 2. Free Exponents (e.g., ^2, ^3, ^0.5)
            for p in free_exponents:
                # Catch domain errors: 0 to a negative power, or negative base to a fractional power
                if (v == 0 and p <= 0) or (v < 0 and not is_int(p)):
                    continue

                try:
                    res = math.pow(v, p)

                    # Format the string beautifully based on the exponent
                    if is_int(p):
                        e_str = f"({expr}^{int(round(p))})"
                    elif abs(p - 0.5) < 1e-8:
                        e_str = f"√{expr}"
                    elif abs(p - (1 / 3)) < 1e-8:
                        e_str = f"³√{expr}"
                    else:
                        e_str = f"({expr}^{p})"

                    if add_val(k, res, e_str):
                        queue.append((res, e_str))
                except (ValueError, OverflowError, ZeroDivisionError):
                    pass

            # 3. Operations requiring Non-Negative Integers
            if is_int(v) and v >= 0:
                n = int(round(v))

                # Factorial (!): Cap n to prevent massive factorial calculation (10! = 3,628,800)
                if n <= 10:
                    fact_val = float(math.factorial(n))
                    if add_val(k, fact_val, f"({expr}!)"):
                        queue.append((fact_val, f"({expr}!)"))

                # Summorial (Σ): T(n) = n * (n + 1) / 2
                if n * (n + 1) // 2 <= max_val:
                    summ_val = float(n * (n + 1) // 2)
                    if add_val(k, summ_val, f"Σ{expr}"):
                        queue.append((summ_val, f"Σ{expr}"))

    def apply_binary(k: int, v1: float, v2: float, e1: str, e2: str):
        """Applies all allowed binary operations between two generated values."""
        add_val(k, v1 + v2, f"({e1} + {e2})")
        add_val(k, v1 - v2, f"({e1} - {e2})")
        add_val(k, v1 * v2, f"({e1} * {e2})")

        if abs(v2) > 1e-9:
            add_val(k, v1 / v2, f"({e1} / {e2})")

        # Standard Binary Exponentiation (e.g. constructing 2^2 using (1+1)^(1+1))
        try:
            if not ((v1 == 0 and v2 <= 0) or (v1 < 0 and not is_int(v2))):
                res = math.pow(v1, v2)
                add_val(k, res, f"({e1} ^ {e2})")
        except (ValueError, OverflowError, ZeroDivisionError):
            pass

    try:
        # Step 1: Base state (One '1')
        add_val(1, 1.0, "1")
        apply_unary(1)

        # Step 2: Combine (One '1' + One '1')
        for v1, e1 in list(memo[1].items()):
            for v2, e2 in list(memo[1].items()):
                apply_binary(2, v1, v2, e1, e2)
        apply_unary(2)

        # Step 3: Combine (Two '1's + One '1') AND (One '1' + Two '1's)
        for v1, e1 in list(memo[1].items()):
            for v2, e2 in list(memo[2].items()):
                apply_binary(3, v1, v2, e1, e2)
                apply_binary(3, v2, v1, e2, e1)
        apply_unary(3)

        # Step 4: Combine (Three '1's + One '1'), (One '1' + Three '1's), and (Two '1's + Two '1's)
        for v1, e1 in list(memo[1].items()):
            for v2, e2 in list(memo[3].items()):
                apply_binary(4, v1, v2, e1, e2)
                apply_binary(4, v2, v1, e2, e1)

        for v1, e1 in list(memo[2].items()):
            for v2, e2 in list(memo[2].items()):
                apply_binary(4, v1, v2, e1, e2)
        apply_unary(4)

    except TargetFound as success:
        return success.expr

    return None


if __name__ == "__main__":
    import time

    # We can pass any rational numbers we want to the free_exponents list!
    my_exponents = [2, 3, 0.5, 1 / 3]
    targets_to_find = [17, 32, 42, 64, 100, 256, 1337]

    print(
        f"Searching using DP Space (Allowed Free Exponents: {my_exponents})...\n"
        + "=" * 65
    )
    for t in targets_to_find:
        start = time.time()
        result = solve_four_ones(t, free_exponents=my_exponents)
        elapsed = time.time() - start

        if result:
            print(f"Target {t} found in {elapsed:.3f}s: \n-> {result}\n")
        else:
            print(f"Target {t} could not be found within the bounded max value.\n")
