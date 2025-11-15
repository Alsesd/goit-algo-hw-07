from functools import wraps
from AdressBook import *

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Give me name please"
        except KeyError:
            return "Contact not found"

    return inner

def check_record(func):
    @wraps(func)
    def inner(args, book):
        name = args[0]
        record = book.find(name)
        if record is None:
            raise KeyError
        return func(args, book)
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
@check_record
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    record.edit_phone(record.phones[0].value, phone)
    return "Contact updated."

@input_error
@check_record
def name_contact(args, book):
    name, *_ = args
    record = book.find(name)
    return f"{name}: {', '.join(phone.value for phone in record.phones)}"

@input_error
@check_record
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return 'Birthday added'

@input_error
@check_record
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    return record.birthday.value

def get_upcoming_birthdays(book):
    return book.get_upcoming_birthdays()


def list_contacts(book):
    if not book.data:
        return 'No contacts found.'
    return book

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close" |"exit":
                print("Good bye!")
                break

            case "hello":
                print("How can I help you?")

            case "add":
                print(add_contact(args, book))

            case "change":
                print(change_contact(args, book))

            case "phone":
                print(name_contact(args, book))

            case "all":
                print(list_contacts(book))

            case "add-birthday":
                print(add_birthday(args, book))    

            case "show-birthday":
                print(show_birthday(args, book))

            case "birthdays":
                print(get_upcoming_birthdays(book))

            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()