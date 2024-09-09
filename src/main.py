# For Bluetooth to work, is important to load winrt.windows.foundation.collections in the main.py file.
# pyinstaller --onefile --noconsole --icon=assets/icon.ico --hidden-import winrt.windows.foundation.collections src/main.py

from ctypes import windll
import gui
from tray_icon import run_tray_icon
from timeflip import start_timeflip_thread
from utils import load_facet_values
from config import LISTEN_PORT
import socket

def main():  
    # Try to connect to an existing instance
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', LISTEN_PORT))  # Connect to the server
        client_socket.sendall(b'activate')  # Send the activate message
        print("Activated existing instance")
    except ConnectionRefusedError:
        print("No existing instance found, starting a new one")
        
        try:
            myappid = 'sirlouen.windows-testing.0.0.1'
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Failed to set App User Model ID: {e}")
        
        # Start a new instance
        root = gui.TkGUI()

        # Load facet values from file
        load_facet_values(root.facet_entries, root.saved_facet_values, root.project_selectors)

        # Start the system tray icon in a separate thread
        run_tray_icon(root)

	# Start the TimeFlip thread
        start_timeflip_thread(root.saved_facet_values, root.gui_logger)
        
        # Start the GUI event loop
        root.mainloop()
    finally:
        print("Closing client socket")
        client_socket.close()  # Close the client socket

if __name__ == "__main__":
    main()