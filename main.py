from art import *
from ascii_magic import *


def escape_colors(string):
    return string.replace("\u001b", "\\u001b")


def unescape_colors(string):
    return string.replace("\\u001b", "\u001b")


def add_color_codes(line, color) -> str:
    """
    :param line:
    :param color: a string like "97m" for white
    """
    # replace each character <c> with \u001b[47m<c>
    return "".join([f"\u001b[{color}{c}" for c in line])


foreground = text2art("szge", font="univers")
foreground = add_color_codes(foreground, "97m")
foreground = foreground[:-1]  # remove last \n
# print(art_1)
foreground = escape_colors(foreground)
# print(art_1)
offset_x, offset_y = 85, 10
# pad lines_foreground with empty lines of offset_y
foreground_lines = foreground.split("\n")
foreground_lines = ["\\u001b[97m " * offset_x + line for line in foreground_lines]
# add empty lines of offset_y to the top
length = len(foreground_lines[0]) // 11
foreground_lines = ["\\u001b[97m " * length] * offset_y + foreground_lines
foreground = "\n".join(foreground_lines)

background = AsciiArt.from_image('abs8.jpg').to_ascii(columns=150)
# print(background)
background = escape_colors(background)
# print(background)


def get_char(ansi_image, x, y) -> str:
    if y >= len(ansi_image.split("\n")) or x * 11 + 11 >= len(ansi_image.split("\n")[y]):
        return "\\u001b[97m "
    char = ansi_image.split("\n")[y][x * 11:x * 11 + 11]
    return char


BORDER_DISTANCE = 2


def merge(background, foreground) -> str:
    """
    :param background:
    :param foreground:
    :return: merged string
    """
    lines_background = background.split("\n")
    lines_foreground = foreground.split("\n")

    for y, background_line in enumerate(lines_background):
        if y >= len(lines_foreground):
            break
        foreground_line = lines_foreground[y]
        foreground_line_arr = list(foreground_line)
        background_line_arr = list(background_line)

        for x in range(len(foreground_line_arr) // 11):
            i = x * 11
            if "".join(foreground_line_arr[i:i+11]) != "\\u001b[97m ":
                background_line_arr[i:i+11] = foreground_line_arr[i:i+11]

        lines_background[y] = "".join(background_line_arr)

    return "\n".join(lines_background)


if __name__ == "__main__":
    # https://talyian.github.io/ansicolors/
    print("\u001b[48;5;232m" + unescape_colors(merge(background, foreground)))
