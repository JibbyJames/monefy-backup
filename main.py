import shutil
import csv
from datetime import datetime, timedelta

from datetime import datetime
from monefy_helper import MonefyDatabase, MonefyCrypto

# Decrypt monefy backup file.
# encrypted_file_path = 'monefy_corrupted'
encrypted_file_path = 'monefy_backup'
# encrypted_file_path = '0425215926'
decrypted_file_path = 'monefy_backup_decrypted.db'
MonefyCrypto.decrypt_file(encrypted_file_path, decrypted_file_path)

# Create Monefy Database object
# monefy_db = MonefyDatabase(decrypted_file_path)

# db_info = monefy_db.info()
# print(db_info)

# old_note = "Tesco Lunch "
# new_note = "Tesco Lunch"
# monefy_db.update_note_in_transactions(old_note, new_note)

# new_transactions_file_path = 'recovered_data/2022-08-02.csv'
# monefy_db.upload_transactions(new_transactions_file_path)
# monefy_db.upload_transactions(new_transactions_file_path)

# now = datetime.now()
# new_encrypted_file_path = f'{now.strftime("%m%d%H%M%S")}'
# MonefyCrypto.encrypt_file(decrypted_file_path, new_encrypted_file_path)

# gdrive_folder = 'C:\\Users\\James\\Google Drive\\Backups\\Monefy'
# shutil.copy(new_encrypted_file_path, gdrive_folder)

