from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


gauth = GoogleAuth()
gauth.LocalWebserverAuth()


def upload_file(file_path, folder_id):
    try:
        drive = GoogleDrive(gauth)
        file_name = os.path.basename(file_path)
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        
        file = drive.CreateFile({'title': f'{file_metadata}'})
        file.SetContentFile(file_path)
        return file.get('id')
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None