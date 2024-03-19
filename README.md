# Image_Steganography-Using-Python

This repository contains Python scripts for hiding messages within images and extracting hidden messages from encoded images. The scripts utilize the Python Imaging Library (PIL) for image manipulation.

## Requirements
1. Python 3.x
2. PIL (Python Imaging Library)
3. psutil (Python library for system monitoring)

## Usage

### 1. Encoding (Hiding Message)
1. Ensure you have Python 3.x installed.
2. Install required libraries using pip install Pillow psutil.
3. Prepare the image file (image_before_encoding.jpg) where you want to hide the message.
4. Run the encode_message.py script, providing the image file path, the message you want to hide, the output image path, and the path to store the generated key.
5. Example: python encode_message.py image_before_encoding.jpg "Keep coding and carry on!" image_after_encoding.png key.txt

### 2. Decoding (Extracting Message)
1. Ensure you have Python 3.x installed.
2. Install required libraries using pip install Pillow.
3. Prepare the encoded image file (image_after_encoding.png) from which you want to extract the hidden message.
4. Provide the path to the encoded image and the path to the key file generated during encoding.
5. Run the decode_message.py script.
6. Example: python decode_message.py image_after_encoding.png key.txt
7. The decoded message will be printed to the console.

### 3. Key Generation
1. The key used for encoding is generated based on the following components:
2. Datetime Component: A unique datetime string (current_datetime) is generated in the format YYYYMMDDHHMMSSffffff. This ensures a level of uniqueness.
3. System Uptime Component: The system uptime is retrieved using the psutil library, and random characters are appended to ensure uniqueness (final_uptime).
4. Process ID Component: The process ID (pid) is retrieved and random characters are appended to ensure uniqueness (final_pid).
5. Random Digits Component: Random digits are generated to fill up the remaining length of the key.
6. These components are concatenated to form the final key, which is used for encoding. Additionally, a binary representation of the key is generated and saved to a text file for later use during decoding.

## Scripts
encode_message.py: This script hides a message within an image using LSB (Least Significant Bit) manipulation.
decode_message.py: This script extracts a hidden message from an encoded image using the provided key.

## Important Notes
Ensure to keep the generated key file (key.txt) secure and accessible for decoding messages.
Avoid lossy compression formats (e.g., JPEG) for encoded images to prevent loss of hidden data.
## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.
