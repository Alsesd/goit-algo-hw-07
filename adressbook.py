from collections import UserDict
from datetime import datetime, timedelta

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
            datetime.strptime(value, "%d.%m.%Y")
            self.value = value
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def string_to_date(self, value):
        return datetime.strptime(value, "%d.%m.%Y").date()
    
    def date_to_string(self, value):
        return datetime.strftime(value, "%d.%m.%Y")

class Name(Field):
    def __init__(self, value):
        super().__init__(value)
    


class Phone(Field):
    def __init__(self, value, required=False):
        super().__init__(value)
        if not len(value) == 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits long")
        
    def __str__(self):
        return str(self.value)


class Record:
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
            new_phone = Phone(new_phone) 
            self.find_phone(old_phone).value = new_phone.value 
    
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError('No number found')

    def __str__(self):
        phones_str = '; '.join(str(p.value) for p in self.phones)
        birthday_str = self.birthday.value if self.birthday else "Not set" 
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def get_upcoming_birthdays(self, days=7):
        if not self.data:
            return 'No contacts found'
        upcoming_birthdays = []
        today = datetime.today().date()
        for record in self.data.values():
            if record.birthday is None:
                continue
            birthday_this_year = record.birthday.string_to_date(record.birthday.value)
            birthday_this_year = birthday_this_year.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year+1)
            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = self.__adjust_for_weekend(birthday_this_year)
                congratulation_date_str = record.birthday.date_to_string(birthday_this_year)
                upcoming_birthdays.append(f'{record.name.value}: {congratulation_date_str}')
        return upcoming_birthdays

    def __find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def __adjust_for_weekend(self,birthday):
        if birthday.weekday() >= 5:
            return self.__find_next_weekday(birthday, 0)
        return birthday
    
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

