import os
import sys
import tkinter as tk
from tkinter import ttk
import csv
from tkinter import filedialog
import configparser
from PIL import Image, ImageTk

# Change the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Configuration setup
config = configparser.ConfigParser()
config_file = "config.ini"

if os.path.exists(config_file):
    config.read(config_file)
    default_csv_file_path = config.get("Settings", "csv_path", fallback="Default.csv")
else:
    default_csv_file_path = "Default.csv"

csv_file_path = default_csv_file_path  # Global variable for CSV file path

print("Current Working Directory:", os.getcwd())
print("Current Database:", csv_file_path)

def save_config():
    """Saves the current configuration to config.ini."""
    config["Settings"] = {"csv_path": csv_file_path}
    with open(config_file, "w") as configfile:
        config.write(configfile)

def find_error_code(query):
    """Finds the matching codes, HEX, and DESCRIPTION for a given query."""
    global csv_file_path
    if not os.path.exists(csv_file_path):
        return "Database file not found. Please select a database.", "", "", ""

    try:
        stripped_query = query.split("-")[0]  # Keep only the numeric core (e.g., "108255")
        matches = []  # Collect all matching rows

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Compare the numeric core of the codes in the CSV
                core_code = row['CODE'].split("-")[1] if "-" in row['CODE'] else row['CODE']
                if core_code.startswith(stripped_query):  # Match core with partial or full query
                    matches.append(row)

        if len(matches) == 1:  # Exactly one match found
            return (
                matches[0]['CODE'],
                matches[0]['HEX'],
                matches[0]['DESCRIPTION'],
                ""
            )
        elif len(matches) > 1:  # More than one match
            return "", "", "", f"Multiple matches found: {', '.join([m['CODE'] for m in matches])}"
        else:  # No match
            return "Code not found.", "", "", ""

    except Exception as e:
        return f"An error occurred: {e}", "", "", ""


def search_and_display():
    """Searches for the error code and displays the results."""
    code = code_input_var.get().strip()  # Get the user input from the text box
    code_result, hex_result, desc_result, multiple_match_result = find_error_code(code)

    # Update the output fields
    code_var.set(code_result)
    hex_var.set(hex_result)
    update_description(desc_result)  # Pass the dynamic description here
    close_match_var.set(multiple_match_result)



def select_csv():
    """Opens a file dialog to select the CSV file."""
    global csv_file_path
    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if csv_file_path:
        csv_path_var.set(f"Database Path: {csv_file_path}") # Update CSV path StringVar
        save_config()  # Save the config when a new CSV is selected.

def load_asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)

def print_coordinates(event):
    """Prints the coordinates of the clicked widget."""
    widget = event.widget
    x = widget.winfo_x()
    y = widget.winfo_y()
    print(f"{widget}: Coordinates: ({x}, {y})")

window = tk.Tk()
window.geometry("862x519")
window.configure(bg="#3a7ff6")
window.title("Playstation 5 - Software Error Lookup")

canvas = tk.Canvas(
    window,
    bg = "#3a7ff6",
    width = 862,
    height = 519,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x=0, y=0)

canvas.create_rectangle(468, 0, 862, 519, fill='#fcfcfc', outline="")

# --- StringVars for output ---
code_var = tk.StringVar()
hex_var = tk.StringVar()
description_var = tk.StringVar()
csv_path_var = tk.StringVar()
close_match_var = tk.StringVar()
code_input_var = tk.StringVar() # StringVar for input

code_output_entry = tk.Entry( # Output CODE Text box - .!entry
    window,
    bd=0,
    bg="#f1f5ff",
    fg="#000000", # Changed to black for visibility
    insertbackground="#000000", # Changed to black for visibility
    highlightthickness=0,
    textvariable=code_var, # Linked StringVar
    font=("ABeeZee", 16, "bold"),
    state="readonly" # Make it readonly
)
code_output_entry.place(x=492, y=191, width=345, height=61)
code_output_entry.bind("<Button-1>", print_coordinates)

hex_output_entry = tk.Entry( # output HEX Textbox - .!entry2
    window,
    bd=0,
    bg="#f1f5ff",
    fg="#000000", # Changed to black for visibility
    insertbackground="#000000", # Changed to black for visibility
    highlightthickness=0,
    textvariable=hex_var, # Linked StringVar
    font=("ABeeZee", 16, "bold"),
    state="readonly" # Make it readonly
)
hex_output_entry.place(x=492, y=289, width=345, height=61)
hex_output_entry.bind("<Button-1>", print_coordinates)

description_output_entry = tk.Text(  # Output Description Text Box - .!entry3
    window,
    bd=0,
    bg="#f1f5ff",
    fg="#000000",  # Changed to black for visibility
    wrap="word",  # Wrap text by words
    font=("ABeeZee", 16, "bold"),
    state="disabled",  # Make it readonly
    highlightthickness=0,
)
description_output_entry.place(x=492, y=402, width=345, height=102)
# Function to update the content of the description_output_entry
def update_description(text):
    description_output_entry.config(state="normal")  # Enable the text box for editing
    description_output_entry.delete(1.0, "end")  # Clear existing content
    description_output_entry.insert("end", text)  # Insert new content
    description_output_entry.config(state="disabled")  # Set it back to readonly

