from common_def import OUTPUT_FILE_SEPARATOR


class Claim:
    def __init__(self, claim, claim_seq):
        self.claim = claim
        self.claim_seq = claim_seq

    def output(self, fs, pnr):
        if fs is None:
            return
        fs.write("{1}{0}{2}{0}{3}\n".format(OUTPUT_FILE_SEPARATOR, pnr, self.claim_seq, self.claim))
