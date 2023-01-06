TESTING = False

def read_board(lines, line_num):
    return([[(int(num), False) for num in row.split()]
            for row in lines[line_num + 1:line_num + 6]])

def read_input():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    draw = [int(num) for num in lines.pop(0).split(",")]
    print(f"Draw: {draw}")

    boards = []
    line_num = 0

    while line_num < len(lines):
        boards.append(read_board(lines, line_num))
        line_num += 6

    print(f"Boards: {boards}")

    return draw, boards

def clear_boards(boards):
    return([[[(num, False) for (num, _) in row]
            for row in board] for board in boards])

def mark_boards(boards, draw_num):
    return([[[(num, marked or num == draw_num) for (num, marked) in row]
            for row in board] for board in boards])

def all_marked(row_or_column):
    return all(marked for (_, marked) in row_or_column)

def transpose(board):
    return list(map(list, zip(*board)))

def check_winner(boards):
    for board in boards:
        for row in board:
            if all_marked(row):
                return board

        for column in transpose(board):
            if all_marked(column):
                return board

    return False

def play_bingo(draw, boards):
    boards = clear_boards(boards)

    for draw_num in draw:
        boards = mark_boards(boards, draw_num)

        winning_board = check_winner(boards)

        if (winning_board):
            print(f"Winning board is {winning_board} after drawing {draw_num}")
            return winning_board, draw_num

    print(f"No winning board after all numbers have been drawn: {boards}")
    exit(1)

def unmarked_nums(board):
    return [num for row in board for (num, marked) in row if not marked]

def part1():
    draw, boards = read_input()

    winning_board, winning_num = play_bingo(draw, boards)

    return sum(unmarked_nums(winning_board)) * winning_num

def part2():
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
