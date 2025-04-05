import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            if '.venv' not in root and '__pycache__' not in root:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, path)
                ziph.write(filepath, arcname)

with zipfile.ZipFile('deploy.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir('.', zipf)
