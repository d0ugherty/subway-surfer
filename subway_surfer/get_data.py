import requests
import os
import zipfile
import shutil
from io import BytesIO

"""
    This script:
    1. Retrieves a zip file from the specified URL
    2. Unzips the folder(s) and extracts the contents
    3. Converts the .txt files to .csv
    4. Moves the .csv files into the proper directory for use with the application

    TO-DO: 
    1. Retrieve NJT data (if possible)
    2. Automate the time replacements in stop_times.csv
"""

url = "https://www3.septa.org/developer/gtfs_public.zip"
extract_dir = "data/septa/"
# retrieve zip file
print(f'Getting zip file from {url}')
response = requests.get(url, allow_redirects=True)

# if response is successful unzip the file
if response.status_code == 200:
    print(f'File retrieved')
    print(f'Extracting all zip file')
    with zipfile.ZipFile(BytesIO(response.content)) as zip_parent_ref:
        zip_parent_ref.extractall(extract_dir)
        for file in zip_parent_ref.namelist():
            file_path = os.path.join(extract_dir, file)
            print(f'file_path : {file_path}')
            if zipfile.is_zipfile(file_path):
                print(f'Extracting child ZIP file: {file}')
                with zipfile.ZipFile(file_path) as zip_child_ref:
                    child_extract_dir = os.path.join(extract_dir, os.path.splitext(file)[0])
                    os.makedirs(child_extract_dir, exist_ok=True)
                    zip_child_ref.extractall(child_extract_dir)
else:
    print(f"Failed to download the file: HTTP {response.status_code}")


# convert to csv
# move into data folder
rail_dir = "data/septa/google_rail/"
for filename in os.listdir(rail_dir):
    if filename.endswith('.txt'):
        current_path = os.path.join(rail_dir, filename)
        new_file = os.path.join(rail_dir, filename.replace('.txt', '.csv'))
        os.rename(current_path, new_file)
        shutil.move(new_file, extract_dir)


