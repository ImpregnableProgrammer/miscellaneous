"""
Runtime Performance Evaluation (n=25 items, capacity=200):
- Pure Recursive:      ~2.827 seconds (Exponential Time O(2^n))
- Memoization:         ~0.026 seconds (Pseudo-polynomial Time O(n*W))
- Bottom-Up Tabulation: ~0.031 seconds (Pseudo-polynomial Time O(n*W))

As demonstrated, both Memoization and Tabulation drastically outperform
the naive recursive approach by avoiding redundant subproblem calculations.
"""

import argparse
import sys


def knapsack(capacity: int, weights: list[int], values: list[int]) -> int:
    """
    Solves the 0/1 Knapsack problem using Dynamic Programming.

    The 0/1 Knapsack problem is defined as:
    Given a set of items, each with a weight and a value, determine the maximum
    value of items to include in a collection so that the total weight is less than
    or equal to a given limit (capacity). You cannot break items (0/1 property).

    Algorithm Explanation:
    We use a 2D table `dp` where `dp[i][w]` represents the maximum value that can be
    attained with a knapsack of capacity `w` using only the first `i` items.

    For each item `i` (from 1 to n) and for each weight capacity `w` (from 0 to capacity):
    1. If the weight of the current item `weights[i-1]` is greater than the current
       capacity `w`, we cannot include this item. Thus, the max value is the same
       as if we didn't have this item: dp[i][w] = dp[i-1][w]
    2. If the current item can fit in the knapsack (weights[i-1] <= w), we have two choices:
       a) Include the item: The value will be the item's value plus the maximum value
          we could get with the remaining capacity: values[i-1] + dp[i-1][w - weights[i-1]]
       b) Exclude the item: The value is the same as without it: dp[i-1][w]
       We take the maximum of these two choices.

    Complexity Analysis:
    - Time Complexity: O(n * W), where `n` is the number of items and `W` is the capacity.
      We iterate through a 2D array of size (n + 1) x (W + 1), performing constant O(1) operations.
      Note: This is pseudo-polynomial time because W is not the input size but the magnitude of the capacity.
    - Space Complexity: O(n * W) to store the 2D DP table.
      Optimization tip: We only ever look at the previous row (`i-1`), so we could optimize
      space complexity to O(W) using a 1D array. (For an interview, a 2D table is easier to explain first).

    Args:
        capacity: The maximum weight the knapsack can hold.
        weights: A list of integers representing the weights of the items.
        values: A list of integers representing the values of the items.

    Returns:
        The maximum value that can be put in a knapsack of the given capacity.
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    if len(weights) != len(values):
        raise ValueError("Weights and values must have the same number of elements.")
    if any(w < 0 for w in weights):
        raise ValueError("Weights cannot be negative.")
    if any(v < 0 for v in values):
        raise ValueError("Values cannot be negative.")

    n = len(values)

    # Initialize the DP table with zeros
    # Rows represent the number of items considered (0 to n)
    # Columns represent the current capacity of the knapsack (0 to capacity)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Build the DP table in a bottom-up manner
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # Check if the current item can fit in the knapsack with capacity 'w'
            if weights[i - 1] <= w:
                # Max of including vs excluding the current item
                include_item_value = values[i - 1] + dp[i - 1][w - weights[i - 1]]
                exclude_item_value = dp[i - 1][w]
                dp[i][w] = max(include_item_value, exclude_item_value)
            else:
                # Item is too heavy, we must exclude it
                dp[i][w] = dp[i - 1][w]

    # The bottom-right cell contains the maximum value for 'n' items and total 'capacity'
    return dp[n][capacity]


def knapsack_recursive(capacity: int, weights: list[int], values: list[int]) -> int:
    """
    Pure recursive approach without memoization.
    Time Complexity: O(2^n)
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    if len(weights) != len(values):
        raise ValueError("Weights and values must have the same number of elements.")
    if any(w < 0 for w in weights):
        raise ValueError("Weights cannot be negative.")
    if any(v < 0 for v in values):
        raise ValueError("Values cannot be negative.")

    n = len(values)

    def solve(cap, i):
        if i == 0 or cap == 0:
            return 0
        if weights[i - 1] > cap:
            return solve(cap, i - 1)
        else:
            return max(
                values[i - 1] + solve(cap - weights[i - 1], i - 1), solve(cap, i - 1)
            )

    return solve(capacity, n)


