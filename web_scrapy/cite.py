from common_def import OUTPUT_FILE_SEPARATOR


class Cite:
    def __init__(self, cited_pnr, language, examiner_cite, pridate, pdate, orig_assignee, title):
        self.cited_pnr = cited_pnr
        self.language = language
        self.examiner_cite = examiner_cite
        self.pridate = pridate
        self.pdate = pdate
        self.orig_assignee = orig_assignee
        self.title = title

    def output(self, fs, pnr):
        if fs is None:
            return
        fs.write(
            "{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{7}\n".format(OUTPUT_FILE_SEPARATOR, pnr, self.cited_pnr, self.language,
                                                            self.examiner_cite, self.pridate, self.pdate,
                                                            self.orig_assignee, self.title))
