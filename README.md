# TimeFlip Toggl Bridge

This project is a desktop application that integrates with the TimeFlip device and Toggl to track time spent on various tasks. The application uses a GUI to configure facets and associate them with Toggl projects.

## Features

- **GUI Interface**: Configure facets and associate them with specific Toggl projects.
- **Time Tracking**: Automatically track time based on the current facet detected by the TimeFlip device.
- **Toggl Integration**: Send time entries to Toggl with descriptions and project IDs.
- **System Tray Icon**: Minimize the application to the system tray for background operation.

## Requirements

- Python 3.x
- Required Python packages: `ctypes`, `tkinter`, `requests`, `bleak`, `pytimefliplib`, `asyncio`, `threading`, `json`, `base64`, `socket`
- TimeFlip device
- Toggl account and [API token](https://track.toggl.com/profile#api-token)

## Setup

### Manual Installation

1. **Install Dependencies**

Use pip to install the required Python packages:

```bash
pip install -r requirements.txt
```

2. **Configure Environment**

Create the `src/config.py` file with the following variables (there is a `config.sample.py` provided in the `src` folder):	

```python
DEVICE_MAC = 'your-device-mac-address'
DEVICE_PASSWORD = 'your-device-password'
TOGGL_API_TOKEN = 'your-toggl-api-token'
TOGGL_WORKSPACE_ID = 'your-workspace-id'
TOGGL_PROJECT_IDS = {
    1: 'Project One',
    2: 'Project Two',
    3: 'Project Three'
}
LISTEN_PORT = 12345
```

Also create a `data` folder to store the facet values in a `facet_values.json` file.

4. **Run the Application**
Execute the main script:
```bash
python src/main.py
```

### Automatic Installation

Soon I will be releasing some binaries for Windows, MacOS and Linux.

## Usage
* **GUI Configuration**: Use the GUI to enter facet descriptions and select associated Toggl projects. Click "SAVE" to store these settings.
* **Time Tracking**: The application will automatically track time based on the current facet detected by the TimeFlip device.
* **STOP Functionality**: Assign the "STOP" description to a facet to stop all current tasks in Toggl without starting a new one.

## Code Overview
### main.py
Initializes the application, sets the App User Model ID, and starts the GUI and TimeFlip threads.
### gui.py
Creates the main window using Tkinter, allowing users to input facet descriptions and select projects.
### utils.py
Handles loading and saving of facet values and project IDs to/from facet_values.json.
### timeflip.py
Manages communication with the TimeFlip device and sends time entries to Toggl based on the current facet.
### toggle.py
Contains functions to interact with the Toggl API, stopping current tasks and sending new time entries.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [Toggl](https://engineering.toggl.com/docs/), for the time tracking API.
- [pytimefliplib](https://github.com/pierre-24/pytimefliplib), for the TimeFlip device library.
- [TimeFlip](https://timeflip.io/), for the device that inspired this project.