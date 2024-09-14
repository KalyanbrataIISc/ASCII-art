from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QFileDialog, QRadioButton, QButtonGroup, QFrame, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PIL import Image
import os
import sys

from ascii_art_converter import main as ascii_art_main

class ASCIIArtConverterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.input_file = None
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # File selection section
        file_layout = QHBoxLayout()
        self.file_button = QPushButton('Select Image File')
        self.file_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_button)

        self.file_label = QLabel('No file selected')
        file_layout.addWidget(self.file_label)

        main_layout.addLayout(file_layout)

        # Output width section
        output_width_layout = QHBoxLayout()
        output_width_label = QLabel('Output Width:')
        self.output_width_input = QLineEdit('100')
        output_width_layout.addWidget(output_width_label)
        output_width_layout.addWidget(self.output_width_input)

        main_layout.addLayout(output_width_layout)

        # HD/SD mode section
        mode_layout = QHBoxLayout()
        mode_label = QLabel('Mode:')
        mode_layout.addWidget(mode_label)

        self.hd_radio = QRadioButton('HD')
        self.sd_radio = QRadioButton('SD')
        self.sd_radio.setChecked(True)

        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.hd_radio)
        self.mode_group.addButton(self.sd_radio)

        mode_layout.addWidget(self.hd_radio)
        mode_layout.addWidget(self.sd_radio)

        main_layout.addLayout(mode_layout)

        # Convert button
        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.convert_image)
        main_layout.addWidget(self.convert_button)

        # Preview section
        preview_layout = QHBoxLayout()

        # Original image preview
        self.original_label = QLabel('Original Image:')
        self.original_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.original_label.setFixedSize(200, 150)
        preview_layout.addWidget(self.original_label)

        # ASCII art preview
        self.ascii_label = QLabel('ASCII Art Preview:')
        self.ascii_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.ascii_label.setFixedSize(400, 300)
        preview_layout.addWidget(self.ascii_label)

        main_layout.addLayout(preview_layout)

        # Save and Reset buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton('Save')
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_image)
        button_layout.addWidget(self.save_button)

        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset)
        button_layout.addWidget(self.reset_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('ASCII Art Converter')

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", 
                                                   "Images (*.png *.jpg *.jpeg);;All Files (*)", options=options)
        if file_path:
            self.input_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.display_original(file_path)

    def display_original(self, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(200, 150)
        self.original_label.setPixmap(pixmap)

    def convert_image(self):
        if not self.input_file:
            self.show_error("Please select an image file first.")
            return

        output_width = self.output_width_input.text()
        try:
            output_width = int(output_width)
        except ValueError:
            self.show_error("Output width must be an integer.")
            return

        hd_mode = self.hd_radio.isChecked()

        # Here, you should call your ASCII conversion logic and save the result to 'temp_preview.jpeg'
        ascii_art_main(self.input_file, 'temp_preview.jpeg', output_width=output_width, hd=hd_mode)

        # For demonstration purposes, we'll just use the original image:
        self.display_ascii_preview('temp_preview.jpeg')
        self.save_button.setEnabled(True)

    def display_ascii_preview(self, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(400, 300)
        self.ascii_label.setPixmap(pixmap)

    def save_image(self):
        if not self.input_file:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save ASCII Art", "", "JPEG Files (*.jpeg);;All Files (*)")
        if save_path:
            # Save the ASCII art (temp_preview.jpeg) to the selected path
            os.rename('temp_preview.jpeg', save_path)

    def reset(self):
        self.input_file = None
        self.file_label.setText('No file selected')
        self.original_label.clear()
        self.ascii_label.clear()
        self.save_button.setEnabled(False)
        if os.path.exists('temp_preview.jpeg'):
            os.remove('temp_preview.jpeg')

    def show_error(self, message):
        messagebox = QMessageBox()
        messagebox.setIcon(QMessageBox.Critical)
        messagebox.setText(message)
        messagebox.exec_()

def start_gui():
    app = QApplication(sys.argv)
    window = ASCIIArtConverterGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_gui()