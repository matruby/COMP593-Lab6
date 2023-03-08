
import hashlib
import os 
import requests 
import subprocess
import sys 

def main():
    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    file_url = "http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256"
    resp_msg = requests.get(file_url)

    if resp_msg.status_code == requests.codes.ok:
        # Get the file hash 
        resp_text = resp_msg.text
        # Split up the response and just get the file hash
        split_text = resp_text.split()
        file_hash = split_text[0]
    else:
        # If URL Fails exit the program
        print(f"Code aborting due to: {resp_msg.status_code}\n!Bad Link!")
        sys.exit()

    return file_hash 

def download_installer():
    # Provide the url and make a get request to download the file
    vlc_file_url = "http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe"
    get_exe = requests.get(vlc_file_url)

    # Ensure the request was completed correctly and return the downloaded content
    if get_exe.status_code == requests.codes.ok:
        file_content = get_exe.content
    else:
        # If the link to the download fails output error message and exit
        print(f"Code aborting due to: {get_exe.status_code}\n!Download Link Failed!")
        sys.exit()
        
    return file_content 

def installer_ok(installer_data, expected_sha256):
    # SHA 256 Hash for installer_data
    file_hash = hashlib.sha256(installer_data).hexdigest()

    # Make sure the hashes match
    if file_hash == expected_sha256:
        return 1
    else:
        print("Code aborted due to:\n!Hashes not Matching!")

def save_installer(installer_data):
    # Save the installer to the temp directory 
    with open(r'C:\Users\rubes\AppData\Local\Temp\vlc_installer.exe', 'wb') as file:
        file.write(installer_data)
    # Return the location of the intstall 
    return r'C:\Users\rubes\AppData\Local\Temp\vlc_installer.exe'

def run_installer(installer_path):
    # Run the installer silently 
    subprocess.run([installer_path, '/L=1033', '/S'])
    return 1
    
def delete_installer(installer_path):
    # Remove the installer 
    os.remove(installer_path)
    return 1

if __name__ == '__main__':
    main()



