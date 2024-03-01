import copy
import random
from queue import PriorityQueue

def create_tile_puzzle(rows, cols):
    board=[]
    for x in range(rows):
        reset=[]
        for y in range(cols):
            reset.append(0)
        board.append(reset)
    for i in range(rows):
        for j in range(cols):
            board[i][j]=1+(cols*i)+j
            board[rows-1][cols-1]=0
    return TilePuzzle(board)

class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.board=board
        self.row_len=len(board)
        self.col_len=len(board[0])

        for empty_row in range(len(board)):
            for empty_col in range(len(board[0])):
                if board[empty_row][empty_col]==0:
                    self.empty_r=empty_row
                    self.empty_c=empty_col

    def get_board(self):
        return self.board

    def perform_move(self, direction):

        r, c = self.empty_r, self.empty_c
        if direction == 'up' :
            r -= 1
        elif direction == 'down':
            r += 1

        elif direction == 'left':
            c -= 1

        elif direction == 'right':
            c += 1
        else:
            return False
        if r<0 or r>=self.row_len:
            return False
        if c<0 or c>=self.col_len:
            return False

        temp=self.board[r][c]
        self.board[r][c]=self.board[self.empty_r][self.empty_c]
        self.board[self.empty_r][self.empty_c]=temp

        self.empty_r=r
        self.empty_c=c
        return True

    def scramble(self, num_moves):
        possible_moves = random.choice(["up", "down", "left", "right"])
        for i in range(num_moves):
            self.perform_move(possible_moves)


    def is_solved(self):
        current = 1
        for i in range(self.row_len):
            for j in range(self.col_len):
                if self.board[i][j]==0:
                    pass
                elif self.board[i][j]!=current:
                    return False
                current += 1

        return True


    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        fourmoves=["up","down","left","right"]
        for move in fourmoves:
            new_puzzle=self.copy()
            if new_puzzle.perform_move(move):
                yield move,new_puzzle

    def iddfs_helper(self, limit, moves):
        if self.is_solved():
            yield moves
        if limit<=0:
            return
        elif limit > 0:
            for move, new_puzzle in self.successors():
                yield from new_puzzle.iddfs_helper(limit - 1, moves + [move])


    def find_solutions_iddfs(self):
        limit = 0
        while True:
            limit=limit+1
            solutionss=list(self.iddfs_helper(limit,[]))
            if solutionss:
                return self.iddfs_helper(limit,[])


    # Required
    def manhattan_distance(self):
        distance = 0
        for i in range(self.row_len):
            for j in range(self.col_len):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j] - 1, 3)
                    distance += abs(x - i) + abs(y - j)
        return distance

    def find_solution_a_star(self):

        solved = TilePuzzle([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

        queue = PriorityQueue()
        queue.put((self.manhattan_distance(), []))

        visited = set()
        visited.add(tuple(map(tuple, self.board)))

        while not queue.empty():
            _,moves = queue.get()
            curr = self.copy()
            for move in moves:
                curr.perform_move(move)

            if curr.board == solved.board:
                return moves

            for direction, neighbor in curr.successors():
                if tuple(map(tuple, neighbor.board)) not in visited:
                    visited.add(tuple(map(tuple, neighbor.board)))
                    next_moves = moves + [direction]
                    queue.put((len(next_moves) + neighbor.manhattan_distance(), next_moves))

b = [[1,2,3], [4,0,5], [6,7,8]]
p = TilePuzzle(b)
print(p.find_solution_a_star())