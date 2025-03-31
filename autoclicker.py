import pyautogui
import time
import threading
import tkinter as tk
from tkinter import messagebox
import keyboard  # For hotkey support

# Settings
click_interval = 1  # Default time between clicks in seconds
click_button = "left"  # Default button to click
click_key = "a"  # Default key to press
hotkey_start = "f7"
hotkey_stop = "f8"

running = False
use_key_mode = False  # Whether to use key mode instead of mouse clicks

# Functions
def clicker():
    global running
    while running:
        if use_key_mode:
            pyautogui.press(click_key)  # Simulate key press
        else:
            pyautogui.click(button=click_button)  # Simulate mouse click
        time.sleep(click_interval)

def start_clicker():
    global running
    if not running:
        running = True
        threading.Thread(target=clicker, daemon=True).start()
        status_label.config(text="Status: Running", fg="#4CAF50")  # Green

def stop_clicker():
    global running
    running = False
    status_label.config(text="Status: Stopped", fg="#F44336")  # Red

def update_interval(event=None):  # Add `event` parameter to handle key binding
    global click_interval
    try:
        new_interval = float(interval_entry.get())
        if new_interval > 0:
            click_interval = new_interval
            current_interval_label.config(text=f"Current Interval: {click_interval} seconds")
        else:
            messagebox.showerror("Error", "Interval must be greater than 0.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

def update_click_button(*args):
    global click_button
    click_button = button_var.get()  # Get value from dropdown
    current_button_label.config(text=f"Current Mouse Button: {click_button}")

def update_click_key(event=None): # Add `event` parameter to handle key binding
    global click_key
    new_key = key_entry.get()
    if new_key:
        click_key = new_key
        current_click_key_label.config(text=f"Current Key: {click_key}")
    else:
        messagebox.showerror("Error", "Please enter a valid key.")

def toggle_mode():
    global use_key_mode
    use_key_mode = not use_key_mode
    if use_key_mode:
        mode_label.config(text="Mode: Key Press", fg="#4CAF50")  # Green
    else:
        mode_label.config(text="Mode: Mouse Click", fg="#4A4A4A")  # Gray

def hotkey_listener():
    while True:
        if keyboard.is_pressed(hotkey_start):
            start_clicker()
        elif keyboard.is_pressed(hotkey_stop):
            stop_clicker()
        time.sleep(0.1)  # Prevent high CPU usage

# Create the GUI
root = tk.Tk()
root.title("Autoclicker")

# Set the size of the window
root.geometry("400x500")

# Set pastel background color
root.configure(bg="#F8E8E8")  # Light pastel pink

# Always on top
root.attributes("-topmost", True)

# Interval input
tk.Label(root, text="Enter A Interval (seconds) ~ Enter To Save:", bg="#F8E8E8", fg="#4A4A4A", font=("Arial", 12)).pack(pady=5)
interval_entry = tk.Entry(root, font=("Arial", 12), bg="#FFF8DC", fg="#4A4A4A")
interval_entry.insert(0, str(click_interval))
interval_entry.pack(pady=5)

# Bind the Enter key to update the interval
interval_entry.bind("<Return>", update_interval)

# Add a label to display the current interval
current_interval_label = tk.Label(root, text=f"Current Interval: {click_interval} seconds", bg="#F8E8E8", fg="#4A4A4A", font=("Arial", 12))
current_interval_label.pack(pady=5)

# Button selection using a dropdown
tk.Label(root, text="Select Mouse Button:", bg="#F8E8E8", fg="#4A4A4A", font=("Arial", 12)).pack(pady=5)

button_var = tk.StringVar(value=click_button)  # Stores the selected button
button_menu = tk.OptionMenu(root, button_var, "left", "right", command=update_click_button)
button_menu.config(font=("Arial", 12), bg="#FFF8DC", fg="#4A4A4A")
button_menu.pack(pady=5)

def update_click_button(*args):
    global click_button
    click_button = button_var.get()
    current_button_label.config(text=f"Current Mouse Button: {click_button}")

# Add a label to display the current mouse button
current_button_label = tk.Label(root, text=f"Current Mouse Button: {click_button}", bg="#F8E8E8", fg="#4A4A4A", font=("Arial", 12))
current_button_label.pack(pady=5)

# Key input
tk.Label(root, text="Enter A Key ~ Press Enter To Save:", bg="#F8E8E8", fg="#4A4A4A", font=("Arial", 12)).pack(pady=5)
key_entry = tk.Entry(root, font=("Arial", 12), bg="#FFF8DC", fg="#4A4A4A")
key_entry.insert(0, str(click_key))
key_entry.pack(pady=5)

# Bind the Enter key to update the key
key_entry.bind("<Return>", update_click_key)

# Add a label to display the current click button
current_click_key_label = tk.Label(root, text=f"Current Key: {click_button}", bg="#F8E8E8", fg="#4A4A4A", font=("Arial", 12))
current_click_key_label.pack(pady=5)

# Mode toggle
mode_toggle_button = tk.Button(root, text="Toggle Mode", command=toggle_mode, bg="#AEDFF7", fg="#4A4A4A", font=("Arial", 12))
mode_toggle_button.pack(pady=5)

# Mode label
mode_label = tk.Label(root, text="Mode: Mouse Click", bg="#F8E8E8", fg="#4A4A4A", font=("Arial", 12))
mode_label.pack(pady=5)

# Buttons
start_button = tk.Button(root, text="Start / F7", command=start_clicker, bg="#AEDFF7", fg="#4A4A4A", font=("Arial", 12))
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop / F8", command=stop_clicker, bg="#F7A8A8", fg="#4A4A4A", font=("Arial", 12))
stop_button.pack(pady=5)

# Status label
status_label = tk.Label(root, text="Status: Stopped", bg="#F8E8E8", fg="#F44336", font=("Arial", 12))
status_label.pack(pady=10)

# Start the hotkey listener in a separate thread
threading.Thread(target=hotkey_listener, daemon=True).start()

# Run the GUI
root.mainloop()