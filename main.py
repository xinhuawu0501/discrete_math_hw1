import random
import sys
import numpy as np
import matplotlib.pyplot as plt


def gen_obstacle(n: int, p: float) -> list:
    num_of_ob = int((n * n - 2) * p)
    obstacles = random.sample(range(1, n * n - 1), num_of_ob)
    return obstacles

def print_board(board: list):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if i == j == 0:
                print("|S", end=" ")
            elif board[i][j] == -1:
                print("|X", end=" ")
            elif i == j == len(board) - 1:
                print("|E", end=" ")
            else:
                print("| ", end=" ")
        print("\n")


def create_board(n: int, obstacle = 0.2) -> list:
    board = [[None for _ in range(n)] for _ in range(n)]
    
    ob = gen_obstacle(n, obstacle)
    for i in range(len(ob)):
        row = int(ob[i] / n)
        col = int(ob[i] % n)
        board[row][col] = -1 
    
    return board

## scenario 1
def numb_of_path_dp(board: list):
    n = len(board)
    dp = [[0 for _ in  range(n)] for _ in range(n)]
    
    dp[0][0] = 1

    for i in range(n):
        for j in range(n):
            if i == j == 0:
                continue
            elif board[i][j] == -1: # obstacle
                dp[i][j] = 0
            elif i == 0: # leftmost col
                dp[i][j] = dp[i][j - 1]
            elif j == 0:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = dp[i][j - 1] + dp[i - 1][j]


    return dp[n - 1][n - 1]

def num_of_path_recursion(board: list) -> int:
    n = len(board)

    def recursion(i: int, j: int) -> int:
        nonlocal n
        if i == j == n - 1:
            return 1
        if i > n - 1 or j > n - 1:
            return 0
        if board[i][j] == -1:
            return 0
        return recursion(i, j + 1) + recursion(i + 1, j)
    
    return recursion(0, 0)


## scenario 2
## whenever changing direction, cost + 1
def num_of_shortest_path_dp(board: list):
    n = len(board)
    
    # dp[i][j][k] = (min_cost, num_of_ways)
    # k indicates the direction of path to the position board[i][j]
    # k = 0 -> comes from left
    # k = 1 -> comes from top
    dp = [[[(0, 0), (0, 0)] for _ in range(n)] for _ in range(n)]
    invalid_path = (sys.maxsize, 0)

    dp[0][0][0] = dp[0][0][1] = (0, 1)

    for i in range(n):
        for j in range(n):
            cur = dp[i][j]
            if i == j == 0:
                continue
            elif board[i][j] == -1:
                cur[0] = cur[1] = invalid_path
            elif j == 0:
                cur[1] = dp[i - 1][j][1]
                cur[0] = invalid_path
            elif i == 0:
                cur[0] = dp[i][j - 1][0]
                cur[1] = invalid_path
            else:
                def calculate(same_direction: tuple[int, int], different_direction: tuple[int, int]) -> tuple[int, int]:
                    if same_direction[0] < different_direction[0] + 1:
                        return same_direction
                    elif same_direction[0] == different_direction[0] + 1:
                        return (same_direction[0], same_direction[1] + different_direction[1])
                    else:
                        return (different_direction[0] + 1, different_direction[1])
                cur[0] = calculate(dp[i][j-1][0], dp[i][j-1][1])
                cur[1] = calculate(dp[i-1][j][1], dp[i-1][j][0])        
    

    result = dp[n - 1][n - 1][0][1]
    if dp[n - 1][n - 1][0][0] == dp[n - 1][n - 1][1][0]:
        result += dp[n - 1][n - 1][1][1]
    elif dp[n - 1][n - 1][1][0] < dp[n - 1][n - 1][0][0]:
        result = dp[n - 1][n - 1][1][1]

    return result

def num_of_shortest_path_recursion(board: list) -> int:
    n = len(board)
    min_cost = sys.maxsize
    path_count = 0

    # 0->from left, 1->from top
    def recursion(i: int, j: int, cost: int, direction: int):
        nonlocal n, min_cost, path_count
        if i == j == n - 1:
            if cost < min_cost:
                min_cost = cost
                path_count = 1
            elif cost == min_cost:
                path_count += 1
            return
        if i > n - 1 or j > n - 1 or board[i][j] == -1:
            return
        else:
            recursion(i, j + 1, cost + (direction != 0), 0)
            recursion(i + 1, j, cost + (direction != 1), 1)
    
    recursion(0, 1, 0, 0)
    recursion(1, 0, 0, 1)

    return path_count


        
def get_expected_value(n=20, obstacle=0.2, fn=numb_of_path_dp) -> float:
    t = 100000 
    sum = 0

    for _ in range(t):
        board = create_board(n, obstacle)
        w = fn(board)
        sum += w
    return sum / t

def draw_plot(max_n: int, fn: callable, obstacle=0.2, color="r", title="", filename="plot.png"):
    x_int = np.arange(1, max_n + 1)
    print(x_int)
        
    y = [get_expected_value(x_int[i], obstacle, fn) for i in range(len(x_int))]
    print(y)

    plt.plot(x_int, y, color)
    plt.xticks(x_int)


    plt.title(title)
    plt.xlabel("n")
    plt.ylabel("path count")

    plt.savefig(filename)

if __name__ == '__main__':
    n = int(input("Enter n:\n"))
    obstacle = float(input("Enter density of obstacle (0-1):\n")) 
   
    # print(get_expected_value(n, numb_of_ways_dp))
    # print(get_expected_value(n, obstacle, num_of_shortest_path_dp))

    ##! comment the code below if you don't want ot draw plot
    ## 1. scenario 1
    title1 = f"Number of path (obstacle density={obstacle})"
    filename1 = "all_path.png"
    draw_plot(n, numb_of_path_dp, obstacle, "r",  title1, filename1)

    ## 2. scenario 2: 
    title2 = f"Number of shortest path (obstacle density={obstacle})"
    filename2 = "shortest_path.png"
    # draw_plot(n, num_of_shortest_path_dp, obstacle, "b", title2, filename2)

    plt.show()
    
