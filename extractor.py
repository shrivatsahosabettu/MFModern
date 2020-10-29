from pathlib import Path
from global_file import *

p = Path(folder_path)
for child in p.rglob("*.*"):
    print(child)

    