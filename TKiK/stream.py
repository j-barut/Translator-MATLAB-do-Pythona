

class Stream:

    def __init__(self, file_: str):
        self.file = open(file_, "r")
        self.current_line = self.file.readline()
        self.line_len = len(self.current_line)
        self.pos = 0

        if self.current_line == "":
            self.current_char = None  # EOF
        else:
            self.current_char = self.current_line[self.pos]


    def advance(self):

        self.pos += 1

        if self.pos >= self.line_len:
            self.current_line = self.file.readline()
            self.line_len = len(self.current_line)
            self.pos = 0

            if self.current_line == '':
                self.current_char = None
                return

        self.current_char = self.current_line[self.pos]

    def close(self):
        self.file.close()
