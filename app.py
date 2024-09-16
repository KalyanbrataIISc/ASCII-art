from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QFileDialog, QRadioButton, QButtonGroup, QFrame, QMessageBox, QSlider, QScrollArea
)
from PyQt5.QtGui import QPixmap, QIcon, QColor, QImage, QPainter
from PyQt5.QtCore import Qt, QRect  # Import Qt for alignment and rectangle handling
import os
import sys

from ascii_art_converter import main as ascii_art_main

class ZoomableLabel(QLabel):
    def __init__(self, parent=None):
        super(ZoomableLabel, self).__init__(parent)
        self.setScaledContents(True)  # Allow scaling of the pixmap
        self._pixmap = None
        self._zoom_level = 1.0

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self.update_pixmap()

    def update_pixmap(self):
        if self._pixmap:
            scaled_pixmap = self._pixmap.scaled(self._zoom_level * self._pixmap.size(), Qt.KeepAspectRatio)
            super(ZoomableLabel, self).setPixmap(scaled_pixmap)

    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming."""
        if event.angleDelta().y() > 0:
            self._zoom_level *= 1.1  # Zoom in
        else:
            self._zoom_level *= 0.9  # Zoom out

        self.update_pixmap()
        event.accept()

class ASCIIArtConverterGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.input_file = None
        self.custom_characters = None
        # Define the path for the temporary file in the same directory as this script
        self.temp_preview_file = os.path.join(os.path.dirname(__file__), 'temp_preview.png')
        # Set the application icon
        self.setWindowIcon(QIcon('assets/icon.png'))  # Replace 'icon.png' with the path to your icon file
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

        # HD/SD/Custom mode section
        mode_layout = QVBoxLayout()
        mode_label = QLabel('Mode:')
        mode_layout.addWidget(mode_label)

        self.hd_radio = QRadioButton('All characters (Gradient)')
        self.sd_radio = QRadioButton('Few characters (Contrast)')
        self.custom_radio = QRadioButton('Custom characters')
        self.sd_radio.setChecked(True)

        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.hd_radio)
        self.mode_group.addButton(self.sd_radio)
        self.mode_group.addButton(self.custom_radio)

        mode_radio_layout = QHBoxLayout()
        mode_radio_layout.addWidget(self.hd_radio)
        mode_radio_layout.addWidget(self.sd_radio)
        mode_radio_layout.addWidget(self.custom_radio)
        mode_layout.addLayout(mode_radio_layout)

        # Custom characters input section
        self.custom_input_layout = QHBoxLayout()
        self.custom_input_box = QLineEdit()
        self.custom_input_box.setPlaceholderText('Enter custom characters')
        self.custom_input_done_button = QPushButton('Done')
        self.custom_input_done_button.clicked.connect(self.set_custom_characters)
        self.custom_input_layout.addWidget(self.custom_input_box)
        self.custom_input_layout.addWidget(self.custom_input_done_button)
        self.custom_input_layout.addStretch()

        # Confirmation label for custom characters
        self.confirmation_label = QLabel('')
        self.confirmation_label.setStyleSheet('color: green')
        mode_layout.addLayout(self.custom_input_layout)
        mode_layout.addWidget(self.confirmation_label)
        
        # Initially hide custom input fields
        self.custom_input_box.setVisible(False)
        self.custom_input_done_button.setVisible(False)
        self.confirmation_label.setVisible(False)

        # Connect custom radio button toggle to show/hide input
        self.custom_radio.toggled.connect(self.toggle_custom_input)

        main_layout.addLayout(mode_layout)

        # Brightness section
        brightness_layout = QHBoxLayout()
        brightness_label = QLabel('Brightness:')
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(0, 10)
        self.brightness_slider.setValue(0)  # Default brightness value
        self.brightness_slider.valueChanged.connect(self.update_brightness_label)  # Connect to update function
        
        # Brightness value label
        self.brightness_value_label = QLabel('0')  # Initial brightness value
        brightness_layout.addWidget(brightness_label)
        brightness_layout.addWidget(self.brightness_slider)
        brightness_layout.addWidget(self.brightness_value_label)  # Add the value label

        main_layout.addLayout(brightness_layout)

        # Convert button
        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.convert_image)
        main_layout.addWidget(self.convert_button)

        # Preview section
        preview_layout = QHBoxLayout()

        # Original image preview (Zoomable and scrollable)
        original_scroll_area = QScrollArea()
        self.original_label = ZoomableLabel()
        self.original_label.setFixedSize(400, 300)
        original_scroll_area.setWidgetResizable(True)
        original_scroll_area.setWidget(self.original_label)
        preview_layout.addWidget(original_scroll_area)

        # ASCII art preview (Zoomable and scrollable)
        ascii_scroll_area = QScrollArea()
        self.ascii_label = ZoomableLabel()
        self.ascii_label.setFixedSize(600, 450)
        ascii_scroll_area.setWidgetResizable(True)
        ascii_scroll_area.setWidget(self.ascii_label)
        preview_layout.addWidget(ascii_scroll_area)

        main_layout.addLayout(preview_layout)

        # Save and Reset buttons
        button_layout = QHBoxLayout()
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset)
        button_layout.addWidget(self.reset_button)

        self.save_button = QPushButton('Save')
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_image)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('ASCII Art Converter')

    def toggle_custom_input(self):
        """Show/hide custom input fields based on custom radio button toggle."""
        if self.custom_radio.isChecked():
            self.custom_input_box.setVisible(True)
            self.custom_input_done_button.setVisible(True)
        else:
            self.custom_input_box.setVisible(False)
            self.custom_input_done_button.setVisible(False)
            self.confirmation_label.setVisible(False)

    def set_custom_characters(self):
        """Set the custom characters entered by the user."""
        custom_string = self.custom_input_box.text()
        if custom_string:
            self.custom_characters = custom_string
            self.confirmation_label.setText(f'Custom characters: {custom_string}')
            self.confirmation_label.setVisible(True)
        else:
            self.confirmation_label.setText('')

    def update_brightness_label(self):
        """Update the brightness label with the current slider value."""
        brightness_value = self.brightness_slider.value()
        self.brightness_value_label.setText(str(brightness_value))

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", 
                                                   "Images (*.png *.jpg *.jpeg);;All Files (*)", options=options)
        if file_path:
            self.input_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.display_original(file_path)
            self.clear_ascii_preview()  # Clear the previous ASCII preview if it exists

    def display_original(self, image_path):
        pixmap = QPixmap(image_path)
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

        # Determine mode
        hd_mode = self.hd_radio.isChecked()
        custom_mode = self.custom_radio.isChecked()

        # Get brightness level from slider
        brightness = self.brightness_slider.value()

        try:
            # Call the ASCII conversion logic and save the result to the temporary file
            if custom_mode and self.custom_characters:
                ascii_art_main(self.input_file, self.temp_preview_file, output_width=output_width, hd=False, custom=self.custom_characters, brightness=brightness)
            else:
                ascii_art_main(self.input_file, self.temp_preview_file, output_width=output_width, hd=hd_mode, brightness=brightness)

            self.display_ascii_preview(self.temp_preview_file)
            self.save_button.setEnabled(True)
        except Exception as e:
            self.show_error(f"Error during conversion: {e}")

    def display_ascii_preview(self, image_path):
        if not os.path.exists(image_path):
            self.show_error("The ASCII art preview could not be found.")
            return
        pixmap = QPixmap(image_path)
        self.ascii_label.setPixmap(pixmap)

    def save_image(self):
        if not self.input_file:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save ASCII Art", "", "JPEG Files (*.jpeg);;PNG Files (*.png);;All Files (*)")
        if save_path:
            try:
                # Save the ASCII art (temp_preview.png) to the selected path
                os.rename(self.temp_preview_file, save_path)
                self.show_info(f"ASCII art saved to: {save_path}")
            except Exception as e:
                self.show_error(f"Error saving file: {e}")

    def reset(self):
        self.input_file = None
        self.file_label.setText('No file selected')
        self.original_label.clear()
        self.ascii_label.clear()
        self.save_button.setEnabled(False)
        self.custom_characters = None
        self.confirmation_label.clear()
        if os.path.exists(self.temp_preview_file):
            try:
                os.remove(self.temp_preview_file)
            except Exception as e:
                self.show_error(f"Error deleting temporary file: {e}")

    def show_error(self, message):
        messagebox = QMessageBox()
        messagebox.setIcon(QMessageBox.Critical)
        messagebox.setText(message)
        messagebox.exec_()

    def show_info(self, message):
        messagebox = QMessageBox()
        messagebox.setIcon(QMessageBox.Information)
        messagebox.setText(message)
        messagebox.exec_()

    def clear_ascii_preview(self):
        self.ascii_label.clear()
        self.save_button.setEnabled(False)

def start_gui():
    app = QApplication(sys.argv)
    # Set the application icon globally
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')  # Ensure this path is correct
    app.setWindowIcon(QIcon(icon_path))  # Set the global application icon

    window = ASCIIArtConverterGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_gui()