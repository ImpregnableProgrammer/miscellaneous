def coin_change_iterative(target: int, coins: list[int] = [1, 2, 5, 10, 20, 50, 100]):
    """
    Dynamic programming implementation for the coin change problem: given `target`, return the minimum number of coins needed to create that amount.

    The table is created bottom-up in an iterartive fashion.
    """
    # Recurrence:
    # DP[A] = min(1 + DP[A - coin]) for coin in coins, DP[0] = 0, DP[x != 0] = inf
    import math

    DP = [math.inf] * (target + 1)
    DP[0] = 0
    for coin in coins:
        for i in range(coin, target + 1):
            DP[i] = min(DP[i], 1 + DP[i - coin])
    return DP[target]


if __name__ == "__main__":
    print(coin_change_iterative(60))
