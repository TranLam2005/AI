from copy import deepcopy

START = []
END = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
MOVE_DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}


class Node:
    def __init__(self, current_node, previous_node, g, h, move):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.move = move

    def f(self):
        return self.g + self.h


def input_matrix():
    print("Trạng thái ban đầu:")
    for _ in range(3):
        START.append([int(x) for x in input().split()])


def print_matrix(matrix):
    for row in matrix:
        for value in row:
            if value == 0:
                print(" ", end=" ")
            else:
                print(value, end=" ")
        print()


def get_position_matrix(BEGIN, END):
    index_dict = {value: index for index, row in enumerate(END) for value in row}
    position_array = [index_dict[value] for row in BEGIN for value in row if value != 0]
    return position_array


def is_solvable(BEGIN, END):
    inv_count = 0
    position_arr = get_position_matrix(BEGIN, END)
    for i in range(0, 8):
        for j in range(i + 1, 8):
            if position_arr[j] < position_arr[i]:
                inv_count += 1
    return inv_count % 2 == 0


def get_pos(element, matrix):
    for row_idx, row in enumerate(matrix):
        if element in row:
            return (row_idx, row.index(element))


def move_empty_tile(matrix, move):
    empty_tile = get_pos(0, matrix)
    new_row = empty_tile[0] + MOVE_DIRECTIONS[move][0]
    new_col = empty_tile[1] + MOVE_DIRECTIONS[move][1]
    if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix):
        matrix[empty_tile[0]][empty_tile[1]], matrix[new_row][new_col] = matrix[new_row][new_col], \
        matrix[empty_tile[0]][empty_tile[1]]
        return matrix
    return None


def manhattan_distance(matrix):
    cost = 0
    for row_idx, row in enumerate(matrix):
        for col_idx, value in enumerate(row):
            if value != 0:
                target_row, target_col = get_pos(value, END)
                cost += abs(row_idx - target_row) + abs(col_idx - target_col)
    return cost


def get_adj_node(node):
    list_node = []
    for move in MOVE_DIRECTIONS:
        new_state = move_empty_tile(deepcopy(node.current_node), move)
        if new_state:
            list_node.append(Node(new_state, node.current_node, node.g + 1, manhattan_distance(new_state), move))
    return list_node


def get_best_node(OPEN):
    return min(OPEN.values(), key=lambda node: node.f())


def build_path(CLOSE):
    node = CLOSE[str(END)]
    path = []
    while node.move:
        path.append({"move": node.move, "node": node.current_node})
        node = CLOSE[str(node.previous_node)]
    path.append({"move": "", "node": node.current_node})
    path.reverse()
    return path


def main(puzzle):
    OPEN = {str(puzzle): Node(puzzle, puzzle, 0, manhattan_distance(puzzle), "")}
    CLOSE = {}
    while True:
        best_node = get_best_node(OPEN)
        CLOSE[str(best_node.current_node)] = best_node
        if best_node.current_node == END:
            return build_path(CLOSE)
        adj_nodes = get_adj_node(best_node)
        for node in adj_nodes:
            if str(node.current_node) not in CLOSE and (
                    str(node.current_node) not in OPEN or OPEN[str(node.current_node)].f() > node.f()):
                OPEN[str(node.current_node)] = node
        del OPEN[str(best_node.current_node)]


def print_example_matrix():
    example_matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    print("Trạng thái đích:")
    for row in example_matrix:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    print_example_matrix()

    while True:
        try:
            input_matrix()
            if len(START) == 3 and len(END) == 3:
                break
            else:
                print("Nhập không đúng vui lòng nhập lại.")
        except ValueError:
            print("Nhập không đúng vui lòng nhập lại.")

    if is_solvable(START, END):
        print("Trạng thái khởi tạo có thể trở thành trạng thái đích!")
    else:
        print("Trạng thái khởi tạo không thể trở thành trạng thái đích!")
        exit()
    path = main(START)
    print("Tổng số bước di chuyển: ", len(path) - 1)
    print("INPUT:")
    for step in path:
        if step["move"]:
            print("Di chuyển:", step["move"])
        print_matrix(step["node"])
        print()
    print("ABOVE IS THE OUTPUT")
