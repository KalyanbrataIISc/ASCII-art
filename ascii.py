import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Import the ASCII art converter functions
from ascii_art_converter import main as ascii_art_main

class ASCIIArtConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Converter")
        self.input_file = None
        self.output_width = tk.IntVar(value=100)
        self.hd_mode = tk.BooleanVar(value=False)
        
        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # File selection button
        self.file_button = tk.Button(self.root, text="Select Image File", command=self.select_file)
        self.file_button.grid(row=0, column=0, padx=10, pady=10)

        # Label to display the selected file path
        self.file_path_label = tk.Label(self.root, text="No file selected", anchor='w')
        self.file_path_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Output width entry
        tk.Label(self.root, text="Output Width:").grid(row=1, column=0, padx=10, pady=5)
        self.width_entry = tk.Entry(self.root, textvariable=self.output_width)
        self.width_entry.grid(row=1, column=1, padx=10, pady=5)

        # HD/SD mode radio buttons
        self.mode_label = tk.Label(self.root, text="Mode:")
        self.mode_label.grid(row=2, column=0, padx=10, pady=5)
        self.hd_radio = tk.Radiobutton(self.root, text="HD", variable=self.hd_mode, value=True)
        self.sd_radio = tk.Radiobutton(self.root, text="SD", variable=self.hd_mode, value=False)
        self.hd_radio.grid(row=2, column=1, padx=5, sticky='w')
        self.sd_radio.grid(row=3, column=1, padx=5, sticky='w')  # Placed in the same column but different row

        # Convert button
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_image)
        self.convert_button.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

        # Canvas for original image preview
        self.original_preview_label = tk.Label(self.root, text="Original Image:")
        self.original_preview_label.grid(row=5, column=0, padx=10, pady=5, columnspan=1)
        self.original_canvas = tk.Canvas(self.root, width=200, height=150, bg="white")
        self.original_canvas.grid(row=6, column=0, padx=10, pady=5)

        # Canvas for ASCII art preview
        self.preview_label = tk.Label(self.root, text="ASCII Art Preview:")
        self.preview_label.grid(row=5, column=1, padx=10, pady=5, columnspan=2)
        self.ascii_canvas = tk.Canvas(self.root, width=400, height=300, bg="white")
        self.ascii_canvas.grid(row=6, column=1, padx=10, pady=5, columnspan=3)

        # Save button
        self.save_button = tk.Button(self.root, text="Save", command=self.save_image, state=tk.DISABLED)
        self.save_button.grid(row=7, column=1, padx=10, pady=10, columnspan=1)

        # Reset button
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.grid(row=7, column=0, padx=10, pady=10, columnspan=1)

    def select_file(self):
        try:
            # Use the file dialog associated with the existing root window
            file_path = filedialog.askopenfilename(
                filetypes=[("JPEG files", "*.jpeg"), ("JPG files", "*.jpg"), ("PNG files", "*.png"), ("All Files", "*.*")]
            )
            if file_path:
                self.input_file = file_path  # Store the file path
                self.file_path_label.config(text=self.input_file)  # Update the label to show the selected file
                self.display_original(file_path)  # Display the original image
            else:
                messagebox.showwarning("File Selection", "No file selected.")
        except Exception as e:
            messagebox.showerror("File Selection Error", str(e))

    def display_original(self, image_path):
        # Display the original image on the canvas
        try:
            original_image = Image.open(image_path)
            original_image.thumbnail((200, 150))  # Resize for preview
            self.original_image_preview = ImageTk.PhotoImage(original_image)
            self.original_canvas.create_image(100, 75, image=self.original_image_preview)
        except Exception as e:
            messagebox.showerror("Original Image Error", str(e))

    def convert_image(self):
        if not self.input_file:
            messagebox.showwarning("No File Selected", "Please select an image file first.")
            return
        
        # Convert the image to ASCII art
        output_width = self.output_width.get()
        hd_mode = self.hd_mode.get()
        try:
            # Use a temporary file path to hold the image in memory for preview
            self.output_image_path = "temp_preview.jpeg"
            ascii_art_main(self.input_file, self.output_image_path, output_width=output_width, hd=hd_mode)

            # Display the converted image
            self.display_ascii_preview(self.output_image_path)
            self.save_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def display_ascii_preview(self, image_path):
        # Open the image and display it in the ASCII canvas
        try:
            ascii_image = Image.open(image_path)
            ascii_image.thumbnail((400, 300))  # Resize for preview
            self.ascii_image_preview = ImageTk.PhotoImage(ascii_image)
            self.ascii_canvas.create_image(200, 150, image=self.ascii_image_preview)
        except Exception as e:
            messagebox.showerror("ASCII Preview Error", str(e))

    def save_image(self):
        # Save the ASCII image to the same directory as the input
        if not self.input_file:
            return
        
        try:
            save_path = os.path.join(os.path.dirname(self.input_file), "ascii_output.jpeg")
            os.rename(self.output_image_path, save_path)
            messagebox.showinfo("Saved", f"ASCII art saved to: {save_path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def reset(self):
        # Reset the application state
        self.input_file = None
        self.file_path_label.config(text="No file selected")
        self.original_canvas.delete("all")
        self.ascii_canvas.delete("all")
        self.save_button.config(state=tk.DISABLED)
        
        # Delete the temporary file (temp_preview.jpeg) if it exists
        if hasattr(self, 'output_image_path') and os.path.exists(self.output_image_path):
            try:
                os.remove(self.output_image_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete temporary file: {e}")
        
        # Clear the temporary file path
        self.output_image_path = None
        messagebox.showinfo("Reset", "Application reset complete.")

# Main function to start the GUI
def start_gui():
    root = tk.Tk()
    app = ASCIIArtConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()