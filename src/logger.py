import logging
import tkinter as tk

class Logger:
    def __init__(self, text_widget):
        self.logger = logging.getLogger('gui_logger')
        self.logger.setLevel(logging.DEBUG)
        self.text_widget = text_widget
        self._setup_handler()

    def _setup_handler(self):
        class GUIHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.see(tk.END)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        gui_handler = GUIHandler(self.text_widget)
        gui_handler.setFormatter(formatter)
        self.logger.addHandler(gui_handler)