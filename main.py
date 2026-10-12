import subprocess
import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

FFMPEG = r"C:\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"

# Each preset = label shown in UI -> FFmpeg flags
PRESETS = {
    "Fast (libshine, 128k)": {
        "flags": [
            "-acodec", "libshine",
            "-ab", "128k",
            "-threads", "0",
        ]
    },
    "Balanced (libmp3lame, VBR ~190k)": {
        "flags": [
            "-acodec", "libmp3lame",
            "-q:a", "2",
            "-threads", "0",
        ]
    },
    "Best quality (libmp3lame, 320k)": {
        "flags": [
            "-acodec", "libmp3lame",
            "-ab", "320k",
            "-threads", "0",
        ]
    },
}


def convert(video_path, mp3_path, preset_name, status_label, convert_btn):
    try:
        status_label.config(text="Converting...")
        convert_btn.config(state="disabled")

        # Common flags shared by all presets
        cmd = [
            FFMPEG,
            "-i", video_path,
            "-vn",              # no video
            "-sn",              # no subtitles
            "-dn",              # no data streams
            "-map", "0:a:0",    # only the first audio track
        ]
        # Append the preset-specific flags
        cmd += PRESETS[preset_name]["flags"]
        cmd += ["-y", mp3_path]

        subprocess.run(cmd, check=True)

        status_label.config(text=f"✅ Done → {os.path.basename(mp3_path)}")
        messagebox.showinfo("Success", f"Saved:\n{mp3_path}\n\nPreset: {preset_name}")

    except subprocess.CalledProcessError:
        status_label.config(text="❌ Conversion failed")
        messagebox.showerror("Error", "FFmpeg failed. Check the file format.")
    except FileNotFoundError:
        status_label.config(text="❌ FFmpeg not found")
        messagebox.showerror("Error", f"FFmpeg not found at:\n{FFMPEG}")
    finally:
        convert_btn.config(state="normal")


def pick_and_convert(video_var, preset_var, status_label, convert_btn):
    video_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=[
            ("Video files", "*.mp4 *.avi *.mkv *.mov *.flv *.webm *.wmv *.m4v"),
            ("All files", "*.*"),
        ],
    )
    if not video_path:
        return

    video_var.set(video_path)
    mp3_path = os.path.splitext(video_path)[0] + ".mp3"

    threading.Thread(
        target=convert,
        args=(video_path, mp3_path, preset_var.get(),
              status_label, convert_btn),
        daemon=True,
    ).start()


def build_ui():
    root = tk.Tk()
    root.title("Video → MP3 Converter")
    root.geometry("560x320")
    root.resizable(False, False)

    # Title
    tk.Label(root, text="Video to MP3 Converter",
             font=("Segoe UI", 16, "bold")).pack(pady=(15, 5))

    # File row
    video_var = tk.StringVar()
    row = tk.Frame(root)
    row.pack(pady=8, padx=15, fill="x")
    tk.Label(row, text="Video:", width=8, anchor="w").pack(side="left")
    tk.Entry(row, textvariable=video_var, width=50).pack(side="left", padx=5)

    # Quality preset row
    preset_var = tk.StringVar(value="Balanced (libmp3lame, VBR ~190k)")
    row2 = tk.Frame(root)
    row2.pack(pady=8, padx=15, fill="x")
    tk.Label(row2, text="Quality:", width=8, anchor="w").pack(side="left")
    ttk.Combobox(
        row2,
        textvariable=preset_var,
        width=38,
        state="readonly",
        values=list(PRESETS.keys()),
    ).pack(side="left", padx=5)

    # Preset help text
    help_label = tk.Label(
        root,
        text=("Fast = quickest, smallest file   •   "
              "Balanced = best size/quality   •   "
              "Best = max quality"),
        font=("Segoe UI", 9), fg="gray",
    )
    help_label.pack(pady=(0, 5))

    # Status
    status_label = tk.Label(root, text="Select a video to begin.",
                            font=("Segoe UI", 10), fg="gray")
    status_label.pack(pady=(15, 5))

    # Convert button
    convert_btn = tk.Button(
        root, text="📂 Choose Video & Convert",
        font=("Segoe UI", 11, "bold"),
        bg="#0078D4", fg="white",
        activebackground="#005A9E", activeforeground="white",
        padx=20, pady=8, cursor="hand2", border=0,
        command=lambda: pick_and_convert(
            video_var, preset_var, status_label, convert_btn
        ),
    )
    convert_btn.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    build_ui()