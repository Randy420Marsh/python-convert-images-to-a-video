import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
from PIL import Image

class ImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")
        self.input_folder = None
        self.output_folder = None

        # Input Folder Selection
        tk.Label(root, text="Select Input Folder:").pack()
        self.input_folder_button = tk.Button(root, text="Choose Folder", command=self.choose_input_folder)
        self.input_folder_button.pack()

        # Output Folder Selection
        tk.Label(root, text="Select Output Folder:").pack()
        self.output_folder_button = tk.Button(root, text="Choose Folder", command=self.choose_output_folder)
        self.output_folder_button.pack()

        # Convert Button
        self.convert_button = tk.Button(root, text="Convert Images", command=self.convert_images)
        self.convert_button.pack()

        # Progress Bar
        self.progress = Progressbar(root, length=300, mode="determinate")
        self.progress.pack()
        self.progress["value"] = 0

    def choose_input_folder(self):
        self.input_folder = filedialog.askdirectory()
        if self.input_folder:
            self.input_folder_button["state"] = "disabled"
            messagebox.showinfo("Info", f"Input folder selected: {self.input_folder}")

    def choose_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.output_folder_button["state"] = "disabled"
            messagebox.showinfo("Info", f"Output folder selected: {self.output_folder}")

    def convert_images(self):
        if not self.input_folder or not self.output_folder:
            messagebox.showerror("Error", "Please select input and output folders.")
            return

        files = os.listdir(self.input_folder)
        total_files = len(files)
        if total_files == 0:
            messagebox.showerror("Error", "No images found in the input folder.")
            return

        for i, filename in enumerate(files):
            input_path = os.path.join(self.input_folder, filename)
            output_filename = f"{i:04d}.jpg"
            output_path = os.path.join(self.output_folder, output_filename)

            img = Image.open(input_path)
            img.save(output_path, "JPEG", quality=99)
            self.progress["value"] = (i + 1) / total_files * 100
            self.root.update()

        messagebox.showinfo("Info", "Image conversion completed.")
        self.progress["value"] = 0
        self.input_folder_button["state"] = "normal"
        self.output_folder_button["state"] = "normal"

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverter(root)
    root.mainloop()
