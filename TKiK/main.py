
from stream import Stream
from skaner2 import Scanner2
from html import Html
if __name__ == "__main__":

    stream = Stream("equation.txt")
    scanner = Scanner2(stream)
    tokens = scanner.tokenize()

    for token in tokens:
        print(token)

    writer = Html(tokens)
    writer.write()
