import tkinter as tk
from tkinter import messagebox
from logger import Logger
from utils import save_facet_values
from config import TOGGL_PROJECT_IDS, LISTEN_PORT
import threading
import socket

class TkGUI(tk.Tk):
    
    facet_entries = {}
    project_selectors = {}
    saved_facet_values = {}
    gui_logger = []
    
    def __init__(self):
        super().__init__(className='TimeflipToggl')
        self.title("Timeflip Toggl Logger")
        
        # Set the icon for the main window using PhotoImage
        icon_path = 'assets/app_icon.png'
        icon_image = tk.PhotoImage(file=icon_path)
        self.iconphoto(False, icon_image)

        # Create a frame for the facet inputs
        facet_frame = tk.Frame(self)
        facet_frame.pack(pady=10)
        
        for i in range(1, 13):
            # Create an entry description for each facet
            label = tk.Label(facet_frame, text=f"Facet {i}:")
            label.grid(row=i-1, column=0, padx=5, pady=5)
            entry = tk.Entry(facet_frame)
            entry.grid(row=i-1, column=1, padx=5, pady=5)
            self.facet_entries[f'Facet {i}'] = entry
            
            # Create a project selector for each facet
            proj_selector = tk.StringVar()
            proj_selector.set('')
            self.project_selectors[f'Facet {i}'] = proj_selector
            project_selector_menu = tk.OptionMenu(facet_frame, proj_selector, *TOGGL_PROJECT_IDS.values())
            project_selector_menu.grid(row=i-1, column=2, padx=5, pady=5)
            
        # Create SAVE button
        save_button = tk.Button(self, text='SAVE', command=lambda: self.save_facet_values_on_click(self.facet_entries, self.saved_facet_values, self.project_selectors))
        save_button.pack(pady=5)

        # Create a text widget to display logs
        log_text = tk.Text(self, width=80, height=20)
        log_text.pack()
        
        # Set up logger
        logger = Logger(log_text)
        self.gui_logger = logger.logger
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.start_server()
        
    def start_server(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', LISTEN_PORT))
        server_socket.listen(1)  # Listen for incoming connections
        while True:
            conn, addr = server_socket.accept()  # Accept a connection
            print('Connected by', addr)
            message = conn.recv(1024).decode()  # Receive the message
            print('Received:', message)
            if message == 'activate':
                self.activate()  # Call activate method
            elif message == 'exit':
                self.destroy()  # Destroy the window and exit the application
                break  # Break the loop to stop the server thread
            conn.close()  # Close the connection
        
    def on_close(self):
        self.withdraw()  # Hide the window instead of destroying it
        
    def activate(self):
        self.deiconify()  # Show the window
        self.lift()  # Bring the window to the foreground

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