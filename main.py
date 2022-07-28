ID_LENGTH = 4
LENGTH_OF_VALUE_LENGTH = 5

FIRST_NAME_KEY = 0x86B7
LAST_NAME_KEY = 0x9E60
PHONE_KEY = 0x5159
TIME_KEY = 0xD812
MISC_KEY = 0x6704
KEYS = [FIRST_NAME_KEY, LAST_NAME_KEY, PHONE_KEY, TIME_KEY, MISC_KEY]

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
    start = 0

    while start < len(line):
        # Read id
        id_end = start + ID_LENGTH
        id = line[start: id_end]

        # Read value
        value_length = int(line[id_end: id_end + LENGTH_OF_VALUE_LENGTH], 16)
        value_start = start + ID_LENGTH + LENGTH_OF_VALUE_LENGTH
        value = line[value_start: value_start + value_length]
        results[id] = value

        start += ID_LENGTH + LENGTH_OF_VALUE_LENGTH + value_length

    return results

if __name__ == '__main__':
    encoded_contact_info_file = open("ex_v8.txt", "r")

    decoded_results = {
        FIRST_NAME_KEY: dict(),
        LAST_NAME_KEY: dict(),
        PHONE_KEY: dict(),
        TIME_KEY: dict(),
        MISC_KEY: dict()
    }
    id_set = set()

    while current_line := encoded_contact_info_file.readline().rstrip():
        line_key = int(current_line[:4], 16)
        current_line = current_line[4:]
        decoded_line = read_encoded_line(current_line)

        decoded_results[line_key].update(decoded_line)
        for id in decoded_line:
            id_set.add(id)

    encoded_contact_info_file.close()

    decoded_contact_info_file = open("decoded_info.csv", "w")
    decoded_contact_info_file.write("id,first_name,last_name,phone,time,misc\n")
    for id in id_set:
        line = f"{id}"
        for key in KEYS:
            value = decoded_results[key].get(id)
            line += f",{value if value is not None else 'None'}"
        decoded_contact_info_file.write(line + '\n')
    decoded_contact_info_file.close()
