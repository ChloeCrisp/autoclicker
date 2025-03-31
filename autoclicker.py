import pyautogui
import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import keyboard  # For hotkey support

# Settings
click_interval = 1  # Default time between clicks in seconds
click_button = "Left"  # Default button to click
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
        status_label.config(text="Status: Running", foreground="#4CAF50")  # Green

def stop_clicker():
    global running
    running = False
    status_label.config(text="Status: Stopped", foreground="#F44336")  # Red

def update_interval(event=None):
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

def update_click_key(event=None):
    global click_key
    new_key = key_entry.get()
    if len(new_key) == 1:  # Ensure only a single character is allowed
        click_key = new_key
        current_click_key_label.config(text=f"Current Key: {click_key}")
    else:
        messagebox.showerror("Error", "Please enter a single character key.")
        key_entry.delete(0, tk.END)  # Clear the entry field to force correct input

def toggle_mode():
    global use_key_mode
    use_key_mode = not use_key_mode
    mode_label.config(text="Mode: Key Press" if use_key_mode else "Mode: Mouse Click", foreground="#4CAF50")

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
root.geometry("400x550")
root.configure(bg="#FDEBD0")  # Soft pastel background
root.attributes("-topmost", True)

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5, background="#AED6F1", foreground="#1B4F72")
style.configure("TLabel", font=("Arial", 12), background="#FDEBD0", foreground="#4A4A4A")
style.configure("TEntry", font=("Arial", 12), fieldbackground="#FCF3CF", foreground="#4A4A4A")
style.configure("TCombobox", font=("Arial", 12))

# Interval input
ttk.Label(root, text="Enter Interval (seconds) ~ Enter To Save:").pack(pady=5)
interval_entry = ttk.Entry(root)
interval_entry.insert(0, str(click_interval))
interval_entry.pack(pady=5)
interval_entry.bind("<Return>", update_interval)
current_interval_label = ttk.Label(root, text=f"Current Interval: {click_interval} seconds")
current_interval_label.pack(pady=5)

# Button selection using a colorful dropdown
ttk.Label(root, text="Select Mouse Button:").pack(pady=5)
button_var = tk.StringVar(value=click_button)
button_menu = ttk.Combobox(root, textvariable=button_var, values=["Left", "Right"], state="readonly")
button_menu.pack(pady=5)
button_menu.bind("<<ComboboxSelected>>", update_click_button)
current_button_label = ttk.Label(root, text=f"Current Mouse Button: {click_button}")
current_button_label.pack(pady=5)

# Key input
ttk.Label(root, text="Enter A Key ~ Press Enter To Save:").pack(pady=5)
key_entry = ttk.Entry(root)
key_entry.insert(0, str(click_key))
key_entry.pack(pady=5)
key_entry.bind("<Return>", update_click_key)
current_click_key_label = ttk.Label(root, text=f"Current Key: {click_key}")
current_click_key_label.pack(pady=5)

# Mode toggle
mode_toggle_button = ttk.Button(root, text="Toggle Mode", command=toggle_mode)
mode_toggle_button.pack(pady=5)
mode_label = ttk.Label(root, text="Mode: Mouse Click", foreground="#4CAF50")
mode_label.pack(pady=5)

# Buttons
start_button = ttk.Button(root, text="Start / F7", command=start_clicker)
start_button.pack(pady=5)
stop_button = ttk.Button(root, text="Stop / F8", command=stop_clicker)
stop_button.pack(pady=5)

# Status label
status_label = ttk.Label(root, text="Status: Stopped", foreground="#F44336")
status_label.pack(pady=10)

# Start the hotkey listener in a separate thread
threading.Thread(target=hotkey_listener, daemon=True).start()

# Run the GUI
root.mainloop()