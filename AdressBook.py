from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value, required=True):
        if required and not value:
            raise ValueError("This field is required")
        self.value = value

    
    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y').date()

        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
    


class Phone(Field):
   def __init__(self, value, required=False):
        super().__init__(value)
        if not len(value) == 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits long")


class Record: #add phone, delete phone, change phone, search phone
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        if self.birthday == None:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones.remove(self.find_phone(phone))

    def edit_phone(self, old_phone, new_phone):
            if self.find_phone(old_phone) == None:
                raise ValueError('Number not found') 
            self.find_phone(old_phone).value = Phone(new_phone)
    
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError('No number found')

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
    pass
        


class AddressBook(UserDict): #add record, delete record, search record
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name, None)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        result = ""
        for record in self.data.values():
            result += str(record) + "\n"
        return result.strip()

