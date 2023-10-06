# todo handle!!
import pandas as pd

def get_user_input(prompt):
    return input(prompt)


def id_exception_handler(func):
    def wrapper(self, *args, **kwargs):
        while True:
            try:
                return func(self, *args, **kwargs)
            except (SerialNotFound, IDNotFound) as e:
                user_input = get_user_input(f"{str(e)} Enter new value, or 's' to skip: ")
                if user_input.lower() == 's':
                    return None
                kwargs['replacement_value'] = user_input  # Provide the replacement_value for the next attempt
    return wrapper


# def id_exception_handler(func):
#     def wrapper(self, *args, **kwargs):
#         try:
#             return func(self, *args, **kwargs)
#         except (SerialNotFound, IDNotFound) as e:
#             user_input = input(f"{str(e)} Enter new value, or 's' to skip: ")
#             if user_input.lower() == 's':
#                 return None  # or whatever value is appropriate to signify a skip
#             # Replace the first argument (the ID or serial) with the new user input:
#             args = (user_input,) + args[1:]
#             # Re-call func with the updated arguments and the same keyword arguments:
#             return func(self, *args, **kwargs)
#
#     return wrapper


#
# class SerialNotFound(Exception):
#     def __init__(self, radio_id):
#         self.radio_id = radio_id
#
#     def __str__(self):
#         return f"No serial number found for ID {self.radio_id}"
# class IDNotFound(Exception):
#     def __init__(self, id_values):
#         self.id_values = id_values
#
#     def __str__(self):
#         if self.id_values.size == 0:
#             return "No ID found for the given serial."
#         else:
#             return f"Multiple IDs found for the given serial: {', '.join(map(str, self.id_values))}"


class NotFoundException(Exception):
    def __init__(self, value, found_values):
        self.value = value
        self.found_values = found_values


class SerialNotFound(NotFoundException):
    def __str__(self):
        if self.found_values.size == 0 or pd.isna(self.found_values[0]):
            return f"No serial number found for ID {self.value}"
        return f"Multiple serial numbers found for ID {self.value}: {', '.join(map(str, self.found_values))}"


class IDNotFound(NotFoundException):
    def __str__(self):
        if self.found_values.size == 0 or pd.isna(self.found_values[0]):
            return f"No ID found for serial {self.value}"
        return f"Multiple IDs found for serial {self.value}: {', '.join(map(str, self.found_values))}"
