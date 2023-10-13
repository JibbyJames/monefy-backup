import shutil
import csv
from datetime import datetime, timedelta

from datetime import datetime
from monefy_helper import MonefyDatabase, MonefyCrypto

decrypted_file_path = 'monefy_backup_decrypted.db'

# Create Monefy Database object
monefy_db = MonefyDatabase(decrypted_file_path)

# Update the record
# old_note = "Subway Lunch "
# new_note = "Subway Lunch"
# monefy_db.update_note_in_transactions(old_note, new_note)

monefy_db.update_notes_remove_trailing_whitespace()
