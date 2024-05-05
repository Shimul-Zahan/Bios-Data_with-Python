import tkinter as tk
from tkinter import messagebox

def show_message_box():
    messagebox.showinfo("Message", "Hello, Windows!")

# Create the main application window
root = tk.Tk()
root.title("Windows Programming in Python")

# Create a button widget
button = tk.Button(root, text="Click Me", command=show_message_box)
button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
