import json
import re
from jsonDB import JsonDB
from rich import print

class PeopleDB(JsonDB):
    """
    Specialized DB class for handling 'user' records in JSON format.
    """
    def __init__(self, filepath):
        super().__init__(filepath, key_field="user.username")

    def find_by_name(self, first_name=None, last_name=None):
        """
        Convenience method to query people by first/last name.
        """
        results = []
        for record in self.data:
            user = record.get("user", {})
            name = user.get("name", {})
            
            if first_name and name.get("first", "").lower() != first_name.lower():
                continue
            if last_name and name.get("last", "").lower() != last_name.lower():
                continue
            results.append(record)

        return results

    def find_by_state(self, state):
        """
        Convenience method to query people by state.
        """
        results = []
        for record in self.data:
            user = record.get("user", {})
            location = user.get("location", {})
            record_state = location.get("state", "").lower()

            if record_state == state.lower():
                results.append(record)

        return results

    def find_by_city(self, city):
        """
        Convenience method to query people by city.
        """
        results = []
        for record in self.data:
            user = record.get("user", {})
            location = user.get("location", {})
            record_city = location.get("city", "").lower()

            if record_city == city.lower():
                results.append(record)

        return results

    def create_person(self, person_data):
        """
        A more domain-specific create method.
        check phone, SSN formats, etc.
        Then call self.create(...) from the base class.
        """
        user = person_data.get("user", {})
        if not user:
            raise ValueError("Must provide a 'user' key in the person data.")
        
        # Validation checks for SSN and phone number formats
        if not self._is_valid_ssn(user.get("SSN", "")):
            raise ValueError("Invalid SSN format. Expected format: XXX-XX-XXXX")
        if not self._is_valid_phone(user.get("phone", "")):
            raise ValueError("Invalid phone format. Expected format: (XXX)-XXX-XXXX")
        
        return self.create(person_data)
    
    def delete_person(self, username):
        """
        A more domain-specific delete method.
        check if the user exists before deletion.
        Then call self.delete(...) from the base class.
        """
        # Assuming username is a unique identifier in the 'user' field
        matches = self.read(**{"user.username": username})
        if not matches:
            raise ValueError(f"Username '{username}' not found in the database.")

        deleted = self.delete(username)
        print(f"Deleted record: {deleted}")
        return deleted
    
    def update_username(self, current_username, new_username):
        """
        A more domain-specific update method.
        check if the new username is valid and not already taken.
        Then call self.update(...) from the base class.
        """
        if self.read(**{"user.username": new_username}):
            raise ValueError(f"Username '{new_username}' is already in use.")

        # Get the current user record
        matches = self.read(**{"user.username": current_username})
        if not matches:
            raise ValueError(f"Username '{current_username}' not found in the database.")

        # Update the username
        record = matches[0]
        record["user"]["username"] = new_username
        self._save_data()
        print(f"[green]Updated username:[/green] {current_username} → {new_username}")
        return record
    
    def _is_valid_ssn(self, ssn):
        """
        Validate SSN format: XXX-XX-XXXX
        """
        pattern = re.compile(r"^\d{3}-\d{2}-\d{4}$")
        return bool(pattern.match(ssn))

    def _is_valid_phone(self, phone):
        """
        Validate phone format: (XXX)-XXX-XXXX
        """
        pattern = re.compile(r"^\(\d{3}\)-\d{3}-\d{4}$")
        return bool(pattern.match(phone))

if __name__ == "__main__":
    print("Running peopleDB.py")

    # Example usage of the PeopleDB class
    db = PeopleDB("./random_people.10000.json")

    print("[bold cyan]First 5 usernames in the database:[/bold cyan]")
    for record in db.data[:5]:
        user = record.get("user", {})
        print(user.get("username"))

    # Create a new test user
    new_user = {
        "user": {
            "username": "testuser123",
            "name": {"first": "Test", "last": "User"},
            "email": "testuser123@example.com",
            "phone": "(555)-555-5555",
            "SSN": "123-45-6789",
            "location": {"city": "Testville", "state": "Testland"}
        }
    }

    try:
        print("\n[bold yellow]Creating a new test user...[/bold yellow]")
        db.create_person(new_user)
    except ValueError as e:
        print(f"[red]Create failed:[/red] {e}")

    # Update the username
    try:
        print("\n[bold yellow]Updating username...[/bold yellow]")
        db.update_username("testuser123", "testuser456")
    except ValueError as e:
        print(f"[red]Update failed:[/red] {e}")

    # Delete the user
    try:
        print("\n[bold yellow]Deleting test user...[/bold yellow]")
        db.delete_person("testuser456")
    except ValueError as e:
        print(f"[red]Delete failed:[/red] {e}")