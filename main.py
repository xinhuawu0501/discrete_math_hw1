import random
import sys

def gen_obstacle(n: int, p: float) -> list:
    num_of_ob = int((n * n - 1) * p)
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


def create_board(n: int) -> list:
    board = [[None for _ in range(n)] for _ in range(n)]
    
    ob = gen_obstacle(n, 0.2)
    for i in range(len(ob)):
        row = int(ob[i] / n)
        col = int(ob[i] % n)
        board[row][col] = -1 
    
    return board

def numb_of_ways(board: list):
    ## all possible ways
    #TODO: print route
    ## dp
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

## whenever changing direction, cost + 1
def num_of_shortest_path(board: list):
    n = len(board)
    dp = [[[(0, 0), (0, 0)] for _ in range(n)] for _ in range(n)]
    invalid_path = (sys.maxsize, 0)

    # dp[i][j][k] = (min_cost, num_of_ways)
    # k indicates the direction of path to the position board[i][j]
    # k = 0 -> comes from left
    # k = 1 -> comes from top
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
                # k = 0 -> from left
                left_block = dp[i][j - 1]

                left_cost_left = left_block[0][0]
                left_cost_top = left_block[1][0] + 1
                min_cost_left = min(left_cost_left, left_cost_top)
                num_of_shortest_path_left = left_block[0][1]

                if left_cost_top == left_cost_left:
                    num_of_shortest_path_left += left_block[1][1]
                elif left_cost_top < left_cost_left:
                    num_of_shortest_path_left = left_block[1][1]

                cur[0] = (min_cost_left, num_of_shortest_path_left)  

                # k = 1 -> from top
                top_block = dp[i - 1][j]

                top_cost_left = top_block[0][0] + 1
                top_cost_top = top_block[1][0]
                min_cost_top = min(top_cost_left, top_cost_top)
                num_of_shortest_path_top = top_block[1][1]

                if top_cost_left == top_cost_top:
                    num_of_shortest_path_top += top_block[1][1]
                elif top_cost_left < top_cost_top:
                    num_of_shortest_path_top = top_block[0][1]
                    
                cur[1] = (min_cost_top, num_of_shortest_path_top)  
                
    print_board(board)
    for i in range(n):
        print(dp[i])

    result = dp[n - 1][n - 1][0][1]
    if dp[n - 1][n - 1][0][0] == dp[n - 1][n - 1][1][0]:
        result += dp[n - 1][n - 1][1][1]
    elif dp[n - 1][n - 1][1][0] < dp[n - 1][n - 1][0][0]:
        result = dp[n - 1][n - 1][1][0]

    print(result)
    return result

def get_expected_value(n: int) -> float:
    t = 1000000 #find threshold
    sum = 0

    num_of_shortest_path(create_board(n))

    # for _ in range(t):
    #     board = create_board(n)
    #     print_board(board)
    #     w = numb_of_ways(board)
    #     print(w)
    #     sum += w
    return sum / t

if __name__ == '__main__':
    n = int(input("Enter n:\n"))
    print(get_expected_value(n))
