from inventor import Inventor
from ipc import IPC
from applicant import Applicant
from claim import Claim
from event import Event
from cite import Cite
from lxml import etree
from common_def import FilePathDef
from common_def import OUTPUT_FILE_SEPARATOR


class PatentInfo:
    def __init__(self):
        self.ida = ""
        self.adate = ""
        self.pnr = ""
        self.pdate = ""
        # self.address = ""
        self.title = ""
        self.desc = ""
        self.ipc = list()
        self.inventor = list()
        self.applicant = list()
        self.claim = list()
        self.event = list()
        self.cite = list()
        self.family_cite = list()
        self.num_ipc = 0
        self.num_claim = 0
        self.num_inventor = 0
        self.num_applicant = 0

    def load_basic(self, pt_tree):
        self.ida = ''.join(pt_tree.xpath('//dd[@itemprop="applicationNumber"]/text()')).strip()
        self.adate = ''.join(pt_tree.xpath('//dd/time[@itemprop="filingDate"]/text()')).strip()
        self.pnr = ''.join(pt_tree.xpath('//dd[@itemprop="publicationNumber"]/text()')).strip()
        self.pdate = ''.join(pt_tree.xpath('//dd/time[@itemprop="publicationDate"]/text()')).strip()
        self.title = ''.join(pt_tree.xpath('//span[@itemprop="title"]/text()')[0]).strip()
        self.desc = ''.join(pt_tree.xpath('//section[@itemprop="description"]//text()')).replace('\n',
                                                                                                 "newline").strip()

    def load_inventor(self, pt_tree):
        inventors = pt_tree.xpath('//dd[@itemprop="inventor"]/text()')
        self.num_inventor = len(inventors)
        if self.num_inventor > 0:
            inventor_seq = 1
            for name in inventors:
                self.inventor.append(Inventor(name.strip(), inventor_seq))
                inventor_seq += 1
        pass

    def load_ipc(self, pt_tree):
        ipcs = pt_tree.xpath(
            '//li[@itemprop="classifications"]/meta[@itemprop="Leaf"]/../span[@itemprop="Code"]//text()')
        self.num_ipc = len(ipcs)
        if self.num_ipc > 0:
            ipc_seq = 1
            for code in ipcs:
                self.ipc.append(IPC(code.strip(), ipc_seq))
                ipc_seq += 1
        pass

    def load_applicant(self, pt_tree):
        applicants = pt_tree.xpath('//dd[@itemprop="assigneeOriginal"]/text()')
        self.num_applicant = len(applicants)
        if self.num_applicant > 0:
            applicant_seq = 1
            for name in applicants:
                self.applicant.append(Applicant(name.strip(), applicant_seq))
                applicant_seq += 1
        pass

    def load_claim(self, pt_tree):
        claims = pt_tree.xpath('//section[@itemprop="claims"]//div[@num]')
        self.num_claim = len(claims)
        if self.num_claim > 0:
            claim_seq = 1
            for claim_orign in claims:
                claim = ''.join(claim_orign.xpath('.//div[@class="claim-text"]//text()')).replace("\n", "").strip()
                self.claim.append(Claim(claim.strip(), claim_seq))
                claim_seq += 1
        pass

    def load_event(self, pt_tree):
        legal_elements = pt_tree.xpath('//tr[@itemprop="legalEvents"]')
        if legal_elements:
            for legal in legal_elements:
                legal_html = etree.tostring(legal, pretty_print=True).decode('utf-8')
                legal_tree = etree.HTML(legal_html)
                date = ''.join(legal_tree.xpath('//time[@itemprop="date"]/text()')).strip()
                code = ''.join(legal_tree.xpath('//td[@itemprop="code"]/text()')).strip()
                title = ''.join(legal_tree.xpath('//td[@itemprop="title"]/text()')).strip()
                legal_desc_lst = legal_tree.xpath('//td//p[@itemprop="attributes"]//text()')
                if legal_desc_lst:
                    legal_description = ''.join([x.strip() for x in legal_desc_lst]).strip()
                else:
                    legal_description = ''
                self.event.append(Event(date, code, title, legal_description))
        pass

    def load_cite(self, pt_tree):
        pc_elements = pt_tree.xpath('//tr[@itemprop="backwardReferences"]')
        if pc_elements:
            for pc in pc_elements:
                pc_html = etree.tostring(pc, pretty_print=True).decode('utf-8')
                pc_tree = etree.HTML(pc_html)
                pn = ''.join(pc_tree.xpath('//span[@itemprop="publicationNumber"]/text()')).strip()
                pl = ''.join(pc_tree.xpath('//span[@itemprop="primaryLanguage"]/text()')).strip()
                ec = ''.join(pc_tree.xpath('//span[@itemprop="examinerCited"]/text()')).strip()
                prd = ''.join(pc_tree.xpath('//td[@itemprop="priorityDate"]/text()')).strip()
                pud = ''.join(pc_tree.xpath('//td[@itemprop="publicationDate"]/text()')).strip()
                ae = ''.join(pc_tree.xpath('//span[@itemprop="assigneeOriginal"]/text()')).strip()
                tl = ''.join(pc_tree.xpath('//td[@itemprop="title"]/text()')).strip()
                self.cite.append(Cite(pn, pl, ec, prd, pud, ae, tl))
        pass

    def load_family_cite(self, pt_tree):
        fc_elements = pt_tree.xpath('//tr[@itemprop="backwardReferencesFamily"]')
        if fc_elements:
            for fc in fc_elements:
                fc_html = etree.tostring(fc, pretty_print=True).decode('utf-8')
                fc_tree = etree.HTML(fc_html)
                pn = ''.join(fc_tree.xpath('//span[@itemprop="publicationNumber"]/text()')).strip()
                pl = ''.join(fc_tree.xpath('//span[@itemprop="primaryLanguage"]/text()')).strip()
                ec = ''.join(fc_tree.xpath('//span[@itemprop="examinerCited"]/text()')).strip()
                prd = ''.join(fc_tree.xpath('//td[@itemprop="priorityDate"]/text()')).strip()
                pud = ''.join(fc_tree.xpath('//td[@itemprop="publicationDate"]/text()')).strip()
                ae = ''.join(fc_tree.xpath('//span[@itemprop="assigneeOriginal"]/text()')).strip()
                tl = ''.join(fc_tree.xpath('//td[@itemprop="title"]/text()')).strip()
                pn_mix = f'{pn}({pl}){ec}'
                self.family_cite.append(Cite(pn_mix, pl, ec, prd, pud, ae, tl))
        pass

    def load_by_data(self, pt_tree):
        self.load_basic(pt_tree)
        self.load_inventor(pt_tree)
        self.load_ipc(pt_tree)
        self.load_applicant(pt_tree)
        self.load_claim(pt_tree)
        self.load_event(pt_tree)
        self.load_cite(pt_tree)
        self.load_family_cite(pt_tree)
        pass

    def output_inventor(self):
        with open(FilePathDef.INVENTOR_FILE_PATH, 'a') as fs:
            for inventor in self.inventor:
                inventor.output(fs, self.pnr)
        pass

    def output_ipc(self):
        with open(FilePathDef.IPC_FILE_PATH, 'a') as fs:
            for ipc in self.ipc:
                ipc.output(fs, self.pnr)
        pass

    def output_applicant(self):
        with open(FilePathDef.APPLICANT_FILE_PATH, 'a') as fs:
            for applicant in self.applicant:
                applicant.output(fs, self.pnr)
        pass

    def output_claim(self):
        with open(FilePathDef.CLAIM_FILE_PATH, 'a') as fs:
            for claim in self.claim:
                claim.output(fs, self.pnr)
        pass

    def output_event(self):
        with open(FilePathDef.EVENT_FILE_PATH, 'a') as fs:
            for event in self.event:
                event.output(fs, self.pnr)
        pass

    def output_publn(self):
        with open(FilePathDef.PUBLN_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}{0}{3}\n".format(OUTPUT_FILE_SEPARATOR, self.ida, self.pnr, self.pdate))
        pass

    def output_date(self):
        with open(FilePathDef.DATE_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, self.pnr, self.adate))
        pass

    def output_basic(self):
        with open(FilePathDef.BASIC_FILE_PATH, 'a') as fs:
            fs.write(
                "{1}{0}{2}{0}{3}{0}{4}{0}{5}\n".format(OUTPUT_FILE_SEPARATOR, self.pnr, self.num_ipc, self.num_claim,
                                                       self.num_inventor, self.num_applicant))
        pass

    def output_desc(self):
        with open(FilePathDef.DESC_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, self.pnr, self.desc))
        pass
    
    def output_title(self):
        with open(FilePathDef.TITLE_FILE_PATH, 'a') as fs:
            fs.write("{1}{0}{2}\n".format(OUTPUT_FILE_SEPARATOR, self.pnr, self.title))
        pass

    def output_cite(self, pnr):
        with open(FilePathDef.CITE_FILE_PATH, 'a') as fs:
            if self.cite:
                for cite in self.cite:
                    cite.output(fs, pnr)
        pass

    def output_family_cite(self, pnr):
        with open(FilePathDef.FAMILY_CITE_FILE_PATH, 'a') as fs:
            if self.family_cite:
                for cite in self.family_cite:
                    cite.output(fs, pnr)
        pass

    def output_data(self):
        self.output_publn()
        self.output_date()
        self.output_basic()
        self.output_cite(self.pnr)
        self.output_family_cite(self.pnr)
        self.output_inventor()
        self.output_ipc()
        self.output_applicant()
        self.output_claim()
        self.output_event()
        self.output_desc()
        self.output_title()
        pass
