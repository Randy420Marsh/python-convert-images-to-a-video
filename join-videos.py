import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import subprocess
import os

class VideoJoiner:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Joiner (Side-by-Side)")
        self.video1_file = ""
        self.video2_file = ""
        self.output_video_folder = ""
        self.output_filename = ""
        self.video_process = None
        self.create_widgets()

    def create_widgets(self):
        # Select First Video
        input_video1_label = tk.Label(self.root, text="Select First Video:")
        input_video1_label.pack()
        input_video1_button = tk.Button(self.root, text="Browse", command=self.browse_video1_file)
        input_video1_button.pack()

        # Select Second Video
        input_video2_label = tk.Label(self.root, text="Select Second Video:")
        input_video2_label.pack()
        input_video2_button = tk.Button(self.root, text="Browse", command=self.browse_video2_file)
        input_video2_button.pack()

        # Output Video Folder
        output_video_label = tk.Label(self.root, text="Output Video Folder:")
        output_video_label.pack()
        output_video_folder_label = tk.Label(self.root, text="")
        output_video_folder_label.pack()
        output_video_button = tk.Button(self.root, text="Browse", command=self.browse_output_video_folder)
        output_video_button.pack()

        # Join Videos button
        join_video_button = tk.Button(self.root, text="Join Videos Side-by-Side", command=self.join_videos)
        join_video_button.pack()
        self.video_progress = Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.video_progress.pack()

        # Cancel button
        cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel_conversion, state=tk.DISABLED)
        cancel_button.pack()
        self.cancel_button = cancel_button

    def browse_video1_file(self):
        self.video1_file = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if self.video1_file:
            print(f"First Video Selected: {self.video1_file}")
            input_video1_label = self.root.nametowidget(self.root.winfo_children()[1])
            input_video1_label.config(text=f"First Video Selected: {self.video1_file}")

    def browse_video2_file(self):
        self.video2_file = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if self.video2_file:
            print(f"Second Video Selected: {self.video2_file}")
            input_video2_label = self.root.nametowidget(self.root.winfo_children()[3])
            input_video2_label.config(text=f"Second Video Selected: {self.video2_file}")

    def browse_output_video_folder(self):
        self.output_video_folder = filedialog.askdirectory()
        if self.output_video_folder:
            print(f"Output Video Folder: {self.output_video_folder}")
            output_video_folder_label = self.root.nametowidget(self.root.winfo_children()[5])
            output_video_folder_label.config(text=f"Output Video Folder: {self.output_video_folder}")
            self.output_filename = f"{self.output_video_folder}/{self.get_output_filename()}"

    def join_videos(self):
        if not self.video1_file or not self.video2_file or not self.output_video_folder:
            messagebox.showerror("Error", "Please select both input videos and an output folder.")
            return
        
        self.cancel_button.config(state=tk.NORMAL)
        self.video_progress["value"] = 0
        self.video_progress["maximum"] = 100

        # Construct the ffmpeg command for side-by-side video join
        command = [
            "ffmpeg", "-i", self.video1_file, "-i", self.video2_file,
            "-filter_complex", "[0:v][1:v]hstack=inputs=2[v]",
            "-map", "[v]", "-c:v", "libx264", "-crf", "0", "-preset", "veryfast", 
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

            messagebox.showinfo("Success", "Videos joined successfully.")
        except Exception as e:
            print(f"Error joining videos: {e}")
            messagebox.showerror("Error", f"An error occurred while joining the videos: {e}")

    def cancel_conversion(self):
        if self.video_process:
            self.video_process.terminate()
        self.cancel_button.config(state=tk.DISABLED)
        self.video_progress["value"] = 0
        print("Video join operation canceled.")

    def get_output_filename(self):
        return f"joined_side_by_side_{os.path.basename(self.video1_file).split('.')[0]}_{os.path.basename(self.video2_file).split('.')[0]}.mp4"

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoJoiner(root)

    # Apply a white theme to the GUI
    root.tk_setPalette(background='white', foreground='black')

    root.mainloop()
