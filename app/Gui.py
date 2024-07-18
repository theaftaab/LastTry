import tkinter as tk
from tkinter import filedialog, ttk
from ttkthemes import ThemedStyle
from threading import Thread
import os
from Main import CHECK

# File types accepted for upload
ALLOWED_FILE_TYPES = [
    ("File Types", ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "*.webp"])
]

# Default document type
DEFAULT_DOCUMENT_TYPE = "Invoice"

def upload_file():
    file_button.config(state="disabled")  # Disable the file browse button
    file_path = filedialog.askopenfilename(filetypes=ALLOWED_FILE_TYPES, title="Select Image File")
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
    file_button.config(state="normal")  # Enable the file browse button
    update_process_button_state()  # Update the state of the process button

def process_file():
    file_entry.config(state="disabled")  # Disable the file entry text box
    file_button.config(state="disabled")  # Disable the file browse button
    document_dropdown.config(state="disabled")  # Disable the document dropdown
    process_button.config(state="disabled")  # Disable the process button
    result_text.config(state="normal")  # Enable the text box for editing
    result_text.delete("1.0", tk.END)  # Clear any previous content
    result_text.insert(tk.END, "Processing...\n")  # Show processing message

    progress_frame.grid(row=4, column=0, pady=10, sticky="ew")  # Show progress bar
    progress_bar.start(10)  # Start the progress bar

    file_path = file_entry.get()
    document_type = document_var.get()
    if file_path and document_type:
        def process_and_display_result():
            result = CHECK(document_type, file_path)
            result_text.config(state="normal")  # Enable the text box for editing
            result_text.insert(tk.END, result)  # Display result
            result_text.config(state="disabled")  # Disable the text box for editing
            progress_bar.stop()  # Stop the progress bar
            progress_frame.grid_remove()  # Hide progress bar
            file_entry.config(state="normal")  # Enable the file entry text box
            file_button.config(state="normal")  # Enable the file browse button
            document_dropdown.config(state="normal")  # Enable the document dropdown
            update_process_button_state()  # Update the state of the process button

        Thread(target=process_and_display_result).start()

def update_process_button_state():
    # Disable the process button if file entry is empty
    if not file_entry.get():
        process_button.config(state="disabled")
    else:
        process_button.config(state="normal")

# Create the main window
root = tk.Tk()
root.title("Similar Document Template Matching Algorithm")

# Apply the theme
style = ThemedStyle(root)
if tk.TkVersion >= 8.6:
    style.set_theme("breeze")  # Choose the theme for Windows
else:
    style.set_theme("aqua")  # Choose the theme for macOS

# Set minimum window size
root.minsize(600, 400)

# Frame for title
title_frame = ttk.Frame(root, padding="10")
title_frame.grid(row=0, column=0)

# Title label
title_label = ttk.Label(title_frame, text="Similar Document Template Matching Algorithm", font=("Poppins", 16))
title_label.grid(row=0, column=0, padx=10, pady=10)  # Center the label using sticky="ew"

# Frame for file selection
file_frame = ttk.Frame(root, padding="10")
file_frame.grid(row=1, column=0)

# File selection label and entry
ttk.Label(file_frame, text="Select Image File:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
file_entry = ttk.Entry(file_frame)
file_entry.grid(row=0, column=1, padx=5, pady=5)
file_entry.bind("<KeyRelease>", lambda e: update_process_button_state())  # Bind key release event to update process button state
file_button = ttk.Button(file_frame, text="Browse", command=upload_file)
file_button.grid(row=0, column=2, padx=5, pady=5)

# Configure grid weights for file_frame
file_frame.columnconfigure(1, weight=1)

# Frame for document type selection
document_frame = ttk.Frame(root, padding="10")
document_frame.grid(row=2, column=0, sticky="ew")

# Document type label and dropdown
ttk.Label(document_frame, text="Select Document Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
document_var = tk.StringVar(value=DEFAULT_DOCUMENT_TYPE)
document_dropdown = ttk.Combobox(document_frame, textvariable=document_var, values=["Invoice", "Prescription", "Labreport"])
document_dropdown.grid(row=0, column=1, padx=5, pady=5) #, sticky="ew"

# Set validation to restrict document dropdown to predefined values
validate_doc = root.register(lambda x: x in {"Invoice", "Prescription", "Labreport"})
document_dropdown.config(validate="key", validatecommand=(validate_doc, '%P'))

# Configure grid weights for document_frame
document_frame.columnconfigure(1, weight=1)

# Process button
process_button = ttk.Button(root, text="Process", command=process_file)
process_button.grid(row=3, column=0, padx=10, pady=10)

# Configure grid weights for process_button
root.columnconfigure(0, weight=1)

# Frame for progress bar
progress_frame = ttk.Frame(root, padding="10")
progress_frame.grid(row=4, column=0)
progress_frame.grid_remove()  # Hide progress bar frame initially

progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="indeterminate")
progress_bar.grid(row=0, column=0, padx=5, pady=5)

# Configure grid weights for progress_frame
progress_frame.columnconfigure(0, weight=1)

# Frame for result text area
result_frame = ttk.Frame(root, padding="10")
result_frame.grid(row=5, column=0, sticky="nsew")
result_frame.columnconfigure(0, weight=1)
result_frame.rowconfigure(0, weight=1)

# Result text area
result_text = tk.Text(result_frame, wrap="word", state="disabled")
result_text.grid(row=0, column=0, padx=5, pady=5) #

# Add scrollbars to result text area
result_scroll_vertical = ttk.Scrollbar(result_frame, orient="vertical", command=result_text.yview)
result_scroll_vertical.grid(row=0, column=1, sticky="ns")
result_text.configure(yscrollcommand=result_scroll_vertical.set)

result_scroll_horizontal = ttk.Scrollbar(result_frame, orient="horizontal", command=result_text.xview)
result_scroll_horizontal.grid(row=1, column=0, sticky="ew")
result_text.configure(xscrollcommand=result_scroll_horizontal.set)

# Configure the main window to expand with the resizing of the result text area
root.rowconfigure(5, weight=1)
root.columnconfigure(0, weight=1)

# Initial update of process button state
update_process_button_state()

# Start the GUI
root.mainloop()
