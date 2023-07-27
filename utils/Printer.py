color = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "WHITE": "\033[97m",
    "RESET": "\033[0m"
}


def print_info(info):
    print(color["GREEN"] + info + color["RESET"])


def print_warn(warn):
    print(color["YELLOW"] + warn + color["RESET"])


def print_err(err):
    print(color["RED"] + err + color["RESET"])
