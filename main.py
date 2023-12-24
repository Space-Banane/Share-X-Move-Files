import requests
import time
# Settings
source_url = "https://fs.rjns.dev"
destination_url = "https://files.duckhosting.net/api/user/objects/processed"

source_auth_token = "" # This token has to PULL images
dest_token = "" # This token has to UPLOAD images

# Function to get all files from the source URL
def get_all_files(source_url):
    # ! Assuming the API returns paginated results
    page = 1
    all_files = []

    while True:
        response = requests.get(f"{source_url}/api/user/objects?type=finished&page={page}",headers={'Authorization': 'auth '+source_auth_token})
        resp = response.json()
        print(f"Request Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Failed to get files. Status code: {response.status_code}")
            break
        try:
            files = response.json().get('list', {}).get('data', [])
        except Exception as e:
            print(f"Error decoding JSON: {e}")
            print(f"Response content: {response.text}")
            break

        if not files:
            break

        all_files.extend(files)
        print(str(page)+"/22")
        page += 1
        time.sleep(0.4)
    return all_files

# Function to upload files to the destination URL
def upload_files(files, destination_url):
    for file in files:
        file_name = file.get('identifier')
        print(file_name)
        file_url = file.get('link').strip()  # Remove leading and trailing spaces
        print(file_url)

        if file_name and file_url:
            print("Making request for " + file_name)
            
            try:
                file_response = requests.get(file_url, timeout=10)
                file_response.raise_for_status()  # Check for HTTP errors
                response = requests.post(destination_url, headers={'Authorization': 'upload '+dest_token}, data=file_response.content)
                print(response.text)
                print(f"Uploaded {file_name}: {response.status_code}")
                time.sleep(0.3)
                
            except requests.exceptions.RequestException as e:
                print(f"Error making request for {file_name}: {e}")


all_files = get_all_files(source_url=source_url)
print("Done Downloading Files!")
upload_files(destination_url=destination_url,files=all_files)