# Example of using the function to insert text
update_description("Type the Code in the search box to lookup the error code.")  # Initial description

description_output_entry.bind("<Button-1>", print_coordinates)

from tkinter import Canvas, Entry, Label
from PIL import Image, ImageTk

# Create a canvas to house the text box and icon
entry_canvas = Canvas(window, bg="#f1f5ff", bd=0, highlightthickness=0, relief="flat")
entry_canvas.place(x=475, y=40, width=370, height=60)  # Same size as the text box

# Create the Entry widget (text box)
code_entry = Entry(
    entry_canvas,
    bd=0,
    bg="#f1f5ff",
    fg="#000000",
    insertbackground="#000000",
    highlightthickness=0,
    textvariable=code_input_var,
    font=("ABeeZee", 16, "bold"),
    justify="center",  # Center-align the text
)
code_entry.place(x=0, y=0, width=260, height=69)  # Adjusted width to leave more space for the icon

# Load and resize the image
original_image = Image.open(load_asset("a.png")).convert("RGBA")
resized_image = original_image.resize((40, 40), Image.Resampling.LANCZOS)
search_icon_image = ImageTk.PhotoImage(resized_image)

# Create a label for the icon
icon_label = Label(
    entry_canvas,
    image=search_icon_image,
    bg="#f1f5ff",  # Match the text box background
    borderwidth=0,
)
icon_label.place(x=320, y=15, width=40, height=40)  # Positioned at the end of the text box

# Bind the click event to perform a search
icon_label.bind("<Button-1>", lambda e: search_and_display())  # Bind left-click to search function

# Keep a reference to avoid garbage collection
icon_label.image = search_icon_image


csv_path_entry = tk.Entry( # Current Data base file from config.ini text box  - .!entry5
    window,
    bd=0,
    bg="#f1f5ff",
    fg="#000000", # Changed to black for visibility
    insertbackground="#000000", # Changed to black for visibility
    highlightthickness=0,
    font=("ABeeZee", 10, "bold"),
    textvariable=csv_path_var, # Linked StringVar
    state="readonly" # Make it readonly
)
csv_path_entry.place(x=36, y=333, width=345, height=61)
csv_path_entry.bind("<Button-1>", print_coordinates)
csv_path_var.set(f": {default_csv_file_path}") # Set initial CSV path

select_csv_button_image = tk.PhotoImage(file=load_asset("2.png")) # button 2 Select CSVD

select_csv_button = tk.Button(
    window,
    image=select_csv_button_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=select_csv # Call select_csv function
)
select_csv_button.place(x=339, y=353, width=24, height=22)
select_csv_button.bind("<Button-1>", print_coordinates)

close_match_label = tk.Label( # Label for multiple match message
    window,
    bg="#3a7ff6",
    fg="yellow",
    text="",
    font=("Arial", 10, "italic")
)
close_match_label.place(x=475, y=95, width=370, height=20) # Position below search box


canvas.create_text(
    725,
    35,
    anchor="nw",
    text="Search",
    fill="#ffffff",
    font=("ABeeZee", 20 * -1)
)

canvas.create_text(
    91,
    281,
    anchor="nw",
    text="Current Database File",
    fill="#ffffff",
    font=("ABeeZee", 20 * -1)
)

canvas.create_text(
    23,
    22,
    anchor="nw",
    text="Error Code Search",
    fill="#ffffff",
    font=("ABeeZee", 48 * -1)
)

canvas.create_text(
    3,
    400,
    anchor="nw",
    text="*Default Database : https://www.psdevwiki.com/ps5/Error_Codes*",
    fill="#000000",
    font=("ABeeZee", 15 * -1, "bold")
)

canvas.create_text(
    492,
    10,
    anchor="nw",
    text="SEARCH",
    fill="#3a7ff6",
    font=("ABeeZee", 20 * -1)
)


canvas.create_text(
    350,
    100,
    anchor="nw",
    text="By Dony.",
    fill="#ffffff",
    font=("ABeeZee", 20 * -1)
)

canvas.create_text(
    492,
    159,
    anchor="nw",
    text="CODE",
    fill="#3a7ff6",
    font=("ABeeZee", 20 * -1)
)

canvas.create_text(
    492,
    260,
    anchor="nw",
    text="HEX",
    fill="#3a7ff6",
    font=("ABeeZee", 20 * -1)
)

canvas.create_text(
    489,
    364,
    anchor="nw",
    text="DESCRIPTION",
    fill="#3a7ff6",
    font=("ABeeZee", 20 * -1)
)

canvas.create_text(
    23,
    466,
    anchor="nw",
    text="GIT: https://github.com/apewalkers",
    fill="#ffffff",
    font=("ABeeZee", 13 * -1)
)

canvas.create_text(
    22,
    491,
    anchor="nw",
    text="Donations : https://www.paypal.me/Dannyjohn08",
    fill="#ffffff",
    font=("ABeeZee", 13 * -1)
)

window.resizable(False, False)
window.mainloop()