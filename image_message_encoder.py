
from PIL import Image
import datetime
import os
import random
import string
import psutil

def generate_key():
    # Generate a unique key based on current datetime, system uptime, and process ID
    current_datetime1 = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    length = 32 - len(current_datetime1)
    substring = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[8:20]
    final_datetime = current_datetime1 + substring
    
    uptime = psutil.boot_time()
    remaining_length = 32 - len(str(int(uptime)))
    random_characters = ''.join(random.choice(str(int(uptime))) for _ in range(remaining_length))
    final_uptime = str(int(uptime)) + random_characters

    pid = str(os.getpid())
    remaining_length = 32 - len(pid)
    random_characters = ''.join(random.choice(pid) for _ in range(remaining_length))
    final_pid = str(pid + random_characters)

    digits = "0123456789"
    random_digits = ''.join(random.choice(digits) for _ in range(32))

    final_key = final_datetime + final_uptime + final_pid + random_digits
    
    # Generate a random selection of digits from the key
    random_digits = ''.join(random.choice(final_key) for _ in range(32))
    random_digits = int(random_digits)
    
    # Convert the selected bits into a binary string of length 128
    binary_key = format(random_digits, '0128b')
    
    return binary_key

def save_key_to_file(key, file_path):
    # Save the key to a text file
    with open(file_path, 'w') as file:
        file.write(key)

def hide_message(image_path, message, output_image_path, key_file_path):
    # Hide the message within the image
    img = Image.open(image_path)
    key = generate_key()
    save_key_to_file(key, key_file_path)
    binary_message = ''.join(format(ord(char), '08b') for char in message)  # Convert message to binary
    message_length = len(binary_message)
    
    # Encode the length of the message into the first 32 pixels of the image
    length_binary = format(message_length, '032b')
    for i in range(32):
        pixel = list(img.getpixel((i, 0)))
        pixel[0] = pixel[0] & ~1 | int(length_binary[i])
        img.putpixel((i, 0), tuple(pixel))
    
    data_index = 0
    # Embed the key into the specified range of pixels
    for i in range(33, 161):  # Pixels (33, 0) to (159, 0)
        pixel = list(img.getpixel((i, 0)))
        pixel[0] = pixel[0] & ~1 | int(key[data_index])
        data_index += 1
        img.putpixel((i, 0), tuple(pixel))
    
    data_index = 0
    # Traverse through each pixel in the image (starting after the first 32 pixels)
    for y in range(img.height):
        for x in range(161, img.width):
            pixel = list(img.getpixel((x, y)))

            # Modify the least significant bit of each color component
            for i in range(3):  # RGB channels
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1

            img.putpixel((x, y), tuple(pixel))

            if data_index >= len(binary_message):
                break

    img.save(output_image_path)
    print("Message Encoded Successfully!!")

# Example usage:
key_file_path = "key.txt"
hide_message("image_before_encoding.jpg", "Keep coding and carry on!", "image_after_encoding.png", key_file_path)