import tkinter as tk
from tkinter import PhotoImage

def analyze_action():
    # Implement your analyze action here
    pass

def search_action():
    # Implement your search action here
    pass

# Create the main window
root = tk.Tk()
root.title("My App")

# Maximize the window to fit the screen
root.state('zoomed')  # This maximizes the window

# Create a black label that covers the entire window
bg_label = tk.Label(root, bg="black")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame for buttons
button_frame = tk.Frame(root, bg="")
button_frame.place(relx=0.5, rely=0.5, anchor="center")

# Create a button for analysis
analyze_button = tk.Button(button_frame, text="Analyze", font=("Helvetica", 24), padx=20, pady=10, command=analyze_action)
analyze_button.pack(pady=10)

# Create a button for searching
search_button = tk.Button(button_frame, text="Search", font=("Helvetica", 24), padx=20, pady=10, command=search_action)
search_button.pack()

# Start the tkinter main loop
root.mainloop()
