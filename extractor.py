from pathlib import Path
from global_file import *

components_path = Path(folder_path)
for extracted_path in components_path.rglob("*.*"):
    str_extr_path = str(extracted_path)
    file_name = str_extr_path[len(str_extr_path) - (''.join(reversed(str_extr_path)).find('/')):]
    file_path_dict[file_name] = str_extr_path

   
