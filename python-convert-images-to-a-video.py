import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from datetime import datetime
import subprocess
import os
import shutil
from PIL import Image

class ImageToVideoConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Video Converter")
        self.input_images_to_video_folder = ""
        self.output_video_folder = ""
        self.output_filename = ""
        self.expected_video_filename = ""
        self.input_image_folder = ""
        self.output_jpg_folder = ""
        self.fps = tk.StringVar()
        self.fps.set("30")
        self.video_process = None
        self.jpg_process = None
        self.create_widgets()

    def create_widgets(self):
        # Input images to video folder
        input_video_label = tk.Label(self.root, text="Input Images To Video Folder:")
        input_video_label.pack()
        input_images_to_video_folder_label = tk.Label(self.root, text="")
        input_images_to_video_folder_label.pack()
        input_video_button = tk.Button(self.root, text="Browse", command=self.browse_input_images_to_video_folder)
        input_video_button.pack()

        # Output video folder
        output_video_label = tk.Label(self.root, text="Output Video Folder:")
        output_video_label.pack()
        output_video_folder_label = tk.Label(self.root, text="")
        output_video_folder_label.pack()
        output_video_button = tk.Button(self.root, text="Browse", command=self.browse_output_video_folder)
        output_video_button.pack()

        # Input Image folder
        input_image_label = tk.Label(self.root, text="Input Image Folder:")
        input_image_label.pack()
        input_image_folder_label = tk.Label(self.root, text="")
        input_image_folder_label.pack()
        input_image_button = tk.Button(self.root, text="Browse", command=self.browse_input_image_folder)
        input_image_button.pack()

        # Output JPG folder
        output_jpg_label = tk.Label(self.root, text="Output JPG Folder:")
        output_jpg_label.pack()
        output_jpg_folder_label = tk.Label(self.root, text="")
        output_jpg_folder_label.pack()
        output_jpg_button = tk.Button(self.root, text="Browse", command=self.browse_output_jpg_folder)
        output_jpg_button.pack()

        # FPS selection
        fps_label = tk.Label(self.root, text="FPS:")
        fps_label.pack()
        fps_entry = tk.Entry(self.root, textvariable=self.fps)
        fps_entry.pack()

        # Convert Video button
        convert_video_button = tk.Button(self.root, text="Convert to Video", command=self.convert_to_video)
        convert_video_button.pack()
        self.video_progress = Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.video_progress.pack()

        # Convert JPG button
        convert_jpg_button = tk.Button(self.root, text="Convert to JPG", command=self.convert_to_jpg)
        convert_jpg_button.pack()
        self.jpg_progress = Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.jpg_progress.pack()

        # Cancel button
        cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel_conversion, state=tk.DISABLED)
        cancel_button.pack()
        self.cancel_button = cancel_button

        # Preview button
        preview_button = tk.Button(self.root, text="Preview", command=self.preview_video, state=tk.DISABLED)
        preview_button.pack()
        self.preview_button = preview_button

    def browse_input_images_to_video_folder(self):
        self.input_images_to_video_folder = filedialog.askdirectory()
        if self.input_images_to_video_folder:
            print(f"Input Images To Video Folder: {self.input_images_to_video_folder}")
            input_images_to_video_folder_label = self.root.nametowidget(self.root.winfo_children()[2])
            input_images_to_video_folder_label.config(text=f"Input Images To Video Folder: {self.input_images_to_video_folder}")

    def browse_output_video_folder(self):
        self.output_video_folder = filedialog.askdirectory()
        if self.output_video_folder:
            print(f"Output Video Folder: {self.output_video_folder}")
            output_video_folder_label = self.root.nametowidget(self.root.winfo_children()[5])
            output_video_folder_label.config(text=f"Output Video Folder: {self.output_video_folder}")
            self.expected_video_filename = f"{self.output_video_folder}/{self.get_expected_video_filename()}"

    def browse_input_image_folder(self):
        self.input_image_folder = filedialog.askdirectory()
        if self.input_image_folder:
            print(f"Input Image Folder: {self.input_image_folder}")
            input_image_folder_label = self.root.nametowidget(self.root.winfo_children()[8])
            input_image_folder_label.config(text=f"Input Image Folder: {self.input_image_folder}")

    def browse_output_jpg_folder(self):
        self.output_jpg_folder = filedialog.askdirectory()
        if self.output_jpg_folder:
            print(f"Output JPG Folder: {self.output_jpg_folder}")
            output_jpg_folder_label = self.root.nametowidget(self.root.winfo_children()[11])
            output_jpg_folder_label.config(text=f"Output JPG Folder: {self.output_jpg_folder}")

    def convert_to_video(self):
        if not self.input_images_to_video_folder or not self.output_video_folder:
            messagebox.showerror("Error", "Please select input and output video folders.")
            return

        self.output_filename = self.get_expected_video_filename()
        self.expected_video_filename = f"{self.output_video_folder}/{self.output_filename}"

        self.cancel_button.config(state=tk.NORMAL)
        self.video_progress["value"] = 0
        self.video_progress["maximum"] = 100

        input_images = sorted(os.listdir(self.input_images_to_video_folder))
        jpg_images = [image for image in input_images if image.lower().endswith(('.jpg', '.jpeg'))]
        png_images = [image for image in input_images if image.lower().endswith('.png')]

        if len(jpg_images) > len(png_images):
            self.image_extension = 'jpg'
        else:
            self.image_extension = 'png'

        command = [
            "ffmpeg", "-framerate", self.fps.get(), "-i", f"{self.input_images_to_video_folder}/%04d.{self.image_extension}",
            "-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-crf", "25",
            "-minrate:v", "6M", "-b:v", "6M", "-maxrate:v", "6M", "-bufsize:v", "6M",
            "-coder", "1", "-pix_fmt", "yuv420p", "-g", "120", "-bf", "2", "-f", "mp4",
            "-movflags", "+faststart", self.expected_video_filename
        ]

        try:
            self.video_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output = self.video_process.stderr.readline()
                if not output:
                    break
                if "frame=" in output:
                    current_frame = int(output.split("frame=")[1].split("fps=")[0].strip())
                    self.video_progress["value"] = (current_frame / 100)  # Assuming 100 frames

            self.video_progress["value"] = 100  # Set to 100% when the conversion is done
            self.video_progress.update()
            self.video_process.communicate()
            self.cancel_button.config(state=tk.DISABLED)

            if self.get_expected_video_filename() == self.get_expected_video_filename():
                messagebox.showinfo("Success", "Conversion completed successfully.")
                self.preview_button.config(state=tk.NORMAL)
            else:
                messagebox.showerror("Error", "Conversion failed. Output filename does not match the expected filename. Please check the output folder.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during conversion: {e}")

    def convert_to_jpg(self):
        if not self.input_image_folder or not self.output_jpg_folder:
            messagebox.showerror("Error", "Please select input and output JPG folders.")
            return

        image_files = os.listdir(self.input_image_folder)
        image_files.sort()  # Sort the image files alphabetically

        self.cancel_button.config(state=tk.NORMAL)
        self.jpg_progress["value"] = 0
        self.jpg_progress["maximum"] = len(image_files)

        for i, image_file in enumerate(image_files):
            if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_image_path = os.path.join(self.input_image_folder, image_file)
                output_filename = f"{self.output_jpg_folder}/{i:04d}.jpg"
                self.convert_image_to_jpg(input_image_path, output_filename)
                self.jpg_progress["value"] = i + 1
                self.jpg_progress.update()

        self.jpg_progress["value"] = len(image_files)  # Set to 100% when the conversion is done
        self.cancel_button.config(state=tk.DISABLED)
        messagebox.showinfo("Success", "Image conversion completed successfully.")

    def convert_image_to_jpg(self, input_path, output_path):
        try:
            img = Image.open(input_path)
            img = img.convert("RGB")
            img.save(output_path, "JPEG", quality=99)
        except Exception as e:
            print(f"Error converting image: {e}")

    def cancel_conversion(self):
        if self.video_process:
            self.video_process.terminate()
        if self.jpg_process:
            self.jpg_process.terminate()
        self.cancel_button.config(state=tk.DISABLED)
        self.video_progress["value"] = 0
        self.jpg_progress["value"] = 0
        print("Conversion canceled.")

    def preview_video(self):
        if not self.output_video_folder:
            messagebox.showerror("Error", "Please select the output video folder.")
            return
        preview_process = subprocess.Popen(["ffplay", self.expected_video_filename, "-loop", "0"])
        preview_process.wait()

    def get_expected_video_filename(self):
        current_datetime = datetime.now()
        return f"{current_datetime.strftime('%d-%m-%Y-%H-%M-%S.mp4')}"

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToVideoConverter(root)

    # Apply a white theme to the GUI
    root.tk_setPalette(background='white', foreground='black')

    root.mainloop()
