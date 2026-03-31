
from kolory import COLOURS

class Colour:

    @staticmethod
    def get_colour(token):
        return COLOURS[token.type]

    @staticmethod
    def get_colour_by_type(token_type):
        return COLOURS[token_type]
