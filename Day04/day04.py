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

def board_is_winner(board):
    for row in board:
        if all_marked(row):
            return True

    for column in transpose(board):
        if all_marked(column):
            return True

    return False

def check_for_winners(boards):
    non_winning_boards = []
    winning_boards = []

    for board_num in range(0, len(boards)):
        board = boards.pop()

        if board_is_winner(board):
            winning_boards.append(board)
        else:
            non_winning_boards.append(board)

    return winning_boards, non_winning_boards

def play_bingo(draw, boards):
    boards = clear_boards(boards)
    winners = []

    for draw_num in draw:
        boards = mark_boards(boards, draw_num)

        winning_boards, boards = check_for_winners(boards)

        if (winning_boards):
            # print(f"After drawing {draw_num}, winning boards are {winning_boards}")
            winners.append((winning_boards, draw_num))

            if len(boards) == 0:
                print("All boards are winners")
                return winners

    print(f"At least one board never wins: {boards}")
    return winners

def unmarked_nums(board):
    return [num for row in board for (num, marked) in row if not marked]

def part1():
    draw, boards = read_input()

    winners = play_bingo(draw, boards)
    winning_boards, winning_num = winners[0]

    return sum(unmarked_nums(winning_boards[0])) * winning_num

def part2():
    draw, boards = read_input()

    winners = play_bingo(draw, boards)
    last_winning_boards, last_winning_num = winners[len(winners) - 1]

    return sum(unmarked_nums(last_winning_boards[0])) * last_winning_num


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
