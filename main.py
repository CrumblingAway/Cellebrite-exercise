ID_LENGTH = 4
NUM_OF_DIGITS_LENGTH = 5

FIRST_NAME_KEY = 0x86B7
SECOND_NAME_KEY = 0x9E60
PHONE_KEY = 0x5159
TIME_KEY = 0xD812


def read_encoded_line(line):
    results = dict()
    start_idx = 0

    while start_idx < len(line):
        id = line[start_idx: start_idx + ID_LENGTH]
        name_length = int(line[start_idx + ID_LENGTH: start_idx + ID_LENGTH + NUM_OF_DIGITS_LENGTH], 16) # TODO: CHECK IF HEX
        name = line[start_idx + ID_LENGTH + NUM_OF_DIGITS_LENGTH: start_idx + ID_LENGTH + NUM_OF_DIGITS_LENGTH + name_length]
        results[id] = name

        start_idx += ID_LENGTH + NUM_OF_DIGITS_LENGTH + name_length

    return results

if __name__ == '__main__':
    encoded_contact_info_file = open("ex_v8.txt", "r")

    first_name_results = dict()
    second_name_results = dict()
    phone_results = dict()
    time_results = dict()

    while current_line := encoded_contact_info_file.readline().rstrip():
        line_key = int(current_line[:4], 16)
        current_line = current_line[4:]

        if line_key == FIRST_NAME_KEY:
            first_name_results = read_encoded_line(current_line)
        elif line_key == SECOND_NAME_KEY:
            second_name_results = read_encoded_line(current_line)
        elif line_key == PHONE_KEY:
            phone_results = read_encoded_line(current_line)
        elif line_key == TIME_KEY:
            time_results = read_encoded_line(current_line)

    encoded_contact_info_file.close()

    for id in first_name_results:
        print(f"{id}: {first_name_results[id]} {second_name_results[id]} {phone_results[id]} {time_results[id]}")
