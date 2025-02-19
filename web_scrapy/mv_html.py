import os
import shutil
import re
from common_def import FilePathDef

class PatentFileOrganizer:
    @staticmethod
    def generate_folder_path(pnr):
        match = re.match(r'(CN\d+)([A-Z]?\d{0,2})$', pnr) 
        if not match:
            return "invalid_path", "invalid_patent_type"
        
        base_num = match.group(1)
        suffix = match.group(2)

        patent_type = "utility"
        if suffix:
            if len(suffix) == 1 and suffix in ("A", "B", "C"):
                patent_type = "invention"
            elif len(suffix) == 2 and suffix in ("A8", "A9", "B8", "B9"):
                patent_type = "invention"
        
        number_part = base_num[2:].zfill(9)
        folder_path = os.path.join(
            f"CN{number_part[:3]}",
            f"CN{number_part[:5]}"
        )
        
        return folder_path, patent_type 
    
    @classmethod
    def locate_patent_file(cls, publn):
        folder_path, patent_type = cls.generate_folder_path(publn)
        
        target_base = FilePathDef.INVENTION_DIR if patent_type == "invention" else FilePathDef.UTILITY_DIR
        
        possible_path = os.path.join(
            target_base,
            folder_path,
            f"{publn}.html"
        )
        if os.path.exists(possible_path):
            return possible_path
        return None


    @classmethod
    def organize_downloaded_file(cls, publn, src_path):

        folder_path, patent_type = cls.generate_folder_path(publn)
        target_base = FilePathDef.INVENTION_DIR if patent_type == "invention" else FilePathDef.UTILITY_DIR
        target_dir = os.path.join(target_base, folder_path)
        os.makedirs(target_dir, exist_ok=True)
        
        target_path = os.path.join(target_dir, f"{publn}.html")
        if os.path.exists(target_path):
            duplicate_dir = os.path.join(target_base, "duplicates")
            os.makedirs(duplicate_dir, exist_ok=True)
            shutil.move(src_path, os.path.join(duplicate_dir, f"{publn}.html"))
        else:
            shutil.move(src_path, target_path)
        return target_path






