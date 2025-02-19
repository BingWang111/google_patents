from common_def import OUTPUT_FILE_SEPARATOR


class IPC:
    def __init__(self, code, ipc_seq):
        self.code = code
        self.ipc_seq = ipc_seq

    def output(self, fs, pnr):
        if fs is None:
            return
        fs.write("{1}{0}{2}{0}{3}\n".format(OUTPUT_FILE_SEPARATOR, pnr, self.ipc_seq, self.code))
