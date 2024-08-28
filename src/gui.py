import tkinter as tk
from tkinter import messagebox
from logger import setup_gui_logger
from utils import save_facet_values 

def create_main_window():
    root = tk.Tk()
    root.title("Timeflip Logger")
    
    # Set the icon for the main window using PhotoImage
    icon_path = 'assets/app_icon.png'
    icon_image = tk.PhotoImage(file=icon_path)
    root.iconphoto(False, icon_image)

    # Create a frame for the facet inputs
    facet_frame = tk.Frame(root)
    facet_frame.pack(pady=10)

    # Create and store values for 12 facets
    facet_entries = {}
    for i in range(1, 13):
        label = tk.Label(facet_frame, text=f"Facet {i}:")
        label.grid(row=i-1, column=0, padx=5, pady=5)
        
        entry = tk.Entry(facet_frame)
        entry.grid(row=i-1, column=1, padx=5, pady=5)
        facet_entries[f'Facet {i}'] = entry
        
    # Create SAVE button
    save_button = tk.Button(root, text='SAVE', command=lambda: save_facet_values_on_click(facet_entries))
    save_button.pack(pady=5)

    # Create a text widget to display logs
    log_text = tk.Text(root, width=80, height=20)
    log_text.pack()

    # Set up logger
    setup_gui_logger(log_text)

    # Modify close event to hide the window instead of closing the app
    root.protocol("WM_DELETE_WINDOW", lambda: root.withdraw())

    return root, facet_entries, log_text

def save_facet_values_on_click(facet_entries):
    save_facet_values(facet_entries)
    messagebox.showinfo('Success', 'Facet values saved!')

def start_gui_event_loop(root):
    root.mainloop()