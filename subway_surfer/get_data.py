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
"""

REPLACEMENTS = [(',24:', ',00:'),
                (',25:', ',01:'),
                (',26:', ',02:'),
                (',27:', ',03:')]

def retrieve_gtfs_zip(agency):
    if agency == 'septa':
        url = "https://www3.septa.org/developer/gtfs_public.zip"
    response = requests.get(url, allow_redirects=True)
    return response

# if response is successful unzip the file
def extract_gtfs(response, agency):
    extract_dir = f'data/{agency}/'
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


# convert to csv
# move into data folder
    
def convert_to_csv(agency):
    agency_dir = f'data/{agency}'
    if agency == 'septa':
        rail_dir = "data/septa/google_rail/"
    for filename in os.listdir(rail_dir):
        if filename.endswith('.txt'):
            current_path = os.path.join(rail_dir, filename)
            new_file = os.path.join(rail_dir, filename.replace('.txt', '.csv'))
            os.rename(current_path, new_file)
            shutil.move(new_file, agency_dir)

# fix time formatting in stop_times
# for scheduling continuity, trips beginning before and ending after midnight 
# will go beyond the 24-hour time format, but datatime types have to be set at 00
# for midnight 
def format_stop_times(agency):
    file_path = f'data/{agency}/stop_times.csv'
    with open(file_path, 'r') as file:
        file_content = file.read()
    for find, replace in REPLACEMENTS:
        file_content = file_content.replace(find, replace)
    with open(file_path, 'w') as file:
        file.write(file_content)
        

if __name__ == '__main__':
    agencies = ['septa']
    for agency in agencies:
        response = retrieve_gtfs_zip(agency)
        if response.status_code == 200:
            extract_gtfs(response, agency)
        else:
            print(f"Failed to download the file: HTTP {response.status_code}")
        print("Converting to CSV")
        convert_to_csv(agency)
        print("Formatting stop times")
        format_stop_times(agency)
