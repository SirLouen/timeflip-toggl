from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import socket
from config import LISTEN_PORT

def run_tray_icon(root):
    def show_window():
        root.activate()

    def hide_window():
        root.on_close()

    def exit_application(icon):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect(('localhost', LISTEN_PORT))  # Connect to the server
            client_socket.sendall(b'exit')  # Send the exit message
            print("Exiting application")
        except ConnectionRefusedError:
            print("No running instance found")
        finally:
            client_socket.close()  # Close the client socket
        icon.stop()  # Stop the icon loop

    menu = Menu(
        MenuItem('Show', show_window),
        MenuItem('Hide', hide_window),
        MenuItem('Exit', exit_application)
    )

    icon_image = Image.open('assets/icon.ico')

    def run_icon():
        icon = Icon("Timeflip Logger", icon_image, menu=menu)
        icon.run()

    thread = threading.Thread(target=run_icon)
    thread.daemon = True
    thread.start()