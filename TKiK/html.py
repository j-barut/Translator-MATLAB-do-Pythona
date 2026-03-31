
from kolor import Colour
from skaner2 import TokenType


class Html:

    def __init__(self, tokens_: list):
        self.tokens = tokens_

    def write(self):
        html = "<pre>\n"
        for token in self.tokens:
            colour = Colour.get_colour_by_type(token.type)
            value = token.value

            if token.type == TokenType.EOL:
                html += "\n"

            elif token.type == TokenType.WHITESPACE:
                html += " "

            elif token.type == TokenType.EOF:
                continue

            else:
                html += f'<span style="color:{colour}">{value}</span>'
        html += "\n</pre>"

        with open('html.html', 'w') as f:
            f.write(html)
