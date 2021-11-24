import tkinter
from tkinter import simpledialog
from time import sleep

x = tkinter.Tk()
sleep(1)
x.withdraw()
# shows a dialogue with a string input field
youtube_url = simpledialog.askstring('YouTube URL', 'Enter the youtube URL of the video', parent=x)
print(youtube_url)