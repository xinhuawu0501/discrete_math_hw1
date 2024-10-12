import random

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



def get_expected_value(n: int) -> float:
    t = 1000 # ?
    sum = 0

    b = create_board(n)
    print_board(b)
    print(numb_of_ways(b))


    # for _ in range(t):
    #     board = create_board(n)
    #     sum += numb_of_ways(board)
    return sum / t

if __name__ == '__main__':
    n = int(input("Enter n:\n"))
    print(get_expected_value(n))
