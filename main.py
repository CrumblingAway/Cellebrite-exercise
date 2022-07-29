from contact import *

ID_LENGTH = 4
LENGTH_OF_VALUE_LENGTH = 5

LINE_KEY_LENGTH = 4
FIRST_NAME_KEY = 0x86B7
LAST_NAME_KEY = 0x9E60
PHONE_KEY = 0x5159
TIME_KEY = 0xD812
IMAGE_KEY = 0x6704
KEYS = [FIRST_NAME_KEY, LAST_NAME_KEY, PHONE_KEY, TIME_KEY, IMAGE_KEY]

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


def decode_lines(filepath):
    """
    Decodes the given file per line and returns a set of contact IDs as well dictionaries of all the values associated
    with said IDs.
    :param filepath:
    :return:
    """
    decoded_results = {
        FIRST_NAME_KEY: dict(),
        LAST_NAME_KEY: dict(),
        PHONE_KEY: dict(),
        TIME_KEY: dict(),
        IMAGE_KEY: dict()
    }
    id_set = set()

    encoded_contact_info_file = open(filepath, "r")
    while current_line := encoded_contact_info_file.readline().rstrip():
        line_key = int(current_line[:LINE_KEY_LENGTH], 16)
        current_line = current_line[LINE_KEY_LENGTH:]

        decoded_line = read_encoded_line(current_line)
        decoded_results[line_key].update(decoded_line)
        for id in decoded_line:
            id_set.add(id)
    encoded_contact_info_file.close()

    return id_set, decoded_results


def save_contacts_csv(filename, contacts):
    """
    Writes the contacts into filepath.
    :param id_set: IDs of contacts.
    :param id_values: values associated with the IDs.
    :param filename: name of file without extension.
    :return:
    """
    decoded_contact_info_file = open(f"{filename}.csv", "w")
    decoded_contact_info_file.write("id,first_name,last_name,phone,time,has_image\n")
    # for id in id_set:
    #     line = f"{id}"
    #     for key in KEYS:
    #         value = id_values[key].get(id)
    #         line += f",{value if value is not None else 'None'}"
    #     decoded_contact_info_file.write(line + '\n')
    for contact in contacts:
        line = f"{contact.id},{contact.first_name},{contact.last_name},{contact.phone},{contact.time}," \
               f"{int(contact.encoded_image is not None)}\n"
        decoded_contact_info_file.write(line)
    decoded_contact_info_file.close()

def extract_contacts(id_set, id_values):
    contacts = []
    for id in id_set:
        contacts.append(Contact(id,
                                id_values[FIRST_NAME_KEY].get(id),
                                id_values[LAST_NAME_KEY].get(id),
                                id_values[PHONE_KEY].get(id),
                                id_values[TIME_KEY].get(id),
                                id_values[IMAGE_KEY].get(id)))
    return contacts

if __name__ == '__main__':
    id_set, id_values = decode_lines("ex_v8.txt")
    contacts = extract_contacts(id_set, id_values)
    save_contacts_csv("decoded_info", contacts)

    for contact in contacts:
        contact.show_image()
