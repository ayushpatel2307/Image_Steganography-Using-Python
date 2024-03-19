
from PIL import Image  # Importing necessary library

def read_key_from_file(file_path):
    # Function to read the key from a text file
    with open(file_path, 'r') as file:
        return file.read().strip()  # Remove leading/trailing whitespace

def extract_message(image_path, key_file_path):
    # Function to extract a message from an encoded image using a key
    # Read the key from the text file
    provided_key = read_key_from_file(key_file_path)
    
    # Open the encoded image
    img = Image.open(image_path)
    
    # Initialize variables
    binary_length = ''  # To store binary representation of message length
    new_key = 0  # Placeholder for new key (not used in current implementation)

    # Extract the length of the message from the first 32 pixels of the image
    for i in range(32):
        pixel = img.getpixel((i, 0))  # Get pixel at position (i, 0)
        binary_length += str(pixel[0] & 1)  # Extract LSB of red component

    message_length = int(binary_length, 2)  # Convert binary length to integer

    extracted_key = ''
    # Extract the key from pixels (33, 0) to (159, 0)
    for i in range(33, 161):
        pixel = img.getpixel((i, 0))
        extracted_key += str(pixel[0] & 1)  # Extract LSB of red component
    
    # Check if extracted key matches the provided key
    if extracted_key == provided_key:
        # Extract the message from the remaining pixels
        binary_message = ''
        data_index = 0  # Counter to keep track of message bits
        
        # Iterate over each pixel in the image
        for y in range(img.height):
            for x in range(161, img.width):
                pixel = img.getpixel((x, y))  # Get pixel at position (x, y)
                
                # Extract the least significant bit of each color component (RGB)
                for i in range(3):  # RGB channels
                    binary_message += str(pixel[i] & 1)  # Extract LSB of color
                    data_index += 1  # Increment data index
                    
                    if data_index >= message_length:
                        break  # Exit inner loop if message length is reached
                if data_index >= message_length:
                    break  # Exit outer loop if message length is reached
            
            if data_index >= message_length:
                break  # Exit outer loop if message length is reached
        
        # Convert binary message to ASCII characters
        message = ''
        for i in range(0, len(binary_message), 8):  # Iterate over every 8 bits
            byte = binary_message[i:i+8]  # Extract a byte (8 bits)
            message += chr(int(byte, 2))  # Convert binary to ASCII character

        return message  # Return extracted message
    else:
        return "wrong key"  # Return error message if keys don't match

# Example usage:
key_file_path = "key.txt"
extracted_message = extract_message("image_after_encoding.png", key_file_path)
print("Extracted message:", extracted_message)  # Print extracted message