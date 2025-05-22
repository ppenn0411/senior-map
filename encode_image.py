import base64
import sys

image_path = "background.png"

try:
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        print(encoded_string)
except FileNotFoundError:
    print(f"Error: File not found at {image_path}", file=sys.stderr)
except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr) 