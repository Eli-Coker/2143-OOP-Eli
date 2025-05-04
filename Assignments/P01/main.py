from InquirerPy import inquirer
from rich.console import Console
from peopleDB import PeopleDB

console = Console()
db = PeopleDB("random_people.10000.json")

def submenu_create():
    """
    Prompt the user for new user details and add them to the database.
    Fields include username, first name, last name, email, phone, SSN, city, and state.
    """
    username = console.input("New username: ")
    first = console.input("First name: ")
    last = console.input("Last name: ")
    email = console.input("Email: ")
    phone = console.input("Phone (format: (XXX)-XXX-XXXX): ")
    ssn = console.input("SSN (format: XXX-XX-XXXX): ")
    city = console.input("City: ")
    state = console.input("State: ")

    new_user = {
        "user": {
            "username": username,
            "name": {"first": first, "last": last},
            "email": email,
            "phone": phone,
            "SSN": ssn,
            "location": {"city": city, "state": state}
        }
    }

    try:
        db.create_person(new_user)
        console.print("[green]User created successfully![/green]")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")

def submenu_search():
    """
    Prompt the user to search for users by name, city, or state.
    Display the usernames of matching records.
    """
    choice = inquirer.select(
        message="Search by:",
        choices=["Name", "City", "State", "Back"]
    ).execute()

    if choice == "Name":
        first = console.input("First name (or leave blank): ")
        last = console.input("Last name (or leave blank): ")
        results = db.find_by_name(first, last)
    elif choice == "City":
        city = console.input("Enter city: ")
        results = db.find_by_city(city)
    elif choice == "State":
        state = console.input("Enter state: ")
        results = db.find_by_state(state)
    else:
        return

    if results:
        for r in results:
            console.print(r["user"]["username"])
    else:
        console.print("[yellow]No users found.[/yellow]")

def submenu_update():
    """
    Prompt the user for the current username and new username.
    Update the username in the database.
    """
    current = console.input("Current username: ")
    new = console.input("New username: ")
    try:
        db.update_username(current, new)
        console.print("[green]Username updated![/green]")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")

def submenu_delete():
    """
    Prompt the user for the username to delete.
    Delete the user from the database.
    """
    username = console.input("Username to delete: ")
    try:
        db.delete_person(username)
        console.print("[green]User deleted successfully.[/green]")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")

def submenu_view_usernames():
    """
    Display all of the usernames in the database.
    """
    console.print("\n[blue] Usernames:[/blue]")
    for record in db.data:
        user = record.get("user", {})
        console.print(user.get("username", "<no username>"))

def main_menu():
    """
    Main menu loop for the PeopleDB application.
    Provides options to view usernames, search, add, update, delete, or exit.
    """
    while True:
        choice = inquirer.select(
            message="PeopleDB Menu:",
            choices=[
                "View all usernames",
                "Find by name/city/state",
                "Add new person",
                "Update username",
                "Delete person",
                "Exit"
            ]
        ).execute()

        if choice == "View all usernames":
            submenu_view_usernames()
        elif choice == "Find by name/city/state":
            submenu_search()
        elif choice == "Add new person":
            submenu_create()
        elif choice == "Update username":
            submenu_update()
        elif choice == "Delete person":
            submenu_delete()
        elif choice == "Exit":
            console.print("[pink]Goodbye![/pink]")
            break

if __name__ == "__main__":
    main_menu()