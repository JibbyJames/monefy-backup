import shutil
import csv
from datetime import datetime, timedelta

from datetime import datetime
from monefy_helper import MonefyDatabase, MonefyCrypto

decrypted_file_path = 'monefy_backup_decrypted.db'

now = datetime.now()
new_encrypted_file_path = f'{now.strftime("%m%d%H%M%S")}'
MonefyCrypto.encrypt_file(decrypted_file_path, new_encrypted_file_path)

gdrive_folder = 'C:\\Users\\James\\Google Drive\\Backups\\Monefy'
shutil.copy(new_encrypted_file_path, gdrive_folder)

