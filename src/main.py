# pyinstaller --onefile --noconsole --icon=assets/icon.ico --hidden-import winrt.windows.foundation.collections src/main.py

from ctypes import windll
from gui import create_main_window, start_gui_event_loop
from tray_icon import run_tray_icon
from timeflip import start_timeflip_thread
from utils import load_facet_values

def main():
    
    # Set the App User Model ID
    try:
        myappid = 'sirlouen.timeflip-toggle.0.0.1'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception as e:
        print(f"Failed to set App User Model ID: {e}")
    
    root, facet_entries, gui_logger, saved_facet_values, project_selectors = create_main_window()
    
    # Load facet values from file
    load_facet_values(facet_entries, saved_facet_values, project_selectors)
    
    # Start the system tray icon in a separate thread
    run_tray_icon(root)
    
    # Start the TimeFlip thread
    start_timeflip_thread(saved_facet_values, gui_logger)
    
    # Start the GUI event loop
    start_gui_event_loop(root)

if __name__ == "__main__":
    main()