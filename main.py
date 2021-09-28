import tkinter as tk
import youtube_dl
from pathlib import Path
import moviepy.editor as mp
import os
import time

downloads_path = str(Path.home() / "Downloads")

def set_status(m, text):
    m.config(text=text)

def download_video():
    url = ent_url.get()
    status = f"Downloading video..."
    print(status)
    set_status(lbl_status, status)
    time.sleep(1)
    audioOnly = audioVar.get()
    print(f"Audio Only: {audioOnly}")
    ydl_opts = {
        'nocheckcertificate': True,
        'outtmpl': f'{downloads_path}/%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', None)
        ydl.download([url])
    if audioOnly == 0:
        print("Download complete!")
        lbl_status["text"] = "Download complete!"
        ent_url.delete(0, 'end')
    else:
        print("Converting to MP3...")
        lbl_status["text"] = "Converting to MP3..."
        for file in os.listdir(downloads_path):
            if file.startswith(title) and file[-4:] != ".mp3":
                search_file = file
        clip_name = downloads_path + "/" + search_file
        final_name = os.path.splitext(clip_name)[0]
        print(clip_name)
        video_clip = mp.VideoFileClip(fr"{clip_name}")
        video_clip.audio.write_audiofile(fr"{final_name}.mp3")
        os.remove(clip_name)
        lbl_status["text"] = "Download complete!"


window = tk.Tk()
window.title("PyVideoDownloader")

frm_entry = tk.Frame(master=window)

audioVar = tk.IntVar()
chk_audioOnly = tk.Checkbutton(master=frm_entry, text="Audio Only", variable=audioVar, onvalue=1, offvalue=0).grid(row=0, sticky="n")

ent_url = tk.Entry(master=frm_entry, width=50)


ent_url.grid(row=1, column=0, sticky="e")


btn_download = tk.Button(
    master=window,
    text="\nDownload",
    command=download_video
)

lbl_status = tk.Label(master=window, text="Status")

# Set-up the layout using the .grid() geometry manager
frm_entry.grid(row=0, column=0, padx=10)
btn_download.grid(row=0, column=1, pady=10)
lbl_status.grid(row=1, column=0, padx=10)

# Run the application
window.mainloop()
