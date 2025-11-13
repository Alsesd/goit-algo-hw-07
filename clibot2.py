from AdressBook import *
from datetime import datetime, date, timedelta

def input_error(func):
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

def get_upcoming_birthdays(book, days=7):
    if not book.data:
        return 'No contacts found'
    upcoming_birthdays = []
    today = date.today()
    for record in book.data.values():
        if record.birthday is None:
            continue
        birthday_this_year = record.birthday.value.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = record.birthday.value.replace(year=today.year+1)
        if 0 <= (birthday_this_year - today).days <= days:
            birthday_this_year = adjust_for_weekend(birthday_this_year)
            congratulation_date_str = date_to_string(birthday_this_year)
            upcoming_birthdays.append(f'{record.name.value}: {congratulation_date_str}')
    return upcoming_birthdays

def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday

def date_to_string(date):
    return date.strftime("%d.%m.%Y")

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
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(record.phones[0].value, phone)
    return "Contact updated."

@input_error
def name_contact(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    return f"{name}: {', '.join(phone.value for phone in record.phones)}"

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return 'Birthday added'

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None: 
        raise KeyError
    return record.birthday.value


def list_contacts(book):
    if not book.data:
        return 'No contacts found.'
    return book

def main():
    book = AddressBook()
    adolf = Record('adolf')
    book.add_record(adolf)
    adolf.add_birthday('15.11.2001')
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

