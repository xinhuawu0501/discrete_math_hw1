import random

def gen_obstacle(n: int, p: float) -> list:
    num_of_ob = int((n * n - 1) * p)
    obstacles = random.sample(range(1, n * n), num_of_ob)
    return obstacles


def create_board(n: int) -> list:
    board = [[None for _ in range(n)] for _ in range(n)]
    
    ob = gen_obstacle(n)
    for i in range(len(ob)):
        row = ob[i] / n
        col = ob[i] % n
        board[row][col] = -1

    return board

def numb_of_ways(board: list):
    ## all possible ways
    ## dp
    dp = [[0 for _ in range(n)] for _ in range(n)]


def get_expected_value(n: int) -> float:
    t = 1000 # ?
    sum = 0
    for _ in range(t):
        board = create_board(n)
        sum += numb_of_ways(board)
    return sum / t

if __name__ == '__main__':
    n = int(input("Enter n:\n"))
    print(get_expected_value(n))
