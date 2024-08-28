import tkinter as tk
from tkinter import messagebox
from logger import Logger
from utils import save_facet_values 
from config import TOGGL_PROJECT_IDS

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

    # Variables to store facet entries, saved facet values, and project selectors
    facet_entries = {}
    project_selectors = {}
    saved_facet_values = {}
    
    for i in range(1, 13):
        # Create an entry description for each facet
        label = tk.Label(facet_frame, text=f"Facet {i}:")
        label.grid(row=i-1, column=0, padx=5, pady=5)
        entry = tk.Entry(facet_frame)
        entry.grid(row=i-1, column=1, padx=5, pady=5)
        facet_entries[f'Facet {i}'] = entry
        
        # Create a project selector for each facet
        proj_selector = tk.StringVar()
        proj_selector.set('')
        project_selectors[f'Facet {i}'] = proj_selector
        project_selector_menu = tk.OptionMenu(facet_frame, proj_selector, *TOGGL_PROJECT_IDS.values())
        project_selector_menu.grid(row=i-1, column=2, padx=5, pady=5)
        
    # Create SAVE button
    save_button = tk.Button(root, text='SAVE', command=lambda: save_facet_values_on_click(facet_entries, saved_facet_values, project_selectors))
    save_button.pack(pady=5)

    # Create a text widget to display logs
    log_text = tk.Text(root, width=80, height=20)
    log_text.pack()

    # Set up logger
    logger = Logger(log_text)
    gui_logger = logger.logger

    # Modify close event to hide the window instead of closing the app
    root.protocol("WM_DELETE_WINDOW", lambda: root.withdraw())

    return root, facet_entries, gui_logger, saved_facet_values, project_selectors

def save_facet_values_on_click(facet_entries, saved_facet_values, project_selectors):
    for facet, entry in facet_entries.items():
        saved_facet_values[facet] = entry.get()
    for facet, selector in project_selectors.items():
        # Find the project ID based on the selected project name
        project_name = selector.get()
        project_id = next((id for id, name in TOGGL_PROJECT_IDS.items() if name == project_name), None)
        saved_facet_values[f'{facet}_project_id'] = project_id
        
    save_facet_values(saved_facet_values)
    messagebox.showinfo('Success', 'Facet values saved!')

def start_gui_event_loop(root):
    root.mainloop()