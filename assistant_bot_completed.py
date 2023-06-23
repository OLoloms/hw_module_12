from collections import UserDict
from datetime import datetime, timedelta
import json
import pickle

class AdressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.name] = record

    def iterator(self, n):
        keys = list(self.data.keys())
        total_records = len(keys)
        current_index = 0

        while current_index < total_records:
            batch_keys = keys[current_index:current_index + n]
            batch_records = [str(self.data[key]) for key in batch_keys]
            current_index += n
            yield batch_records
    
    def save_to_file(self, file_name='hw_module_12/test.bin'):
        with open(file_name, 'wb') as f:
            pickle.dump(self.data, f)

    def read_from_file(self, file_name='hw_module_12/test.bin'):
        with open(file_name, 'rb') as f:
            return pickle.load(f)

class Record:
    def __init__(self, name, *field, birthday=None) -> None:
        self.name = name
        self.field = list(field) or []
        self.birthday = birthday.value

    def days_to_birthday(self):
        if self.birthday:
            birthday = datetime.strptime(self.birthday, '%d %B %Y')

            current_day = datetime.now().date()

            if current_day - datetime(year=datetime.now().year, month=birthday.month, day=birthday.day).date() < timedelta(days=0):
                diff = datetime(year=datetime.now().year, month=birthday.month, day=birthday.day).date() - current_day
            elif current_day - datetime(year=datetime.now().year, month=birthday.month, day=birthday.day).date() == timedelta(days=0):
                return 'Todays is your birthday'
            else:
                diff = datetime(year=datetime.now().year+1, month=birthday.month, day=birthday.day).date() - current_day
            return diff.days
        else:
            return "Birthday isn't set"
        
    def __str__(self):
        phones_list = [phone.value for phone in self.field]
        return f'Name: {self.name.name}, Phone: {phones_list}, Birthday: {self.birthday}'
    

class Field:
    def __init__(self, data):
        self.data = data.data

    def find_match(self, name=None, phone=None):
        if name and phone:
            result = []
            records = [value for value in self.data.values() if name in self.data.keys()]
            if not records:
                return "Nothing hasn't finded"
            for value in records:
                phones = value.field
                for number in phones:
                    if phone in str(number):
                        result.append(str(value))
            if result:
                return result
            else:
                return "Nothing hasn't finded"
        elif name:
            result = []
            for key in self.data:
                if name in key: 
                    result.append(str(self.data[key]))
            if result:
                return result
            else:
                return "Nothing hasn't finded"
        elif phone:
            result = []
            for value in self.data.values():
                phones = value.field
                for number in phones:
                    if phone in str(number):
                        result.append(str(value))
            if result:
                return result
            else:
                return "Nothing hasn't finded"
        else:
            return "Haven't choosed the parametrs of searching"

class Name:
    def __init__(self, name) -> None:
        self.name = name

class Phone:
    def __init__(self) -> None:
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if len(new_value) == 13:
            self.__value = new_value
            print('Phone number has saved')
        else:
            print('Incorrect format number')

    def __str__(self):
        return self.__value

class Birtday:
    def __init__(self) -> None:
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
        data_list = new_value.split(' ')
        if 0 < int(data_list[0]) < 32 and data_list[1] in months and len(data_list[2]) == 4:
            self.__value = new_value
            print('Birthday has saved')
        else:
            print('Incorrect formar record')

name_1 = Name('Sergij')
phone_1_a = Phone()
phone_1_a.value = '+380988623491'
phone_1_b = Phone()
phone_1_b.value = '+380988699491'
birthday_1 = Birtday()
birthday_1.value = '10 January 2021'
rec_1= Record(name_1, phone_1_a, phone_1_b, birthday=birthday_1)
name_2 = Name('Alina')
phone_2 = Phone()
phone_2.value = '+380988623493'
birthday_2 = Birtday()
birthday_2.value = '10 May 2021'
rec_2 = Record(name_2, phone_2, birthday=birthday_2)
name_3 = Name('Anton')
phone_3 = Phone()
phone_3.value = '+380988623411'
birthday_3 = Birtday()
birthday_3.value = '12 May 2021'
rec_3 = Record(name_3, phone_3, birthday=birthday_3)
ab = AdressBook()
ab.add_record(rec_1)
ab.add_record(rec_2)
ab.add_record(rec_3)
finder = Field(ab)
print(finder.find_match(phone='+3'))


