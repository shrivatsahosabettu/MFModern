from pathlib import Path

folder_path = r'/projects/MFModern/dump/'
p = Path(folder_path)
for child in p.rglob("*.*"):
    print(child)