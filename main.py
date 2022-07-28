ID_LENGTH = 4
NUM_OF_DIGITS_LENGTH = 5

FIRST_NAME_KEY = 0x86B7
SECOND_NAME_KEY = 0x9E60
PHONE_KEY = 0x5159
TIME_KEY = 0xD812
MISC_KEY = 0x6704

class Contact:

    def __init__(self, id, first_name, second_name, phone, time, misc):
        self.id = id
        self.first_name = first_name
        self.second_name = second_name
        self.phone = phone
        self.time = time
        self.misc = misc

    def __repr__(self):
        return f"id: {self.id}, first_name: {self.first_name}, second_name: {self.second_name}, phone: {self.phone}," \
               f"time: {self.time}"


def read_encoded_line(line):
    """
    Parses line into (id, value) pairs
    :param line:
    :return:
    """
    results = dict()
    start_idx = 0

    while start_idx < len(line):
        id = line[start_idx: start_idx + ID_LENGTH]
        name_length = int(line[start_idx + ID_LENGTH: start_idx + ID_LENGTH + NUM_OF_DIGITS_LENGTH], 16)
        name = line[start_idx + ID_LENGTH + NUM_OF_DIGITS_LENGTH: start_idx + ID_LENGTH + NUM_OF_DIGITS_LENGTH + name_length]
        results[id] = name

        start_idx += ID_LENGTH + NUM_OF_DIGITS_LENGTH + name_length

    return results

if __name__ == '__main__':
    encoded_contact_info_file = open("ex_v8.txt", "r")

    decoded_results = {
        FIRST_NAME_KEY: dict(),
        SECOND_NAME_KEY: dict(),
        PHONE_KEY: dict(),
        TIME_KEY: dict(),
        MISC_KEY: dict()
    }

    while current_line := encoded_contact_info_file.readline().rstrip():
        line_key = int(current_line[:4], 16)
        current_line = current_line[4:]

        decoded_results[line_key] = read_encoded_line(current_line)

    encoded_contact_info_file.close()
