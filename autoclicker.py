import pyautogui
import time
import threading
import tkinter as tk
from tkinter import messagebox
import keyboard  # For hotkey support

# Settings
click_interval = 1  # Default time between clicks in seconds
click_button = "left"  # Default button to click
hotkey_start = "f7"
hotkey_stop = "f8"

running = False

# Functions
def clicker():
    global running
    while running:
        pyautogui.click(button=click_button)
        time.sleep(click_interval)

def start_clicker():
    global running
    if not running:
        running = True
        threading.Thread(target=clicker, daemon=True).start()
        status_label.config(text="Status: Running", fg="green")

def stop_clicker():
    global running
    running = False
    status_label.config(text="Status: Stopped", fg="red")

def update_interval():
    global click_interval
    try:
        new_interval = float(interval_entry.get())
        if new_interval > 0:
            click_interval = new_interval
            messagebox.showinfo("Success", f"Click interval updated to {click_interval} seconds.")
        else:
            messagebox.showerror("Error", "Interval must be greater than 0.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

def update_click_button(selected_button):
    global click_button
    click_button = selected_button
    messagebox.showinfo("Success", f"Click button updated to '{click_button}'.")

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

# Set the size of the window (e.g., 600x400 pixels)
root.geometry("600x400")

# Interval input
tk.Label(root, text="Click Interval (seconds):").pack(pady=5)
interval_entry = tk.Entry(root)
interval_entry.insert(0, str(click_interval))
interval_entry.pack(pady=5)

# Click button selection
tk.Label(root, text="Click Button:").pack(pady=5)
click_button_var = tk.StringVar(value=click_button)
click_button_menu = tk.OptionMenu(root, click_button_var, "left", "right", command=update_click_button)
click_button_menu.pack(pady=5)

# Buttons
start_button = tk.Button(root, text="Start", command=start_clicker, bg="green", fg="white")
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=stop_clicker, bg="red", fg="white")
stop_button.pack(pady=5)

update_button = tk.Button(root, text="Update Interval", command=update_interval)
update_button.pack(pady=5)

# Status label
status_label = tk.Label(root, text="Status: Stopped", fg="red")
status_label.pack(pady=10)

# Start the hotkey listener in a separate thread
threading.Thread(target=hotkey_listener, daemon=True).start()

# Run the GUI
root.mainloop()