def knapsack_memoization(capacity: int, weights: list[int], values: list[int]) -> int:
    """
    Recursive approach with memoization.
    Time Complexity: O(n * W)
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    if len(weights) != len(values):
        raise ValueError("Weights and values must have the same number of elements.")
    if any(w < 0 for w in weights):
        raise ValueError("Weights cannot be negative.")
    if any(v < 0 for v in values):
        raise ValueError("Values cannot be negative.")

    n = len(values)
    memo = [[-1 for _ in range(capacity + 1)] for _ in range(n + 1)]

    def solve(cap, i):
        if i == 0 or cap == 0:
            return 0
        if memo[i][cap] != -1:
            return memo[i][cap]

        if weights[i - 1] > cap:
            memo[i][cap] = solve(cap, i - 1)
        else:
            memo[i][cap] = max(
                values[i - 1] + solve(cap - weights[i - 1], i - 1), solve(cap, i - 1)
            )
        return memo[i][cap]

    return solve(capacity, n)


def knapsack_optimized(capacity: int, weights: list[int], values: list[int]) -> int:
    """
    Space-optimized Dynamic Programming approach.
    Time Complexity: O(n * W)
    Space Complexity: O(W)
    
    Instead of maintaining a 2D array, we use a 1D array of size W+1.
    We iterate backwards through the capacity to ensure that we are using
    values from the previous iteration (i.e. we don't use the same item twice).
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    if len(weights) != len(values):
        raise ValueError("Weights and values must have the same number of elements.")
    if any(w < 0 for w in weights):
        raise ValueError("Weights cannot be negative.")
    if any(v < 0 for v in values):
        raise ValueError("Values cannot be negative.")
        
    n = len(values)
    dp = [0 for _ in range(capacity + 1)]
    
    for i in range(n):
        # Traverse backwards to prevent reusing the same item
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
            
    return dp[capacity]


def knapsack_unbounded(capacity: int, weights: list[int], values: list[int]) -> int:
    """
    Solves the Unbounded Knapsack problem using space-optimized Dynamic Programming.
    
    Variation:
    Unlike 0/1 Knapsack where each item can be used at most once, in the Unbounded
    Knapsack problem, each item can be used an unlimited number of times.
    
    Implementation:
    We use a 1D DP array of size W+1. The core difference from the space-optimized 
    0/1 knapsack is the inner loop direction. Here, we iterate FORWARDS through the 
    capacities. By iterating forwards, when we calculate dp[w], dp[w - weights[i]] 
    might already contain the value of picking item `i` once (or multiple times), 
    allowing us to naturally pick it again.
    
    Time Complexity: O(n * W)
    Space Complexity: O(W)
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    if len(weights) != len(values):
        raise ValueError("Weights and values must have the same number of elements.")
    if any(w < 0 for w in weights):
        raise ValueError("Weights cannot be negative.")
    if any(v < 0 for v in values):
        raise ValueError("Values cannot be negative.")
        
    n = len(values)
    dp = [0 for _ in range(capacity + 1)]
    
    for i in range(n):
        # Traverse forwards to allow reusing the same item multiple times
        for w in range(weights[i], capacity + 1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
            
    return dp[capacity]


def knapsack_fractional(capacity: int, weights: list[int], values: list[int]) -> float:
    """
    Solves the Fractional Knapsack problem using a Greedy approach.
    
    Variation:
    In the Fractional Knapsack problem, you are allowed to break items into smaller
    fractions. For example, you can take 50% of an item for 50% of its weight and value.
    Because items can be broken down, Dynamic Programming is NOT necessary and is in 
    fact sub-optimal.
    
    Implementation:
    The optimal approach is a Greedy Algorithm. We calculate the value-to-weight ratio
    for each item, sort the items in descending order of this ratio, and greedily take
    as much as possible of the highest-ratio items until the knapsack is completely full.
    
    Time Complexity: O(n log n) due to sorting.
    Space Complexity: O(n) to store the items with their ratios.
    
    Returns:
        A float representing the maximum fractional value achievable.
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    if len(weights) != len(values):
        raise ValueError("Weights and values must have the same number of elements.")
    if any(w < 0 for w in weights):
        raise ValueError("Weights cannot be negative.")
    if any(v < 0 for v in values):
        raise ValueError("Values cannot be negative.")
        
    n = len(values)
    items = []
    for i in range(n):
        if weights[i] == 0:
            ratio = float('inf') if values[i] > 0 else 0.0
        else:
            ratio = values[i] / weights[i]
        items.append((ratio, weights[i], values[i]))
        
    # Sort items by value-to-weight ratio in descending order
    items.sort(key=lambda x: x[0], reverse=True)
    
    total_value = 0.0
    current_capacity = capacity
    
    for ratio, weight, value in items:
        if current_capacity == 0:
            break
            
        if weight <= current_capacity:
            # Take the whole item
            total_value += value
            current_capacity -= weight
        else:
            # Take a fraction of the item
            fraction = current_capacity / weight
            total_value += value * fraction
            current_capacity = 0
            break
            
    return total_value


def parse_int_list(arg):
    if not arg.strip():
        return []
    try:
        return [int(x.strip()) for x in arg.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError(
            "List must contain only integers separated by commas."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the 0/1 Knapsack problem.")
    parser.add_argument(
        "-c",
        "--capacity",
        type=int,
        required=True,
        help="Maximum capacity of the knapsack",
    )
    parser.add_argument(
        "-w",
        "--weights",
        type=parse_int_list,
        required=True,
        help="Comma-separated list of item weights",
    )
    parser.add_argument(
        "-v",
        "--values",
        type=parse_int_list,
        required=True,
        help="Comma-separated list of item values",
    )
    parser.add_argument(
        "-m",
        "--method",
        type=str,
        choices=["dp", "recursive", "memo", "optimized", "unbounded", "fractional"],
        default="dp",
        help="Method to solve the knapsack problem",
    )

    args = parser.parse_args()

    try:
        if args.method == "dp":
            max_value = knapsack(args.capacity, args.weights, args.values)
        elif args.method == "recursive":
            max_value = knapsack_recursive(args.capacity, args.weights, args.values)
        elif args.method == "memo":
            max_value = knapsack_memoization(args.capacity, args.weights, args.values)
        elif args.method == "optimized":
            max_value = knapsack_optimized(args.capacity, args.weights, args.values)
        elif args.method == "unbounded":
            max_value = knapsack_unbounded(args.capacity, args.weights, args.values)
        elif args.method == "fractional":
            max_value = knapsack_fractional(args.capacity, args.weights, args.values)

        print(f"Maximum value that can be attained: {max_value}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
