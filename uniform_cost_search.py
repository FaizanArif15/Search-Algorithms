import heapq

class PuzzleState:
    def __init__(self, puzzle, parent=None, action=None, cost=0):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        # Compare states based on their cost
        return self.cost < other.cost

    def __eq__(self, other):
        return self.puzzle == other.puzzle

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.puzzle))

    def find_blank_position(self):
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] == 0:
                    return i, j

    def get_possible_moves(self):
        moves = []
        row, col = self.blank_position
        if row > 0:
            moves.append("Up")
        if row < 2:
            moves.append("Down")
        if col > 0:
            moves.append("Left")
        if col < 2:
            moves.append("Right")
        return moves

    def perform_move(self, move):
        row, col = self.blank_position
        if move == "Up":
            new_row = row - 1
            new_puzzle = [list(row) for row in self.puzzle]
            new_puzzle[row][col], new_puzzle[new_row][col] = new_puzzle[new_row][col], new_puzzle[row][col]
        elif move == "Down":
            new_row = row + 1
            new_puzzle = [list(row) for row in self.puzzle]
            new_puzzle[row][col], new_puzzle[new_row][col] = new_puzzle[new_row][col], new_puzzle[row][col]
        elif move == "Left":
            new_col = col - 1
            new_puzzle = [list(row) for row in self.puzzle]
            new_puzzle[row][col], new_puzzle[row][new_col] = new_puzzle[row][new_col], new_puzzle[row][col]
        elif move == "Right":
            new_col = col + 1
            new_puzzle = [list(row) for row in self.puzzle]
            new_puzzle[row][col], new_puzzle[row][new_col] = new_puzzle[row][new_col], new_puzzle[row][col]
        return PuzzleState(new_puzzle, parent=self, action=move, cost=self.cost + 1)

def solve_8_puzzle(initial_state, goal_state):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, initial_state)

    while open_set:
        current_state = heapq.heappop(open_set)

        if current_state.puzzle == goal_state:
            return get_solution_path(current_state)

        closed_set.add(current_state)

        possible_moves = current_state.get_possible_moves()
        for move in possible_moves:
            new_state = current_state.perform_move(move)

            if new_state not in closed_set:
                heapq.heappush(open_set, new_state)

    return None

def get_solution_path(final_state):
    path = []
    current_state = final_state
    while current_state:
        path.append(current_state.action)
        current_state = current_state.parent
    return list(reversed(path))

# Example usage:
initial_state = [
    [1, 2, 3],
    [4, 0, 5],
    [6, 7, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

solution = solve_8_puzzle(PuzzleState(initial_state), goal_state)
if solution:
    print("Solution path:", solution)
else:
    print("No solution found.")
