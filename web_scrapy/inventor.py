from common_def import OUTPUT_FILE_SEPARATOR


class Inventor:
    def __init__(self, name, inventor_seq):
        self.name = name
        self.inventor_seq = inventor_seq

    def output(self, fs, pnr):
        if fs is None:
            return
        fs.write("{1}{0}{2}{0}{3}\n".format(OUTPUT_FILE_SEPARATOR, pnr, self.inventor_seq, self.name))
