OUTPUT_TO_CONSOLE = False


def log(message, end="\n"):
    if OUTPUT_TO_CONSOLE:
        print(message, end=end)
