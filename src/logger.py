import logging
import tkinter as tk

# Create a logger

global gui_logger
gui_logger = logging.getLogger('gui_logger')
gui_logger.setLevel(logging.INFO)

def setup_gui_logger(log_text):  
    class GUIHandler(logging.Handler):
        def __init__(self, text_widget):
            logging.Handler.__init__(self)
            self.text_widget = text_widget
        
        def emit(self, record):
            msg = self.format(record)
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    gui_handler = GUIHandler(log_text)
    gui_handler.setFormatter(formatter)
    gui_logger.addHandler(gui_handler)