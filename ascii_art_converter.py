import platform
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Character sets for SD and HD ASCII art
ASCII_CHARS_SD = "@%#*+=-:. "
ASCII_CHARS_HD = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def resize_image(image, new_width):
    """Resize image to a new width while maintaining aspect ratio."""
    width, height = image.size
    aspect_ratio = height / width
    # Adjust the height to account for ASCII character's aspect ratio
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))

def grayscale_image(image):
    """Convert image to grayscale."""
    return image.convert("L")

def map_pixels_to_ascii_chars(image, ascii_chars):
    """Map each pixel to an ASCII character based on its intensity."""
    pixels = np.array(image)
    ascii_str = ''
    # Normalize pixel values to select characters from ASCII_CHARS
    range_width = 256 / len(ascii_chars)
    for pixel_value in pixels.flatten():
        ascii_str += ascii_chars[int(pixel_value // range_width)]
    return ascii_str

def convert_image_to_ascii(image, new_width, ascii_chars):
    """Convert an image to ASCII art."""
    # Resize the image
    image = resize_image(image, new_width)

    # Convert the image to grayscale
    image = grayscale_image(image)

    # Convert the image to ASCII characters
    ascii_str = map_pixels_to_ascii_chars(image, ascii_chars)
    img_width = image.width

    # Split the ASCII string into lines of appropriate width
    ascii_str_len = len(ascii_str)
    ascii_img = [ascii_str[index: index + img_width] for index in range(0, ascii_str_len, img_width)]

    return "\n".join(ascii_img)

def get_font_path():
    """Get the appropriate font path based on the operating system."""
    os_name = platform.system()
    if os_name == 'Windows':
        return "C:/Windows/Fonts/consola.ttf"  # Windows: Consolas
    elif os_name == 'Darwin':  # Darwin is the system name for macOS
        return "/System/Library/Fonts/Menlo.ttc"  # macOS: Menlo
    else:
        raise OSError("Unsupported operating system. Please use macOS or Windows.")

def save_ascii_as_image(ascii_art, output_image_path, font_size):
    """Save ASCII art as a JPEG image."""
    font_path = get_font_path()

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font not found: {font_path}. Using default monospaced font.")
        font = ImageFont.load_default()

    lines = ascii_art.splitlines()
    
    # Determine character width and height using getbbox
    char_width, char_height = font.getbbox("A")[2], font.getbbox("A")[3]
    
    width = max(len(line) for line in lines) * char_width
    height = len(lines) * char_height

    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    y_offset = 0
    for line in lines:
        draw.text((0, y_offset), line, font=font, fill='black')
        y_offset += char_height

    image.save(output_image_path, 'JPEG')

def main(image_path, output_jpeg_path, output_width=100, hd=False):
    # Determine parameters based on HD or SD
    if hd:
        ascii_chars = ASCII_CHARS_HD
        font_size = 6
        output_width = max(output_width, 200)  # Ensure minimum width for HD
    else:
        ascii_chars = ASCII_CHARS_SD
        font_size = 10
        output_width = min(output_width, 100)  # Cap width for SD

    # Open the input image
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}.")
        print(e)
        return

    # Convert image to ASCII
    ascii_art = convert_image_to_ascii(image, new_width=output_width, ascii_chars=ascii_chars)

    # Save the ASCII art as a JPEG image using a monospaced font
    save_ascii_as_image(ascii_art, output_jpeg_path, font_size=font_size)

# Example usage
if __name__ == "__main__":
    # Replace 'input_image.jpeg' with your input image file path
    # The output JPEG image will be saved as 'ascii_output.jpeg'
    # Set hd=True for HD output, False for SD output
    main('pic.png', 'ascii_output.jpeg', output_width=100, hd=False)