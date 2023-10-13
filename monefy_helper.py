import sqlite3
import os
import csv
import uuid
import random

from datetime import datetime
from Crypto.Cipher import AES

class MonefyDatabase:
    def __init__(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
            conn.close()
        except Exception as ex:
            raise Exception("Error encountered when connecting to DB", ex)
        self.db_file = db_file
        self.accounts = self.__query_output_to_key_value_dict("SELECT title, _id FROM accounts;", 'title', '_id')
        self.categories = self.__query_output_to_key_value_dict("SELECT title, _id FROM categories WHERE deletedOn IS NULL;", 'title', '_id')

    def info(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
        table_sizes = {}
        for table_name, table_sql in cursor.fetchall():
            cursor.execute("SELECT COUNT(*) FROM {}".format(table_name))
            table_size = cursor.fetchone()[0]
            table_sizes[table_name] = table_size
        cursor.close()
        conn.close()
        return table_sizes

    def __query_output_to_key_value_dict(self, query, key, value):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        headers = [i[0] for i in cursor.description]
        key_index = headers.index(key)
        value_index = headers.index(value)
        return {row[key_index]: row[value_index] for row in rows}

    def __convert_date_to_unix_timestamp(self, date):
        # Create a random millisecond value
        milliseconds = random.randint(0, 999)
        # Convert the date into a unix timestamp with the random millisecond value.
        return round(datetime.strptime(date + f" 12:34:56.{milliseconds:03d}", "%d/%m/%Y %H:%M:%S.%f").timestamp() * 1000)

    def get_account_id(self, account):
        # Look up the account_id based on the account name.
        if account in self.accounts:
            return self.accounts[account]

    def get_category_id(self, category):
        # Look up the category_id based on the category name.
        if category in self.categories:
            return self.categories[category]

    def get_transaction_count(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM transactions")
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count

    def upload_transactions(self, csv_path):

        initial_count = self.get_transaction_count()

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                account_id = self.get_account_id(row['account'])
                category_id = self.get_category_id(row['category'])
                amount = abs(float(row['amount'].replace(',','')) * 1000)
                createdOn = self.__convert_date_to_unix_timestamp(row['date'])
                note = row['description']
                scheduleId = None
                deletedOn = None
                _id = str(uuid.uuid4())
                localHashCode = random.randint(-2147483648, 2147483647)
                remoteHashCode = localHashCode
                hashCode = 0

                transaction = (account_id, "0", int(amount), category_id, createdOn, note, scheduleId, deletedOn, _id, localHashCode, remoteHashCode, hashCode)
                print(transaction)
                cursor.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", transaction)


        conn.commit()
        cursor.close()
        conn.close()

        new_count = self.get_transaction_count()
        print(f'[{new_count - initial_count}] rows have been added to the transactions table.')

    def update_note_in_transactions(self, old_note, new_note):

        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Find records with the old note value
        cursor.execute(f'SELECT * FROM transactions WHERE note = "{old_note}"')
        records = cursor.fetchall()

        # Update the note value for each record found
        for record in records:
            record_id = record[8]  # Assuming '_id' is the 9th field in the table
            cursor.execute(f'UPDATE transactions SET note = "{new_note}" WHERE _id = "{record_id}"')

        records_length = len(records)
        print(f'[{records_length}] records were updated by replacing "{old_note}" with "{new_note}".')

        # Commit the changes to the database and close the connection
        conn.commit()
        conn.close()

    def update_notes_remove_trailing_whitespace(self):

        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Find records with trailing whitespace in the note field
        cursor.execute(f'SELECT * FROM transactions WHERE note LIKE "% "')
        records = cursor.fetchall()

        # Update the note value for each record found
        for record in records:
            record_id = record[8]  # '_id' is the 9th field in the table
            old_note = record[5]  # 'note' is the 6th field in the table
            new_note = old_note.rstrip()  # Remove trailing whitespace
            try:
                cursor.execute(f'UPDATE transactions SET note = "{new_note}" WHERE _id = "{record_id}"')
            except:
                print(f'Ran into error for note [{new_note}]. Likely includes a character that breaks the SQL.')

        records_length = len(records)
        print(f'[{records_length}] records were updated by removing trailing whitespace".')

        # Commit the changes to the database
        conn.commit()
        conn.close()


class MonefyCrypto:

    # This is the key value used in the Monefy APK.
    __key = 'MyDifficultPassw'

    @staticmethod
    def encrypt_file(input_file_path, output_file_path):
        try:
            cipher = AES.new(MonefyCrypto.__key.encode(), AES.MODE_ECB)
            with open(input_file_path, 'rb') as input_file:
                input_bytes = input_file.read()
            output_bytes = cipher.encrypt(input_bytes)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(output_bytes)

        except Exception as ex:
            raise Exception("Error encrypting file", ex)

    @staticmethod
    def decrypt_file(input_file_path, output_file_path):
        try:
            cipher = AES.new(MonefyCrypto.__key.encode(), AES.MODE_ECB)
            with open(input_file_path, 'rb') as input_file:
                input_bytes = input_file.read()
            output_bytes = cipher.decrypt(input_bytes)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(output_bytes)

        except Exception as ex:
            raise Exception("Error decrypting file", ex)