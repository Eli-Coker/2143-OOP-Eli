import json
from rich import print

class JsonDB:
    """
    Base class for a simple JSON "database."

    Attributes:
        filepath (str): Path to the JSON file on disk.
        data (any): The loaded JSON data (e.g., list, dict).
    """

    def __init__(self, filepath, key_field=None):
        """
        Initialize the DB with a path to the JSON file.
        """
        self.filepath = filepath
        self.key_field = key_field
        self.data = []
        self._load_data()
        self.current = 0

    def _load_data(self):
        """
        Internal helper to load JSON data from the file into self.data.
        Handle exceptions and set self.data appropriately if file is missing/corrupted.
        """
        try:
            with open(self.filepath) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"[red]File not found: {self.filepath}[/red]")
            self.data = []

    def _save_data(self):
        """
        Internal helper to save self.data back to the JSON file.
        """
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"[red]Error saving data: {e}[/red]")

    def create(self, record):
        """
        Insert a new record into self.data.
        'record' could be a dict or some structure that matches the data layout.
        Return the inserted record or some identifier.
        """
        self.data.append(record)
        self._save_data()
        return record
    
    def atEnd(self):
        """
        Testing to see if we are at the end of the data.
        Return True if we are at the end, False otherwise.
        """
        return self.current == len(self.data) - 1

    def getNext(self):
        record = self.data[self.current]
        self.current += 1
        if self.current >= len(self.data):
            self.current = 0
        return record

    def _get_nested_value(self, record, key_path):
        """
        helper for getting a nested value from a record
        """
        keys = key_path.split('.')
        value = record
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value.get(key)
            else:
                return None
        return value

    def read(self, **filters):
        """
        Read/search the database.
        E.g., read(name="Teresa", city="Los Angeles") might filter by matching fields.
        Return a list of matching records or a single record.
        """
        results = []
        for record in self.data:
            if all(record.get(k) == v for k, v in filters.items()):
                results.append(record)
        return results

    def update(self, record_id, updated_data):
        """
        Update an existing record by some identifier.
        Return the updated record, or raise an error if not found.
        """
        if not self.key_field:
            raise ValueError("key_field must be set to use update()")

        for i, record in enumerate(self.data):
            value = self._get_nested_value(record, self.key_field)
            if value == record_id:
                self.data[i].update(updated_data)
                self._save_data()
                return self.data[i]

        raise ValueError(f"Record with ID {record_id} not found.")

    def delete(self, record_id):
        """
        Remove a record by its identifier.
        Return the deleted record, or raise an error if not found.
        """
        if not self.key_field:
            raise ValueError("key_field must be set to use delete()")

        for i, record in enumerate(self.data):
            value = self._get_nested_value(record, self.key_field)
            if value == record_id:
                deleted_record = self.data.pop(i)
                self._save_data()
                return deleted_record

        raise ValueError(f"Record with ID {record_id} not found.")


if __name__ == "__main__":
    print("Running jsonDB.py")

    # Example usage of the JsonDB class
    dbptr = JsonDB("./random_people.10000.json", key_field="user.username")

    for record in dbptr.data:
        user = record.get("user", {})
        username = user.get("username", None)
        if username:
            print(username)