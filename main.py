from peopleDB import PeopleDB
from rich import print

def show_menu():
    print("\n[bold cyan]--- PeopleDB Menu ---[/bold cyan]")
    print("[1] View all usernames")
    print("[2] Find by name")
    print("[3] Find by city")
    print("[4] Find by state")
    print("[5] Add new person")
    print("[6] Update username")
    print("[7] Delete person")
    print("[0] Exit")

def main():
    db = PeopleDB("random_people.10000.json")

    while True:
        show_menu()
        choice = input("\n[bold green]Enter choice:[/bold green] ").strip()

        if choice == "1":
            for record in db.data[:20]:  # Limit to first 20 for readability
                user = record.get("user", {})
                print(user.get("username", "<no username>"))

        elif choice == "2":
            first = input("First name (or leave blank): ")
            last = input("Last name (or leave blank): ")
            results = db.find_by_name(first, last)
            for r in results:
                print(r["user"]["username"])

        elif choice == "3":
            city = input("Enter city: ")
            results = db.find_by_city(city)
            for r in results:
                print(r["user"]["username"])

        elif choice == "4":
            state = input("Enter state: ")
            results = db.find_by_state(state)
            for r in results:
                print(r["user"]["username"])

        elif choice == "5":
            username = input("New username: ")
            first = input("First name: ")
            last = input("Last name: ")
            email = input("Email: ")
            phone = input("Phone (format: (XXX)-XXX-XXXX): ")
            ssn = input("SSN (format: XXX-XX-XXXX): ")
            city = input("City: ")
            state = input("State: ")

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
                print("[green]User created successfully![/green]")
            except ValueError as e:
                print(f"[red]Error:[/red] {e}")

        elif choice == "6":
            current = input("Current username: ")
            new = input("New username: ")
            try:
                db.update_username(current, new)
            except ValueError as e:
                print(f"[red]Error:[/red] {e}")

        elif choice == "7":
            username = input("Username to delete: ")
            try:
                db.delete_person(username)
            except ValueError as e:
                print(f"[red]Error:[/red] {e}")

        elif choice == "0":
            print("[bold magenta]Goodbye![/bold magenta]")
            break

        else:
            print("[red]Invalid option.[/red]")

if __name__ == "__main__":
    main()