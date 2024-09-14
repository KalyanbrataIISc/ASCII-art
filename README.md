### README.md
```markdown
# ASCII Art Converter

## Overview
The ASCII Art Converter is a graphical application built with PyQt5 that converts images into ASCII art. The application allows users to select an image, adjust the output width, choose between HD and SD modes, and preview the generated ASCII art before saving it. It features an easy-to-use graphical interface and an icon for a polished look.

## Features
- Convert images (JPEG, PNG, etc.) into ASCII art.
- Adjustable output width for fine control over the ASCII art resolution.
- HD and SD modes for different ASCII art styles.
- Preview the original image and the resulting ASCII art side by side.
- Save the ASCII art as a high-quality PNG image.

## Prerequisites
- Python 3.6 or later
- pip (Python package installer)

## Installation

### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone [https://github.com/KalyanbrataIISc/ASCII-art.git]
cd ascii-art-converter
```

### Step 2: Install Dependencies
Install the required Python packages:
```bash
pip install PyQt5 Pillow numpy
```

### Step 3: Run the Application
Run the `main.py` file from inside the cloned directory to start the ASCII Art Converter:
```bash
python main.py
```

## Usage
1. **Launch the Application**: Run `main.py` to open the ASCII Art Converter.
2. **Select an Image**: Click "Select Image File" to choose an image from your file system.
3. **Adjust Settings**:
   - Set the "Output Width" to control the ASCII art resolution.
   - Choose "HD" or "SD" mode for different ASCII art styles.
4. **Convert**: Click the "Convert" button to generate and preview the ASCII art.
5. **Save**: If satisfied, click the "Save" button to save the ASCII art as a PNG image.
6. **Reset**: Click "Reset" to clear the selection and previews.

## Project Structure
```
ascii-art-converter/
│
├── assets/                 # Directory for assets (e.g., icons)
│   └── icon.png            # Application icon
│
├── ascii_app.py            # Main PyQt5 application code
├── ascii_art_converter.py  # ASCII art conversion logic
├── main.py                 # Entry point to launch the application
└── README.md               # Project documentation
```

## Requirements
- **PyQt5**: Provides the graphical user interface.
- **Pillow**: Used for image processing (PIL fork).
- **numpy**: For efficient pixel mapping and image manipulation.

## requirements.txt
```
PyQt5
Pillow
numpy
```

## Icon
The application uses a custom icon for a polished look. Place your icon in the `assets` directory and ensure the path is correctly referenced in `ascii_app.py`.

## Notes
- The `ascii_art_converter.py` script provides the core functionality to convert images into ASCII art.
- The `ascii_app.py` script manages the graphical interface and user interaction.
- The application saves the ASCII art in PNG format for high-quality output.

## Troubleshooting
- If the application icon does not change on macOS, ensure the correct icon path is specified, and clear the dock cache if necessary:
  ```bash
  killall Dock
  ```
- If you encounter issues with font paths, make sure the correct paths are provided in `ascii_art_converter.py` for your operating system.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Author
- **Kalyanbrata Chandra** 
```

### Summary:
- **Project Overview**: A brief description of the ASCII Art Converter and its features.
- **Installation and Setup**: Step-by-step instructions for setting up the project, including installing dependencies.
- **Usage**: A guide on how to use the application.
- **Project Structure**: Overview of the project files and directories.
- **Requirements**: List of required Python packages.
- **Troubleshooting**: Tips for addressing common issues.
- **License and Author**: Basic licensing and author information.

### Usage:
- Save this content as `README.md` in the root directory of your project.
- Ensure that all paths and filenames in the README match your actual project structure.
