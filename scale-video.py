import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from datetime import datetime
import subprocess
import os

class VideoScaler:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Scaler")
        self.input_video_file = ""
        self.output_video_folder = ""
        self.output_filename = ""
        self.scale_resolution = tk.StringVar()
        self.scale_resolution.set("")  # Default value (no scaling)
        self.video_process = None
        self.create_widgets()

    def create_widgets(self):
        # Select Existing Video
        input_video_label = tk.Label(self.root, text="Select Video to Scale:")
        input_video_label.pack()
        input_video_button = tk.Button(self.root, text="Browse", command=self.browse_input_video_file)
        input_video_button.pack()

        # Output Video Folder
        output_video_label = tk.Label(self.root, text="Output Video Folder:")
        output_video_label.pack()
        output_video_folder_label = tk.Label(self.root, text="")
        output_video_folder_label.pack()
        output_video_button = tk.Button(self.root, text="Browse", command=self.browse_output_video_folder)
        output_video_button.pack()

        # Resolution Scaling Input
        scale_label = tk.Label(self.root, text="Scale Resolution (e.g., 1280x720):")
        scale_label.pack()
        scale_entry = tk.Entry(self.root, textvariable=self.scale_resolution)
        scale_entry.pack()

        # Convert Video button
        convert_video_button = tk.Button(self.root, text="Scale Video", command=self.scale_video)
        convert_video_button.pack()
        self.video_progress = Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.video_progress.pack()

        # Cancel button
        cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel_conversion, state=tk.DISABLED)
        cancel_button.pack()
        self.cancel_button = cancel_button

        # Preview button
        preview_button = tk.Button(self.root, text="Preview", command=self.preview_video, state=tk.DISABLED)
        preview_button.pack()
        self.preview_button = preview_button

    def browse_input_video_file(self):
        self.input_video_file = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if self.input_video_file:
            print(f"Input Video Selected: {self.input_video_file}")
            # Update UI with selected video file
            input_video_label = self.root.nametowidget(self.root.winfo_children()[1])
            input_video_label.config(text=f"Video Selected: {self.input_video_file}")

    def browse_output_video_folder(self):
        self.output_video_folder = filedialog.askdirectory()
        if self.output_video_folder:
            print(f"Output Video Folder: {self.output_video_folder}")
            output_video_folder_label = self.root.nametowidget(self.root.winfo_children()[5])
            output_video_folder_label.config(text=f"Output Video Folder: {self.output_video_folder}")
            self.output_filename = f"{self.output_video_folder}/{self.get_output_filename()}"

    def scale_video(self):
        if not self.input_video_file or not self.output_video_folder:
            messagebox.showerror("Error", "Please select both an input video and an output video folder.")
            return
        
        scale_resolution = self.scale_resolution.get().strip()
        if not scale_resolution:
            messagebox.showerror("Error", "Please provide a scale resolution (e.g., 1280x720).")
            return
        
        self.cancel_button.config(state=tk.NORMAL)
        self.video_progress["value"] = 0
        self.video_progress["maximum"] = 100

        # Construct the ffmpeg command for video scaling
        command = [
            "ffmpeg", "-i", self.input_video_file, 
            "-vf", f"scale={scale_resolution}",  # Apply scaling filter
            "-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k", "-f", "mp4", self.output_filename
        ]
        
        try:
            self.video_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            while True:
                output = self.video_process.stderr.readline()
                if not output:
                    break
                if "frame=" in output:
                    # Extract frame number to update progress bar
                    current_frame = int(output.split("frame=")[1].split("fps=")[0].strip())
                    self.video_progress["value"] = (current_frame / 100)  # Assuming 100 frames

            self.video_progress["value"] = 100  # Set to 100% when the conversion is done
            self.video_progress.update()
            self.video_process.communicate()
            self.cancel_button.config(state=tk.DISABLED)

            messagebox.showinfo("Success", "Video scaling completed successfully.")
            self.preview_button.config(state=tk.NORMAL)
        except Exception as e:
            print(f"Error scaling video: {e}")
            messagebox.showerror("Error", f"An error occurred while scaling the video: {e}")

    def cancel_conversion(self):
        if self.video_process:
            self.video_process.terminate()
        self.cancel_button.config(state=tk.DISABLED)
        self.video_progress["value"] = 0
        print("Conversion canceled.")

    def preview_video(self):
        if not self.output_video_folder:
            messagebox.showerror("Error", "Please select the output video folder.")
            return
        preview_process = subprocess.Popen(["ffplay", self.output_filename, "-loop", "0"])
        preview_process.wait()

    def get_output_filename(self):
        current_datetime = datetime.now()
        return f"{current_datetime.strftime('%d-%m-%Y-%H-%M-%S')}-scaled.mp4"

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoScaler(root)

    # Apply a white theme to the GUI
    root.tk_setPalette(background='white', foreground='black')

    root.mainloop()
