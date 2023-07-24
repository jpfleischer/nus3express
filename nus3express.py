import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from main import runner

def start_button(selected_file):
    if selected_file:
        # Your function code here (e.g., process the selected file)
        print("Start button clicked! Selected file:", selected_file)
    else:
        messagebox.showinfo("Error", "Please choose a file.")

def open_file_dialog():
    selected_file = filedialog.askopenfilename(initialdir='.')
    if selected_file:
        runner(selected_file)
    exit()

# Create the main application window
root = tk.Tk()
root.title("File Selection GUI")

# Set the default size of the GUI
root.geometry("400x120")

# Add a label to instruct the user
label = tk.Label(root, text="Choose your nus3audio file:")
label.pack(pady=10)

# Add a button to open the file dialog
file_button = tk.Button(root, text="Select File", command=open_file_dialog)
file_button.pack(pady=5)

# Run the main event loop
root.mainloop()
