from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import os

def run_tray_icon(root):
    def show_window():
        root.deiconify()

    def hide_window():
        root.withdraw()

    menu = Menu(
        MenuItem('Show', show_window),
        MenuItem('Hide', hide_window),
        MenuItem('Exit', lambda: os._exit(0))
    )

    icon_image = Image.open('assets/icon.ico')

    def run_icon():
        icon = Icon("Timeflip Logger", icon_image, menu=menu)
        icon.run()

    thread = threading.Thread(target=run_icon)
    thread.daemon = True
    thread.start()