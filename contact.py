from os.path import isfile, isdir
from os import mkdir
from datetime import datetime
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

IMAGES_DIR = "images"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class Contact:
    """
    Class representing a contact on a phone.
    """

    def __init__(self, id, first_name, last_name, phone, unix_timestamp, image):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.unix_timestamp = unix_timestamp
        self.encoded_image = image

        self.time = datetime.fromtimestamp(int(self.unix_timestamp)).strftime(DATE_FORMAT)
        self.decoded_image = base64.b64decode(self.encoded_image) if self.encoded_image is not None else None

    def __repr__(self):
        return f"id: {self.id}\nfirst name: {self.first_name}\nlast name: {self.last_name}\nphone: {self.phone}\n" \
               f"time: {self.time}"

    def show_image(self):
        """
        Shows image associated with contact if one exists.
        :return:
        """
        if self.decoded_image is None:
            print(f"Contact with id {self.id} has no associated image.")
            return

        filepath = f"images/{self.id}.gif"
        if not isdir(IMAGES_DIR):
            mkdir(IMAGES_DIR)
        if not isfile(filepath):
            image_file = open(filepath, "wb")
            image_file.write(self.decoded_image)
            image_file.close()

        plt.imshow(mpimg.imread(filepath))
        plt.show()
