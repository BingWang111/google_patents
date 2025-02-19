import os

# OUTPUT_DIR = "paper_output"
OUTPUT_DIR = "patent_output"
INPUT_DIR = "patent_input"
HTML_DIR = "description/invention" 
HTML_DOWNLOAD_DIR = "description/htmltemp/"
UTILITY_DIR = "description/utility"
INVENTION_DIR = "description/invention"

INVENTOR_FILE_NAME = "inventor.txt"
APPLICANT_FILE_NAME = "applicant.txt"
IPC_FILE_NAME = "ipc.txt"
# ADDRESS_FILE_NAME = "address.txt"
DATE_FILE_NAME = "date.txt"
TITLE_FILE_NAME = "title.txt"
PUBLN_FILE_NAME = "publn.txt"
CITE_FILE_NAME = "cite.txt"
FAMILY_CITE_FILE_NAME = "family_cite.txt"
DESC_FILE_NAME = "desc.txt"
CLAIM_FILE_NAME = "claim.txt"
EVENT_FILE_NAME = "event.txt"
BASIC_FILE_NAME = "basic.txt"
OUTPUT_FILE_SEPARATOR = "|_"
PROC_HISTORY_PTS_FILE_NAME = PUBLN_FILE_NAME


class FilePathDef:
    INVENTOR_FILE_PATH = os.path.join(OUTPUT_DIR, INVENTOR_FILE_NAME)
    APPLICANT_FILE_PATH = os.path.join(OUTPUT_DIR, APPLICANT_FILE_NAME)
    IPC_FILE_PATH = os.path.join(OUTPUT_DIR, IPC_FILE_NAME)
    # ADDRESS_FILE_PATH = os.path.join(OUTPUT_DIR, ADDRESS_FILE_NAME)
    DATE_FILE_PATH = os.path.join(OUTPUT_DIR, DATE_FILE_NAME)
    TITLE_FILE_PATH = os.path.join(OUTPUT_DIR, TITLE_FILE_NAME)
    PUBLN_FILE_PATH = os.path.join(OUTPUT_DIR, PUBLN_FILE_NAME)
    CITE_FILE_PATH = os.path.join(OUTPUT_DIR, CITE_FILE_NAME)
    DESC_FILE_PATH = os.path.join(OUTPUT_DIR, DESC_FILE_NAME)
    FAMILY_CITE_FILE_PATH = os.path.join(OUTPUT_DIR, FAMILY_CITE_FILE_NAME)
    CLAIM_FILE_PATH = os.path.join(OUTPUT_DIR, CLAIM_FILE_NAME)
    EVENT_FILE_PATH = os.path.join(OUTPUT_DIR, EVENT_FILE_NAME)
    BASIC_FILE_PATH = os.path.join(OUTPUT_DIR, BASIC_FILE_NAME)
    PROC_HISTORY_PTS_FILE_PATH = os.path.join(OUTPUT_DIR, PROC_HISTORY_PTS_FILE_NAME)
    UTILITY_DIR = os.path.join(UTILITY_DIR)
    INVENTION_DIR = os.path.join(INVENTION_DIR)
