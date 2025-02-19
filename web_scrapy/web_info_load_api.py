from web_parser import PatentInfo
from proc_history_manager import is_pt_in_proc_history
import os
import requests
from common_def import HTML_DIR
from common_def import HTML_DOWNLOAD_DIR
from mv_html import PatentFileOrganizer
from lxml import etree


# Put all files which contain the publication number of patents that to be processed in one directory

def patent_info_proc(pt_tree):
    patent_info = PatentInfo()
    patent_info.load_by_data(pt_tree)
    patent_info.output_data()

def get_patent_html(publn: str) -> str:
    print(f"Downloading {publn}")
    pt_nmb = publn.replace(r".html", "")
    url = f"https://patents.google.com/patent/{pt_nmb}"
    response = requests.get(url, timeout=10)
    response.encoding = "utf-8"
    
    if response.status_code == 200 and len(response.text) > 0:
        html_content = response.text
        temp_path = os.path.join(HTML_DOWNLOAD_DIR, f"{publn}.html")
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        PatentFileOrganizer.organize_downloaded_file(publn, temp_path)
        return html_content
    else:
        print(f"Download error: {response.status_code}")
        return None


def load_patent_info_file(file_path: str, load_proc):
    with open(file_path, "r") as fs:
        print("file path %s format" % file_path)
        for line in fs:
            publn = line.replace("\n", "")
            print("publn: {}".format(publn))

            # skip the processed patent
            if is_pt_in_proc_history(publn):
                print("pt {} is already processed".format(publn))
                continue

            # check if the html file exists
            html_path = PatentFileOrganizer.locate_patent_file(publn)
            for root, dirs, files in os.walk(HTML_DIR):
                if f"{publn}.html" in files:
                    html_path = os.path.join(root, f"{publn}.html")
                    break
            
            # file exists: load the patent info
            if html_path and os.path.exists(html_path):
                print(f"Found HTML at: {html_path}")
                with open(html_path, "r", encoding="utf-8") as html_file:
                    html_content = html_file.read()
                
                # parse the html content          
                try:
                    pt_tree = etree.HTML(html_content)
                    if pt_tree is not None:
                        load_proc(pt_tree)
                        continue
                # re-download the html content if parsing failed
                except IndexError as e:
                    print(f"Parsing failed: {html_path}, re-downloading...")
                    os.remove(html_path)
                    html_content = get_patent_html(publn)
            # file not exists: download the html content
            else:
                html_content = get_patent_html(publn)

            # parse the html content
            if html_content is None:
                print(f"can't get html content of {publn}")
                continue

            pt_tree = etree.HTML(html_content)
            if pt_tree is not None:
                load_proc(pt_tree)
            else:
                print("unvalidated html: {}".format(publn))

def load_patent_input(dir_path: str, load_proc):
    patent_input_path = os.path.join(os.getcwd(), dir_path)
    for dir_v in os.listdir(patent_input_path):
        dir_tmp = os.path.join(dir_path, dir_v)
        if os.path.isdir(dir_tmp):
            # for a directory, continue to traverse the directory
            load_patent_input(dir_tmp, load_proc)
        else:
            # for a file, load the file
            load_patent_info_file(dir_tmp, load_proc)
    pass
